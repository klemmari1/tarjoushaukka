import pprint
import re
from datetime import datetime, timezone
from typing import List, Tuple

import pytz
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from flask import jsonify
from sqlalchemy import desc

import settings
from mail_service import send_mail, send_tg
from models.db import db
from models.emails import Email
from models.posts import Post


def get_posts() -> List[Post]:
    return Post.query.order_by(desc(Post.time)).all()


def drop_post_table() -> None:
    Post.__table__.drop(db.engine)
    db.create_all()


def print_posts() -> None:
    posts = get_posts()
    pprint.pprint(jsonify(posts))


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=settings.HEADERS)
    if not response.ok:
        raise Exception(
            f"Failed to fetch soup! Status: {response.status_code}. Content: {response.content.decode('utf-8')}."
        )
    return BeautifulSoup(response.content, features="html.parser")


def get_last_page_url() -> str:
    soup = get_soup(settings.POSTS_URL)

    ul_elem = soup.find("ul", {"class": "pageNav-main"})
    li_elems = ul_elem.find_all("li", recursive=False)
    last_page_li = li_elems[-1]
    last_page_a = last_page_li.find("a")

    url = last_page_a["href"]
    return url


def add_hilight(post: Post, hilights: List[Post]) -> None:
    tz = pytz.timezone("Europe/Helsinki")
    post_time = post.time.replace(tzinfo=tz)
    seconds_since_post = (datetime.now(tz) - post_time).total_seconds()
    if not post.is_sent and (
        (
            post.likes >= 5
            and seconds_since_post <= 3 * 60 * 60  # >=5 likes within the first 3h
        )
        or (
            post.likes >= 2
            and seconds_since_post <= 30 * 60  # >=2 likes within the first 0.5h
        )
    ):
        post.is_sent = True
        hilights.append(post)


def handle_bs_and_create_hilights(
    hilights: List[Post],
    post_bs: BeautifulSoup,
    saved_posts: List[Post],
    page_number: int,
) -> None:
    post_id = int(post_bs["data-content"].split("-")[-1])
    post_url = post_bs.find("a", {"class": "u-concealed"})["href"]
    post_content = post_bs.find("div", {"class": "bbWrapper"})
    post_content_fist_link = post_bs.select_one("a")["href"]
    post_content_html = str(post_content).strip()
    post_content_plain = f"{post_content.text.strip()}\n\n{post_content_fist_link}"
    post_datetime = parse(post_bs.find("time", {"class": "u-dt"})["datetime"])
    reactions_link = post_bs.find("a", {"class": "reactionsBar-link"})
    reactions_count = 0
    if reactions_link:
        reactions_text = reactions_link.text
        p = re.compile(" ja (.*) muuta")
        reactions = p.findall(reactions_text)
        if reactions:
            reactions_count += int(reactions[0]) + 3
        elif " ja " in reactions_text:
            reactions_count = 2

    existing_post = next((x for x in saved_posts if x.id == post_id), None)
    if not existing_post:
        post = Post(
            id=post_id,
            likes=reactions_count,
            page=page_number,
            time=post_datetime,
            url=settings.BASE_URL + post_url,
            content=post_content_html,
            content_plain=post_content_plain,
            is_sent=False,
        )
        db.session.add(post)
        add_hilight(post, hilights)
    else:
        existing_post.content = post_content_html
        existing_post.content_plain = post_content_plain
        existing_post.likes = reactions_count
        add_hilight(existing_post, hilights)


def fetch_hilights_from_url(
    url: str, saved_posts: List[Post], page_number: int
) -> List[Post]:
    hilights: List[Post] = []

    soup = get_soup(url)
    posts = soup.findAll("article", {"class": "message"})
    for post_bs in posts:
        handle_bs_and_create_hilights(hilights, post_bs, saved_posts, page_number)
    return hilights


def fetch_posts():
    last_page_url = get_last_page_url()
    last_page_url_split = last_page_url.split("-")
    last_page_number = int(last_page_url_split[-1])
    last_page_url_split[-1] = str(last_page_number - 1)
    second_to_last_page_url = "-".join(last_page_url_split)

    saved_posts = get_posts()
    # Last page
    hilights1 = fetch_hilights_from_url(
        settings.BASE_URL + last_page_url, saved_posts, last_page_number
    )

    # Second to last page
    hilights2 = fetch_hilights_from_url(
        settings.BASE_URL + second_to_last_page_url,
        saved_posts,
        last_page_number - 1,
    )
    db.session.commit()

    hilights = hilights1 + hilights2
    send_mail(hilights)
    send_tg(hilights)


def delete_old_posts() -> None:
    last_page_url = get_last_page_url()
    last_page = int(last_page_url.split("-")[-1])
    posts = Post.query.filter(Post.page < last_page - 1)
    for post in posts:
        db.session.delete(post)
    db.session.commit()


def subscribe_email(email_address: str) -> bool:
    email = Email.query.get(email_address)
    if not email:
        email = Email(email=email_address)
        email.subscribe()
        return True
    return False


def unsubscribe_email(email_address: str) -> bool:
    email = Email.query.get(email_address)
    if email:
        email.unsubscribe()
        return True
    return False

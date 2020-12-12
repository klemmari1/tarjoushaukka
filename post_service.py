import re
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

import settings
from mail_service import send_mail
from posts import Post


def get_posts() -> dict:
    return Post.load_posts()


def save_posts(posts: dict) -> None:
    Post.save_posts(posts)


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=settings.HEADERS)
    if not response.ok:
        raise Exception(
            f"Failed to fetch soup! Status: {response.status}. Content: {response.content}."
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


def fetch_posts_from_url(url: str, page_number: int) -> List[Post]:
    soup = get_soup(url)
    posts_list = []

    posts = soup.findAll("article", {"class": "message"})
    for post in posts:
        post_id = int(post["data-content"].split("-")[-1])
        post_url = post.find("a", {"class": "u-concealed"})["href"]
        post_content = post.find("div", {"class": "bbWrapper"}).text
        reactions_link = post.find("a", {"class": "reactionsBar-link"})
        reactions_count = 2
        if reactions_link:
            reactions_text = reactions_link.text
            p = re.compile("ja (.*) muuta")
            reactions = p.findall(reactions_text)
            if reactions:
                reactions_count = int(reactions[0])
        posts_list.append(
            Post(
                post_id,
                reactions_count,
                page_number,
                settings.BASE_URL + post_url,
                post_content.strip(),
            )
        )
    return posts_list


def check_new_posts_and_hilights(
    posts_dict: dict, new_posts: list
) -> Tuple[dict, List[Post]]:
    hilights = []
    post_ids = posts_dict.keys()
    for post in new_posts:
        post_id = post.id
        if post_id not in post_ids:
            posts_dict[post_id] = post.to_dict()
            if post.likes >= 5:
                hilights.append(post)
        else:
            prev_likes = posts_dict[post_id]["likes"]
            if prev_likes < 5 and post.likes >= 5:
                hilights.append(post)
    return hilights


def fetch_posts():
    posts_dict = get_posts()

    last_page_url = get_last_page_url()
    last_page_url_split = last_page_url.split("-")
    last_page_number = int(last_page_url_split[-1])
    last_page_url_split[-1] = str(last_page_number - 1)
    second_to_last_page_url = "-".join(last_page_url_split)

    posts1 = fetch_posts_from_url(settings.BASE_URL + last_page_url, last_page_number)
    hilights1 = check_new_posts_and_hilights(posts_dict, posts1)

    posts2 = fetch_posts_from_url(
        settings.BASE_URL + second_to_last_page_url, last_page_number - 1
    )
    hilights2 = check_new_posts_and_hilights(posts_dict, posts2)

    send_mail(hilights1 + hilights2)

    save_posts(posts_dict)


if __name__ == "__main__":
    fetch_posts()

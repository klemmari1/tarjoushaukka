import os
import re
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from posts import Post


class PostService:

    BASE_URL = "https://bbs.io-tech.fi/"
    POSTS_URL = "https://bbs.io-tech.fi/threads/hyvaet-tarjoukset-ei-keskustelua.151/"
    HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    @staticmethod
    def get_posts() -> dict:
        return Post.load_posts()

    @staticmethod
    def save_posts(posts: dict) -> None:
        Post.save_posts(posts)

    def get_soup(self, url: str) -> BeautifulSoup:
        response = requests.get(url, headers=self.HEADERS)
        if not response.ok:
            raise Exception(
                f"Failed to fetch soup! Status: {response.status}. Content: {response.content}."
            )
        return BeautifulSoup(response.content, features="html.parser")

    def get_last_page_url(self) -> str:
        soup = self.get_soup(self.POSTS_URL)

        ul_elem = soup.find("ul", {"class": "pageNav-main"})
        li_elems = ul_elem.find_all("li", recursive=False)
        last_page_li = li_elems[-1]
        last_page_a = last_page_li.find("a")

        url = last_page_a["href"]
        return url

    def fetch_posts_from_url(self, url: str, page_number: int) -> List[Post]:
        soup = self.get_soup(url)
        posts_list = []

        posts = soup.findAll("article", {"class": "message"})
        for post in posts:
            post_id = int(post["data-content"].split("-")[-1])
            post_url = post.find("a", {"class": "u-concealed"})["href"]
            post_content = post.find("div", {"class": "bbWrapper"}).text
            reactions_link = post.find("a", {"class": "reactionsBar-link"})
            reactions_count = 0
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
                    self.BASE_URL + post_url,
                    post_content.strip(),
                )
            )
        return posts_list

    def check_new_posts_and_hilights(
        self, posts_dict: dict, new_posts: list
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

    def fetch_posts(self):
        posts_dict = self.get_posts()

        last_page_url = self.get_last_page_url()
        last_page_url_split = last_page_url.split("-")
        last_page_number = int(last_page_url_split[-1])
        last_page_url_split[-1] = str(last_page_number - 1)
        second_to_last_page_url = "-".join(last_page_url_split)

        posts1 = self.fetch_posts_from_url(
            self.BASE_URL + last_page_url, last_page_number
        )
        hilights1 = self.check_new_posts_and_hilights(posts_dict, posts1)

        posts2 = self.fetch_posts_from_url(
            self.BASE_URL + second_to_last_page_url, last_page_number - 1
        )
        hilights2 = self.check_new_posts_and_hilights(posts_dict, posts2)

        ms = MailService()
        # ms.send_mail(hilights1 + hilights2)

        self.save_posts(posts_dict)


class MailService:
    # Load ENV variables
    FROM_EMAIL = os.environ.get("FROM_EMAIL")
    TO_EMAIL = os.environ.get("TO_EMAIL")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USER = os.environ.get("MAIL_USER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    def send_mail(self, hilights: List[Post]) -> None:
        hilight_messages = (hilight.content for hilight in hilights)
        message = "\n\n".join(hilight_messages)

        msg = MIMEText(message)
        msg["Subject"] = "You have new sale alerts!"
        msg["From"] = self.FROM_EMAIL
        msg["To"] = self.TO_EMAIL

        s = SMTP(self.MAIL_SERVER, self.MAIL_PORT)

        s.login(self.MAIL_USER, self.MAIL_PASSWORD)
        s.sendmail(self.FROM_EMAIL, self.TO_EMAIL, msg.as_string())
        s.quit()


if __name__ == "__main__":
    ps = PostService()
    ps.fetch_posts()

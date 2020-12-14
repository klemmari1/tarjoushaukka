from __future__ import annotations

import pickle
import pprint
from dataclasses import dataclass
from datetime import datetime
from os import path

from settings import POSTS_FILE


@dataclass
class Post:
    id: int
    likes: int
    page: int
    time: datetime
    url: str
    content: str

    @staticmethod
    def load_posts() -> dict:
        if path.isfile(POSTS_FILE):
            with open(POSTS_FILE, "rb") as posts_file:
                return pickle.load(posts_file)
        else:
            return {}

    @staticmethod
    def save_posts(posts: dict) -> None:
        with open(POSTS_FILE, "wb") as posts_file:
            pickle.dump(posts, posts_file)

    @staticmethod
    def delete_all_posts() -> None:
        with open(POSTS_FILE, "wb") as posts_file:
            pickle.dump({}, posts_file)

    @staticmethod
    def print_posts() -> None:
        pprint.pprint(Post.load_posts())

    @staticmethod
    def delete_old_posts() -> None:
        from post_service import get_last_page_url

        posts_dict = Post.load_posts()
        last_page_url = get_last_page_url()
        last_page = int(last_page_url.split("-")[-1])
        for post_id, post in dict(posts_dict).items():
            if post["page"] < last_page - 1:
                del posts_dict[post_id]

        Post.save_posts(posts_dict)

    def to_dict(self) -> dict:
        post_dict = self.__dict__
        del post_dict["id"]
        return post_dict


if __name__ == "__main__":
    Post.print_posts()

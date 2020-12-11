from __future__ import annotations

import pickle
import pprint
from dataclasses import dataclass
from os import path

POSTS_FILE = "posts.pkl"


@dataclass
class Post:
    id: int
    likes: int
    page: int
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
    def delete_posts() -> None:
        with open(POSTS_FILE, "wb") as posts_file:
            pickle.dump({}, posts_file)

    @staticmethod
    def print_posts() -> None:
        pprint.pprint(Post.load_posts())

    def to_dict(self) -> dict:
        post_dict = self.__dict__
        del post_dict["id"]
        return post_dict


if __name__ == "__main__":
    Post.print_posts()

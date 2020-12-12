from post_service import fetch_posts
from posts import Post


def fetch_posts() -> None:
    fetch_posts()


def delete_old_posts() -> None:
    Post.delete_old_posts()

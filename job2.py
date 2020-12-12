from posts import Post


def delete_old_posts() -> None:
    Post.delete_old_posts()


if __name__ == "__main__":
    delete_old_posts()

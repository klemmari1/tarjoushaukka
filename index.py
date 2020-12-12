from flask_api import FlaskAPI

from post_service import fetch_posts, get_posts
from posts import Post

app = FlaskAPI(__name__)


@app.route("/", methods=["GET"])
def home():
    return {"hello": "world"}


@app.route("/posts/", methods=["GET"])
def posts_list():
    return get_posts()


@app.route("/posts/fetch/", methods=["GET"])
def posts_fetch():
    fetch_posts()
    return {"status": "ok"}


@app.route("/posts/delete_old/", methods=["GET"])
def posts_delete_old():
    Post.delete_old_posts()
    return {"status": "ok"}


@app.route("/posts/delete_all/", methods=["GET"])
def posts_delete_all():
    Post.delete_all_posts()
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)

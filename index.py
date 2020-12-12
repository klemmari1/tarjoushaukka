from flask_api import FlaskAPI

from post_service import get_posts

app = FlaskAPI(__name__)


@app.route("/", methods=["GET"])
def home():
    return {"hello": "world"}


@app.route("/posts/", methods=["GET"])
def posts_list():
    return get_posts()


if __name__ == "__main__":
    app.run(debug=True)

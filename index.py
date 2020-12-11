from flask_api import FlaskAPI

from services import PostService

app = FlaskAPI(__name__)


@app.route("/", methods=["GET"])
def home():
    return {"hello": "world"}


@app.route("/posts/", methods=["GET"])
def posts_list():
    return PostService.get_posts()


if __name__ == "__main__":
    app.run(debug=True)

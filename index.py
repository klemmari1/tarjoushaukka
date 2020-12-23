import urllib

from flask.json import jsonify
from flask_api import FlaskAPI

import settings
from post_service import delete_all_posts, delete_old_posts, fetch_posts, get_posts
from posts import db

app = FlaskAPI(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


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
    delete_old_posts()
    return {"status": "ok"}


@app.route("/posts/delete_all/", methods=["GET"])
def posts_delete_all():
    delete_all_posts()
    return {"status": "ok"}


if __name__ == "__main__":
    conn_str = "sqlite:///app.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = conn_str

    db.init_app(app)
    app.app_context().push()
    db.create_all()

    app.run(debug=True, port=5000)
else:
    driver = "{ODBC Driver 17 for SQL Server}"
    db_name = settings.DATABASE_NAME
    user = settings.DATABASE_USER
    password = settings.DATABASE_PASSWORD

    conn = f"""Driver={driver};Server=tcp:{db_name}.database.windows.net,1433;Database={db_name};
    Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""

    params = urllib.parse.quote_plus(conn)
    conn_str = "mssql+pyodbc:///?autocommit=true&odbc_connect={}".format(params)
    app.config["SQLALCHEMY_DATABASE_URI"] = conn_str

    db.init_app(app)
    app.app_context().push()
    db.create_all()

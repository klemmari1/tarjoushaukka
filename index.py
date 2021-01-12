import urllib

from flask import redirect, render_template, request, session, url_for
from flask_api import FlaskAPI

import settings
from mail_service import subscribe_email, unsubscribe_email
from models.db import db
from post_service import delete_old_posts, drop_post_table, fetch_posts, get_posts

app = FlaskAPI(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = settings.SECRET_KEY


@app.route("/", methods=["GET"])
def home():
    unsubscribe = request.args.get("unsubscribe")
    if unsubscribe:
        is_unsubscribed = unsubscribe_email(unsubscribe)
        if is_unsubscribed:
            session["success"] = "Email unsubscribed from bargain alerts!"
        else:
            session["warning"] = "Email is not subscribed to bargain alerts!"
    return render_template(
        "index.html",
        success=session.pop("success", None),
        warning=session.pop("warning", None),
    )


@app.route("/", methods=["POST"])
def handle_email_form():
    sub_type = request.form["sub-type"]
    email_input = request.form["email-input"][:120]

    if sub_type == "subscribe":
        is_subscribed = subscribe_email(email_input)
        if is_subscribed:
            session["success"] = "Email subscribed to bargain alerts!"
        else:
            session["warning"] = "Email already subscribed to bargain alerts!"
    elif sub_type == "unsubscribe":
        is_unsubscribed = unsubscribe_email(email_input)
        if is_unsubscribed:
            session["success"] = "Email unsubscribed from bargain alerts!"
        else:
            session["warning"] = "Email is not subscribed to bargain alerts!"
    return redirect(url_for("home"))


@app.route("/posts/", methods=["GET"])
def posts_list():
    return get_posts()


@app.route("/posts/fetch/", methods=["GET"])
def posts_fetch():
    fetch_posts(request)
    return {"status": "ok"}


@app.route("/posts/delete_old/", methods=["GET"])
def posts_delete_old():
    delete_old_posts()
    return {"status": "ok"}


@app.route("/posts/delete_all/", methods=["GET"])
def drop_posts():
    drop_post_table()
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

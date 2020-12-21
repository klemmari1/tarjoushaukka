import os

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

POSTS_FILE = "posts.pkl"

BASE_URL = "https://bbs.io-tech.fi/"

POSTS_URL = "https://bbs.io-tech.fi/threads/hyvaet-tarjoukset-ei-keskustelua.151/"

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


# Load ENV variables
FROM_EMAIL = os.getenv("FROM_EMAIL", "test")

TO_EMAIL = os.getenv("TO_EMAIL", "test, test").split(", ")

EMAIL_API_KEY = os.getenv("EMAIL_API_KEY", "test")

TG_SEND_URL = os.getenv("TG_SEND_URL", "http://localhost:5000")

TG_KEY = os.getenv("TG_KEY", "test")

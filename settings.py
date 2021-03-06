import os

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

BASE_URL = "https://bbs.io-tech.fi"

POSTS_URL = "https://bbs.io-tech.fi/threads/hyvaet-tarjoukset-ei-keskustelua.151/"

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


# Load ENV variables
SECRET_KEY = os.getenv("SECRET_KEY", "test")

DATABASE_NAME = os.getenv("DATABASE_NAME", "test")

DATABASE_USER = os.getenv("DATABASE_USER", "test")

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "test")

FROM_EMAIL = os.getenv("FROM_EMAIL", "a@b.com")

EMAIL_API_KEY = os.getenv("EMAIL_API_KEY", "test")

EXTERNAL_SEND_URL = os.getenv("EXTERNAL_SEND_URL", "test")

EXTERNAL_SEND_KEY = os.getenv("EXTERNAL_SEND_KEY", "test")

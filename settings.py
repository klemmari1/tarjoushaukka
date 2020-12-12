import os

from dotenv import load_dotenv

load_dotenv()


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
FROM_EMAIL = os.getenv("FROM_EMAIL")

TO_EMAIL = os.getenv("TO_EMAIL")

EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

import datetime
from typing import List

import jwt
import requests
import sendgrid
from sendgrid import Content, Email, Mail

import settings
from posts import Post


def get_auth_token():
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
            "iat": datetime.datetime.utcnow(),
            "sub": "dummy",
        }
        return jwt.encode(payload, settings.TG_KEY, algorithm="HS256"), True
    except Exception as e:
        return e, False


def send_tg(hilights: List[Post]) -> None:
    if not hilights:
        return
    hilight = hilights[0]
    message = f"{hilight.url}\n\n{hilight.content_plain}"
    auth_token, success = get_auth_token()
    if success:
        try:
            response = requests.post(
                settings.TG_SEND_URL,
                data=message.encode("utf-8"),
                headers={"Authorization": auth_token},
            )
            print(response.status_code)
            print(response.content)
        except Exception as e:
            print(str(e))


def send_mail(hilights: List[Post]) -> None:
    if not hilights:
        return
    hilight_messages = (
        f"{hilight.url}<br/><br/>{hilight.content}" for hilight in hilights
    )
    message = "<br/><br/><br/><br/>".join(hilight_messages)

    sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_API_KEY)
    from_email = Email(settings.FROM_EMAIL)
    subject = "You have new sale alerts!"
    content = Content("text/html", message)
    print(settings.FROM_EMAIL)
    print(settings.TO_EMAIL)
    print(settings.EMAIL_API_KEY)

    mail = Mail(from_email, settings.TO_EMAIL, subject, content)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
    except Exception as e:
        print(str(e))


def test_mail() -> None:
    post = Post(
        id=1, likes=2, page=1, time=None, url="test_url", content="test_content"
    )
    send_mail([post])
    send_tg([post])


if __name__ == "__main__":
    test_mail()

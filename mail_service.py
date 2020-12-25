import datetime
import time
from typing import List

import jwt
import requests
import sendgrid
from sendgrid import Content
from sendgrid import Email as SEmail
from sendgrid import Mail as SMail

import settings
from models.emails import Email
from models.posts import Post


def get_auth_token():
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
            "iat": datetime.datetime.utcnow(),
            "sub": "tarjoushaukka",
        }
        return jwt.encode(payload, settings.EXTERNAL_SEND_KEY, algorithm="HS256"), True
    except Exception as e:
        return e, False


def send_post(hilights: List[Post]) -> None:
    if not hilights:
        return
    for hilight in hilights:
        message = f"{hilight.url}\n\n{hilight.content_plain}"
        auth_token, success = get_auth_token()
        if success:
            try:
                response = requests.post(
                    settings.EXTERNAL_SEND_URL,
                    data=message.encode("utf-8"),
                    headers={"Authorization": auth_token},
                )
                print(response.status_code)
                print(response.content)
            except Exception as e:
                print(str(e))
        time.sleep(3)


def send_mail(hilights: List[Post]) -> None:
    if not hilights:
        return
    hilight_messages = (
        f"{hilight.url}<br/><br/>{hilight.content}" for hilight in hilights
    )
    message = "<br/><br/><br/><br/>".join(hilight_messages)

    sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_API_KEY)
    from_email = SEmail(settings.FROM_EMAIL)
    subject = "You have new sale alerts!"
    content = Content("text/html", message)

    print(settings.FROM_EMAIL)
    to_emails = [email.email for email in Email.query.all()]
    print(to_emails)

    mail = SMail(from_email, to_emails, subject, content)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
    except Exception as e:
        print(str(e))


def subscribe_email(email_address: str) -> bool:
    email = Email.query.get(email_address)
    if not email:
        email = Email(email=email_address)
        email.subscribe()
        return True
    return False


def unsubscribe_email(email_address: str) -> bool:
    email = Email.query.get(email_address)
    if email:
        email.unsubscribe()
        return True
    return False

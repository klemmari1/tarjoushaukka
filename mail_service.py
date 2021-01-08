import datetime
import time
from typing import List

import jwt
import requests
import sendgrid
from flask import Request
from sendgrid import Content, From, Mail, To

import settings
from models.emails import Email
from models.posts import Post


def get_auth_token():
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30),
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


def send_mail(hilights: List[Post], request: Request = None) -> None:
    if not hilights:
        return
    title_section = f'<h2><a href="{request.url_root if request else ""}">Tarjoushaukka</a> sale alerts</h2>'
    hilight_messages_section = list(
        f"{hilight.url}<br/><br/>{hilight.content}" for hilight in hilights
    )
    unsubscribe_section = f'<p style="font-size:12px"><a href="{request.url_root if request else ""}?unsubscribe=-email-">Unsubscribe</a> from sale alerts</p>'
    sections = [title_section] + hilight_messages_section + [unsubscribe_section]
    message = "<br/><br/><br/>".join(sections)

    sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_API_KEY)
    from_email = From(settings.FROM_EMAIL, "Tarjoushaukka")
    subject = "You have new sale alerts!"
    content = Content("text/html", message)

    emails = Email.query.all()
    to_emails = [
        To(email=email.email, substitutions={"-email-": email.email})
        for email in emails
    ]

    mail = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=content,
        is_multiple=True,
    )
    try:
        print("SENDING MAIL...")
        print(emails)
        print(message)
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

import datetime
import time
from typing import List

import requests
import sendgrid
from sendgrid import Content, Email, Mail

import settings
from posts import Post
from producer import publish_sale_alert


def send_tg(hilights: List[Post]) -> None:
    if not hilights:
        return
    for hilight in hilights:
        message = f"{hilight.url}\n\n{hilight.content_plain}"
        publish_sale_alert("io-tech", message)
        time.sleep(3)


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

    mail = Mail(from_email, settings.TO_EMAIL, subject, content)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
    except Exception as e:
        print(str(e))

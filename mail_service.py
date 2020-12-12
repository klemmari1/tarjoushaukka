from typing import List

import sendgrid
from sendgrid.helpers.mail import *

import settings
from posts import Post


def send_mail(hilights: List[Post]) -> None:
    if hilights:
        hilight_messages = (
            f"{hilight.url}:\n{hilight.content}" for hilight in hilights
        )
        message = "\n\n\n".join(hilight_messages)

        sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_API_KEY)
        from_email = Email(settings.FROM_EMAIL)
        to_email = To(settings.TO_EMAIL)
        subject = "You have new sale alerts!"
        content = Content("text/plain", message)
        print(settings.FROM_EMAIL)
        print(settings.TO_EMAIL)
        print(settings.EMAIL_API_KEY)
        print(message)

        mail = Mail(from_email, to_email, subject, content)
        sg.client.mail.send.post(request_body=mail.get())

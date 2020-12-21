from typing import List

import sendgrid
from sendgrid import Content, Email, Mail

import settings
from posts import Post


def send_mail(hilights: List[Post]) -> None:
    if hilights:
        hilight_messages = (
            f"{hilight.url}\n\n{hilight.content}" for hilight in hilights
        )
        message = "<br/> <br/> <br/> <br/>".join(hilight_messages)

        sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_API_KEY)
        from_email = Email(settings.FROM_EMAIL)
        subject = "You have new sale alerts!"
        content = Content("text/html", message)
        print(settings.FROM_EMAIL)
        print(settings.TO_EMAIL)
        print(settings.EMAIL_API_KEY)
        print(message)

        mail = Mail(from_email, settings.TO_EMAIL, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)


def test_mail() -> None:
    post = Post(
        id=1, likes=2, page=1, time=None, url="test_url", content="test_content"
    )
    send_mail([post])


if __name__ == "__main__":
    test_mail()

import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def send_reset_code_email(to_email, code):
    sender = os.environ["MAIL_USERNAME"]
    app_password = os.environ["MAIL_APP_PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = "Your TicketFlow password reset code"
    msg["From"] = f"TicketFlow <{sender}>"
    msg["To"] = to_email
    msg.set_content(
        f"Your password reset code is: {code}\n\n"
        "This code expires in 10 minutes. If you didn't request this, you can ignore this email."
    )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(sender, app_password)
        server.send_message(msg)

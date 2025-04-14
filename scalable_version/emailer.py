import os
import sendgrid
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email, subject, html_content):
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    email = Mail(
        from_email=os.getenv("EMAIL_FROM"),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    sg.send(email)
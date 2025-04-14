import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def generate_prompt(plattform, tema):
    return f"""Lag 3 engasjerende captions for sosiale medier basert på:

Plattform: {plattform}
Tema: {tema}

Regler:
- Maks 3 linjer per caption
- Bruk emojis og relevante hashtags
- Svar kun med selve captionene, nummerert
"""

def format_captions(text):
    return text.replace("\n", "<br>")

def send_email(to_email, subject, html_content):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = to_email
    msg.set_content("Din e-postklient støtter ikke HTML.")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as smtp:
        smtp.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        smtp.send_message(msg)
# utils.py

import os
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_caption(topic, platform):
    prompt = f"Generer en engasjerende caption til {platform} om emnet: {topic}.\n\n"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du er en kreativ tekstforfatter for sosiale medier."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()


def send_email(receiver_email, caption_text):
    sender_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Din nye caption er klar!"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>🚀 Din caption er klar!</h2>
        <p>{caption_text}</p>
        <hr>
        <p>Hilsen InstaPrompt</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

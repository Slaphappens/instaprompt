# /mvp/app.py

from flask import Flask, request, render_template_string
import os
import openai
from dotenv import load_dotenv

from utils import generate_prompt, format_captions, send_email

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Debug-logging
print("🔧 Loading environment variables...")

# Get and validate environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is missing")
openai.api_key = OPENAI_API_KEY

EMAIL_FROM = os.getenv("EMAIL_FROM")
if not EMAIL_FROM:
    raise ValueError("❌ EMAIL_FROM is missing")

print("✅ App environment ready")

# Home route
@app.route("/")
def home():
    return "InstaPrompt is running!"

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    print("📥 Webhook triggered")

    try:
        data = request.get_json()
        print("📦 Incoming JSON:", data)
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return "Invalid JSON", 400

    # Parse values from Tally-like structure
    try:
        fields = {f["label"]: f["value"] for f in data["fields"]}
        email = fields.get("Hva er e-postadressen din?")
        theme = fields.get("Hva handler innlegget om?")
        platform = fields.get("Hvilken plattform gjelder innlegget?")
    except Exception as e:
        print("❌ Missing or malformed fields:", e)
        return "Malformed form data", 400

    if not email or not theme or not platform:
        return "Missing fields", 400

    # Check if email is already used
    if os.path.exists("used_emails.txt"):
        with open("used_emails.txt", "r") as f:
            used_emails = f.read().splitlines()
    else:
        used_emails = []

    if email in used_emails:
        print(f"⚠️ {email} har allerede brukt sin gratis caption.")
        return "⚠️ Du har allerede brukt din gratis caption!", 403

    # Generate captions
    prompt = generate_prompt(theme, platform)
    try:
        captions = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        ).choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT request failed:", e)
        return "OpenAI error", 500

    # Mark email as used
    with open("used_emails.txt", "a") as f:
        f.write(email + "\n")

    # Format captions and email
    html_output = format_captions(captions)
    subject = f"Dine AI-genererte captions for {platform}"
    html_email = f"""<div style="font-family:Arial;padding:20px;">
    <h2>Hei!</h2>
    <p>Her er dine AI-genererte captions for <b>{platform}</b>:</p>
    {html_output}
    <p>Hilsen,<br>InstaPrompt 🚀</p>
    </div>"""

    # Send email
    try:
        send_email(to=email, subject=subject, html=html_email)
        print(f"📧 Email sendt til {email}")
    except Exception as e:
        print("❌ Email sending failed:", e)
        return "Email error",

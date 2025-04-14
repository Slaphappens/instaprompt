from flask import Flask, request, render_template_string
from utils import generate_prompt, format_captions, send_email
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

USED_EMAILS_FILE = "used_emails.txt"

def is_used(email):
    if not os.path.exists(USED_EMAILS_FILE):
        return False
    with open(USED_EMAILS_FILE, "r") as f:
        return email.strip() in f.read().splitlines()

def mark_used(email):
    with open(USED_EMAILS_FILE, "a") as f:
        f.write(email.strip() + "\n")

@app.route("/", methods=["GET"])
def health_check():
    return "InstaPrompt is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    fields = {f['label']: f['value'] for f in data.get("fields", [])}

    email = fields.get("Hva er e-postadressen din?")
    tema = fields.get("Hva handler innlegget om?")
    plattform = fields.get("Hvilken plattform gjelder innlegget?")

    if is_used(email):
        return render_template_string("<h3>⚠️ Du har allerede brukt din gratis caption!</h3><p>Besøk oss igjen med InstaPrompt Pro 🚀</p>")

    prompt = generate_prompt(plattform, tema)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    captions_raw = response.choices[0].message.content.strip()
    captions_html = format_captions(captions_raw)

    html_email = f"""<div style="font-family:Arial;padding:20px;">
      <h2>Hei! 👋</h2>
      <p>Her er dine captions for <strong>{plattform}</strong> om <strong>{tema}</strong>:</p>
      <div style="background:#eee;padding:10px;margin:10px 0;">{captions_html}</div>
    </div>"""

    send_email(email, f"Dine InstaPrompt captions for {plattform}", html_email)
    mark_used(email)

    return render_template_string(html_email)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template_string
from utils import generate_prompt, format_captions, send_email
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    prompt = generate_prompt(plattform, tema)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    captions_raw = response.choices[0].message.content.strip()
    captions_html = format_captions(captions_raw)

    html_email = f"""<div style="font-family:Arial,sans-serif;padding:20px;border:1px solid #ccc;border-radius:8px;">
      <h2>Hei! 👋</h2>
      <p>Takk for at du brukte InstaPrompt!</p>
      <p>Her er dine captions for <strong>{plattform}</strong> basert på <strong>{tema}</strong>:</p>
      <div style="background:#f9f9f9;padding:15px;border-radius:6px;margin:20px 0;line-height:1.6;font-size:15px;">
        {captions_html}
      </div>
      <p>Trenger du flere forslag? Besøk <a href="https://instaprompt.no">instaprompt.no</a></p>
      <p>Hilsen,<br>InstaPrompt-teamet ✨</p>
    </div>"""

    send_email(email, f"Dine InstaPrompt captions for {plattform}", html_email)

    return render_template_string(html_email)

if __name__ == "__main__":
    app.run(debug=True)
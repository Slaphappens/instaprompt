from prompt_engine import generate_prompt, format_captions
from emailer import send_email
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_request(email, tema, plattform):
    prompt = generate_prompt(plattform, tema)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    captions = response.choices[0].message.content.strip()
    captions_html = format_captions(captions)

    html_body = f"""
    <div style='font-family:Arial;padding:20px;border:1px solid #ccc;border-radius:8px;'>
        <h2>Hei! 👋</h2>
        <p>Her er dine captions for <strong>{plattform}</strong> basert på <strong>{tema}</strong>:</p>
        <div style='background:#f9f9f9;padding:15px;margin:20px 0;'>{captions_html}</div>
        <p>Hilsen,<br>InstaPrompt ✨</p>
    </div>
    """
    send_email(email, f"Dine InstaPrompt captions for {plattform}", html_body)
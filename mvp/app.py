from flask import Flask, request
from utils import generate_caption, send_email

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("✅ Webhook called")

    try:
        data = request.get_json(force=True)
        print("📦 JSON payload:", data)
    except Exception as e:
        print("❌ JSON parsing error:", e)
        return "Invalid JSON", 400

    if not data or "fields" not in data:
        print("❌ 'fields' missing in payload")
        return "Missing fields", 400

    try:
        fields = {f["label"]: f["value"] for f in data["fields"]}
        email = fields.get("Hva er e-postadressen din?")
        theme = fields.get("Hva handler innlegget om?")
        platform = fields.get("Hvilken plattform gjelder innlegget?")

        print(f"📬 Email: {email}, 🧠 Theme: {theme}, 📱 Platform: {platform}")
        if not all([email, theme, platform]):
            raise ValueError("Missing one or more fields")

        caption = generate_caption(theme, platform)
        print("📝 Generated caption:", caption)

        send_email(email, caption)
        return "OK", 200

    except Exception as e:
        print("❌ Unexpected error:", e)
        return "Internal error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

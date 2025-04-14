def generate_prompt(plattform, tema):
    return f"""
Lag 3 engasjerende captions for sosiale medier basert på:

Plattform: {plattform}
Tema: {tema}

Regler:
- Maks 3 linjer per caption
- Bruk emojis og relevante hashtags
- Svar kun med selve captionene, nummerert
"""

def format_captions(text):
    return text.replace("\n", "<br>")
import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

app = Flask(__name__)

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


@app.route("/")
def index():
    """Landing page with redirect to news"""
    return render_template("index.html")


@app.route("/api/news")
def api_news():
    """Fetch Azure AI Foundry news via Gemini Search"""
    model = genai.GenerativeModel("gemini-2.5-pro")

    # Use search/generation prompt for structured news
    prompt = """
    Perform a web search for the latest Azure AI Foundry news.
    Return 5 professional news items with:
    - Headline (max 10 words)
    - Summary (2–3 sentences)
    Format each as:
    Headline: ...
    Summary: ...
    ---
    """

    response = model.generate_content(prompt)
    news_text = response.text or "No news available."

    # Split into structured articles
    articles = []
    for block in news_text.split("---"):
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if len(lines) >= 2:
            headline = lines[0].replace("Headline:", "").strip()
            summary = lines[1].replace("Summary:", "").strip()
            articles.append({"headline": headline, "summary": summary})

    return jsonify({"articles": articles})


@app.route("/news")
def news():
    """News page (AJAX)"""
    return render_template("news.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

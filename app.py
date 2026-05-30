from flask import Flask, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.route("/")
def home():
    return {
        "status": "online",
        "api_key_loaded": API_KEY is not None
    }

@app.route("/search")
def search():

    query = request.args.get("q")

    if not query:
        return {
            "error": "Missing query"
        }

    if not API_KEY:
        return {
            "error": "YOUTUBE_API_KEY not found"
        }

    url = (
        "https://www.googleapis.com/youtube/v3/search"
        "?part=snippet"
        "&type=video"
        "&maxResults=5"
        f"&q={query}"
        f"&key={API_KEY}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        return {
            "api_key_loaded": True,
            "youtube_response": data
        }

    except Exception as e:

        return {
            "error": str(e)
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

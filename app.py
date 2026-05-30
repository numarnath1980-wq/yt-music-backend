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
        return {"error": "Missing query"}

    url = (
        "https://www.googleapis.com/youtube/v3/search"
        "?part=snippet"
        "&type=video"
        "&maxResults=5"
        f"&q={query}"
        f"&key={API_KEY}"
    )

    response = requests.get(url).json()

    results = []

    for item in response.get("items", []):

        results.append({
            "title": item["snippet"]["title"],
            "artist": item["snippet"]["channelTitle"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        })

    return {"results": results}

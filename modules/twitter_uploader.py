import os
import time
import requests
from requests_oauthlib import OAuth1
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET


class TwitterUploader:
    def __init__(self):
        self.api_key = X_API_KEY
        self.api_secret = X_API_SECRET
        self.access_token = X_ACCESS_TOKEN
        self.access_token_secret = X_ACCESS_TOKEN_SECRET

    def _get_auth(self):
        if self.api_key and self.api_secret and self.access_token and self.access_token_secret:
            return OAuth1(self.api_key, self.api_secret, self.access_token, self.access_token_secret)
        return None

    def upload_video_tweet(self, video_path: Path, text: str) -> dict:
        auth = self._get_auth()
        if not auth:
            return {"status": "skipped", "message": "X (Twitter) API keys not configured in .env"}

        try:
            # 1. Upload Video Chunked to Twitter Media Upload
            upload_url = "https://upload.twitter.com/1.1/media/upload.json"
            total_bytes = os.path.getsize(video_path)

            # INIT
            init_res = requests.post(upload_url, auth=auth, data={
                "command": "INIT",
                "total_bytes": total_bytes,
                "media_type": "video/mp4",
                "media_category": "tweet_video"
            })
            media_id = init_res.json().get("media_id_string")
            if not media_id:
                return {"status": "error", "message": f"INIT failed: {init_res.text}"}

            # APPEND
            segment_id = 0
            with open(video_path, "rb") as f:
                while True:
                    chunk = f.read(4 * 1024 * 1024) # 4MB
                    if not chunk:
                        break
                    requests.post(upload_url, auth=auth, data={
                        "command": "APPEND",
                        "media_id": media_id,
                        "segment_index": segment_id
                    }, files={"media": chunk})
                    segment_id += 1

            # FINALIZE
            requests.post(upload_url, auth=auth, data={"command": "FINALIZE", "media_id": media_id})
            time.sleep(3) # Processing buffer

            # 2. Post Tweet via X API v2
            tweet_url = "https://api.twitter.com/2/tweets"
            payload = {
                "text": text,
                "media": {"media_ids": [media_id]}
            }
            res = requests.post(tweet_url, auth=auth, json=payload)
            data = res.json()
            if "data" in data and "id" in data["data"]:
                return {"status": "success", "tweet_id": data["data"]["id"], "url": f"https://x.com/i/status/{data['data']['id']}"}
            return {"status": "error", "message": str(data)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

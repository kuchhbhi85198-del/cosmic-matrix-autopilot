import requests
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID


class FacebookUploader:
    def __init__(self):
        self.access_token = FACEBOOK_ACCESS_TOKEN
        self.page_id = FACEBOOK_PAGE_ID

    def upload_video(self, video_path: Path, caption: str) -> dict:
        if not self.access_token or not self.page_id:
            return {"status": "skipped", "message": "Facebook API credentials not configured in .env"}

        url = f"https://graph-video.facebook.com/v19.0/{self.page_id}/videos"
        payload = {
            "description": caption,
            "access_token": self.access_token
        }

        try:
            with open(video_path, "rb") as video_file:
                files = {"source": video_file}
                res = requests.post(url, data=payload, files=files, timeout=120)
                data = res.json()
                if "id" in data:
                    return {"status": "success", "video_id": data["id"]}
                return {"status": "error", "message": str(data)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

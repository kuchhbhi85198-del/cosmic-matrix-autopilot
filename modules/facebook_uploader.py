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

        # Priority 1: Meta Official Facebook Reels API
        try:
            from modules.meta_instagram_publisher import meta_ig_publisher
            if meta_ig_publisher.is_configured:
                print("📘 [FACEBOOK REELS API] Publishing Native Reel to Facebook Page...")
                res = meta_ig_publisher.publish_facebook_reel(video_path, caption)
                if res.get("status") == "success":
                    return res
                print(f"[!] Facebook Reels API returned non-success: {res}. Falling back to graph-video...")
        except Exception as e:
            print(f"[!] Facebook Reels API error: {e}. Falling back to graph-video...")

        # Fallback 2: Graph-Video legacy endpoint
        url = f"https://graph-video.facebook.com/v21.0/{self.page_id}/videos"
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

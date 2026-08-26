import requests
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN


class LinkedInUploader:
    def __init__(self):
        self.access_token = LINKEDIN_ACCESS_TOKEN
        self.person_urn = LINKEDIN_PERSON_URN

    def post_text(self, text: str) -> dict:
        if not self.access_token or not self.person_urn:
            return {"status": "skipped", "message": "LinkedIn access token / URN not configured in .env"}

        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        payload = {
            "author": f"urn:li:person:{self.person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        try:
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 201:
                return {"status": "success", "post_id": res.json().get("id")}
            return {"status": "error", "message": res.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def upload_video_post(self, video_path: Path, text: str) -> dict:
        if not self.access_token or not self.person_urn:
            return {"status": "skipped", "message": "LinkedIn access token / URN not configured in .env"}

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        try:
            # 1. Register Upload
            reg_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
            reg_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
                    "owner": f"urn:li:person:{self.person_urn}",
                    "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
                }
            }
            reg_res = requests.post(reg_url, headers=headers, json=reg_payload)
            reg_data = reg_res.json()
            upload_url = reg_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
            asset_urn = reg_data["value"]["asset"]

            # 2. Upload Video Binary
            with open(video_path, "rb") as f:
                requests.put(upload_url, headers={"Authorization": f"Bearer {self.access_token}"}, data=f)

            # 3. Create UGC Post
            post_url = "https://api.linkedin.com/v2/ugcPosts"
            post_payload = {
                "author": f"urn:li:person:{self.person_urn}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "VIDEO",
                        "media": [{
                            "status": "READY",
                            "media": asset_urn
                        }]
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            post_res = requests.post(post_url, headers=headers, json=post_payload)
            if post_res.status_code == 201:
                return {"status": "success", "post_id": post_res.json().get("id")}
            
            # Fallback to Text Post
            return self.post_text(text)
        except Exception:
            return self.post_text(text)


if __name__ == "__main__":
    uploader = LinkedInUploader()
    res = uploader.post_text("🌌 Cosmic Matrix Autopilot System connected to LinkedIn! ⚡")
    print("LinkedIn Post Result:", res)

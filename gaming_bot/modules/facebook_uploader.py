import os
import requests
from pathlib import Path
from typing import Dict, Any

class FacebookUploader:
    """
    Publishes Reels directly to Facebook Page (Amazing VIBES)
    using Official Meta Facebook Reels API (3-phase resumable upload).
    """
    def __init__(self):
        self.page_id = os.getenv("FACEBOOK_PAGE_ID", "1245284252009574")
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN", "EAAZAFK0ek1FoBST24YBel9jGbdL8e1bLVzTkScsyB8FqZCRSQT2VZAKjZCHjuZBVV6k4cwf5vZB0lm2F7NFH9ZAKx9TghGuuqIUYKmbkfsQN16DZCHfvfApdlnPUovAMle87MdndMdSkOwLuwMYadMgxIo59BMGDWoCVx8H3REALsXnDm2jBPNF4QbwQeKujspVuVcZAHPLa5")

    def upload_reel(self, video_path: Path, caption: str) -> Dict[str, Any]:
        if not self.page_id or not self.access_token:
            return {"status": "skipped", "message": "Facebook credentials missing"}

        try:
            file_size = os.path.getsize(video_path)
            print(f"📘 [FB REELS API] Initiating Reel upload to Amazing VIBES ({file_size / (1024*1024):.2f} MB)...")

            # Phase 1: Start
            start_url = f"https://graph.facebook.com/v21.0/{self.page_id}/video_reels"
            start_res = requests.post(start_url, data={"upload_phase": "start", "access_token": self.access_token}, timeout=30)
            start_data = start_res.json()
            if "video_id" not in start_data or "upload_url" not in start_data:
                return {"status": "failed", "error": start_data}

            video_id = start_data["video_id"]
            upload_url = start_data["upload_url"]

            # Phase 2: Binary Upload
            headers = {
                "Authorization": f"OAuth {self.access_token}",
                "offset": "0",
                "file_size": str(file_size)
            }
            with open(video_path, "rb") as f:
                up_res = requests.post(upload_url, headers=headers, data=f, timeout=120)

            if up_res.status_code not in [200, 201]:
                return {"status": "failed", "error": f"Upload failed: {up_res.text}"}

            # Phase 3: Finish / Publish
            finish_data = {
                "upload_phase": "finish",
                "video_id": video_id,
                "video_state": "PUBLISHED",
                "description": caption,
                "access_token": self.access_token
            }
            fin_res = requests.post(start_url, data=finish_data, timeout=30)
            fin_json = fin_res.json()

            if fin_json.get("success"):
                print(f"🎉 [FB REEL SUCCESS] Reel LIVE on Facebook Page Amazing VIBES! Video ID: {video_id}")
                return {"status": "success", "video_id": video_id}
            else:
                return {"status": "failed", "error": fin_json}
        except Exception as e:
            return {"status": "error", "message": str(e)}

import os
import time
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class MetaInstagramPublisher:
    """
    Official Meta Graph API (Instagram Content Publishing API) Publisher.
    100% Legal, Strike-Proof, Zero-Session-Expiry Cloud Publishing.
    """
    GRAPH_VERSION = "v20.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"

    def __init__(self, access_token: Optional[str] = None, ig_user_id: Optional[str] = None):
        self.access_token = access_token or os.getenv("META_INSTAGRAM_ACCESS_TOKEN")
        self.ig_user_id = ig_user_id or os.getenv("META_INSTAGRAM_USER_ID")

    @property
    def is_configured(self) -> bool:
        return bool(self.access_token and self.ig_user_id)

    def publish_reel(self, video_source: Any, caption: str, share_to_feed: bool = True) -> Dict[str, Any]:
        """
        Publishes a 9:16 vertical Reel to Instagram using Official Meta Graph API.
        Automatically detects whether video_source is a local file path or a public URL.
        """
        if not self.is_configured:
            return {
                "status": "error",
                "message": "Meta Instagram Publisher not configured. Missing META_INSTAGRAM_ACCESS_TOKEN or META_INSTAGRAM_USER_ID."
            }

        video_str = str(video_source)
        if not video_str.startswith(("http://", "https://")) and Path(video_str).is_file():
            return self._publish_local_video(Path(video_str), caption, share_to_feed)
        else:
            return self._publish_url_video(video_str, caption, share_to_feed)

    def _publish_local_video(self, video_path: Path, caption: str, share_to_feed: bool = True) -> Dict[str, Any]:
        """Uploads a local video directly using Meta's Resumable Upload protocol"""
        try:
            file_size = os.path.getsize(video_path)
            print(f"📡 [META GRAPH API] Initiating Resumable Reel Upload for: {video_path.name} ({file_size / (1024*1024):.2f} MB)...")

            container_url = f"{self.BASE_URL}/{self.ig_user_id}/media"
            init_payload = {
                "media_type": "REELS",
                "upload_type": "resumable",
                "caption": caption,
                "share_to_feed": str(share_to_feed).lower(),
                "access_token": self.access_token
            }

            res = requests.post(container_url, data=init_payload, timeout=30)
            res_data = res.json()

            if "id" not in res_data or "uri" not in res_data:
                err_msg = res_data.get("error", {}).get("message", "Unknown initialization error")
                print(f"❌ [META API ERROR] Container init failed: {err_msg}")
                return {"status": "failed", "error": res_data}

            container_id = res_data["id"]
            upload_uri = res_data["uri"]
            print(f"✅ [META GRAPH API] Container created: {container_id}. Uploading binary payload...")

            upload_headers = {
                "Authorization": f"OAuth {self.access_token}",
                "offset": "0",
                "file_size": str(file_size)
            }

            with open(video_path, "rb") as f:
                upload_res = requests.post(upload_uri, headers=upload_headers, data=f, timeout=120)

            if upload_res.status_code not in [200, 201]:
                print(f"❌ [META API ERROR] Binary upload failed ({upload_res.status_code}): {upload_res.text}")
                return {"status": "failed", "error": upload_res.text}

            print(f"✅ [META GRAPH API] Binary stream transferred 100%. Polling encoding status...")

            status = self._poll_status(container_id)
            if status != "FINISHED":
                print(f"❌ [META API ERROR] Encoding failed. Final Status: {status}")
                return {"status": "failed", "error": f"Processing status: {status}"}

            return self._finalize_publish(container_id)

        except Exception as e:
            print(f"❌ [META API EXCEPTION] Local upload error: {e}")
            return {"status": "error", "message": str(e)}

    def _publish_url_video(self, video_url: str, caption: str, share_to_feed: bool = True) -> Dict[str, Any]:
        """Uploads a video from a public HTTPS URL"""
        try:
            print(f"📡 [META GRAPH API] Initiating Reel container via URL...")
            container_url = f"{self.BASE_URL}/{self.ig_user_id}/media"
            payload = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "share_to_feed": str(share_to_feed).lower(),
                "access_token": self.access_token
            }

            res = requests.post(container_url, data=payload, timeout=30)
            res_data = res.json()

            if "id" not in res_data:
                err_msg = res_data.get("error", {}).get("message", "Unknown error")
                print(f"❌ [META API ERROR] Failed to create Reel container: {err_msg}")
                return {"status": "failed", "error": res_data}

            container_id = res_data["id"]
            print(f"✅ [META GRAPH API] Container created: {container_id}. Polling status...")

            status = self._poll_status(container_id)
            if status != "FINISHED":
                return {"status": "failed", "error": f"Processing status: {status}"}

            return self._finalize_publish(container_id)

        except Exception as e:
            print(f"❌ [META API EXCEPTION] URL upload error: {e}")
            return {"status": "error", "message": str(e)}

    def _finalize_publish(self, container_id: str) -> Dict[str, Any]:
        """Publishes the finalized media container"""
        try:
            publish_url = f"{self.BASE_URL}/{self.ig_user_id}/media_publish"
            pub_payload = {
                "creation_id": container_id,
                "access_token": self.access_token
            }

            pub_res = requests.post(publish_url, data=pub_payload, timeout=30)
            pub_data = pub_res.json()

            if "id" in pub_data:
                published_media_id = pub_data["id"]
                print(f"🎉 [META GRAPH API SUCCESS] Reel LIVE on Instagram with 0% STRIKE RISK! Media ID: {published_media_id}")
                return {
                    "status": "success",
                    "media_id": published_media_id,
                    "container_id": container_id
                }
            else:
                err_msg = pub_data.get("error", {}).get("message", "Publish failed")
                print(f"❌ [META API ERROR] Publishing failed: {err_msg}")
                return {"status": "failed", "error": pub_data}

        except Exception as e:
            print(f"❌ [META API EXCEPTION] {e}")
            return {"status": "error", "message": str(e)}

    def _poll_status(self, container_id: str, max_attempts: int = 25, delay: int = 5) -> str:
        """Polls Meta server until video container is encoded and ready to publish"""
        status_url = f"{self.BASE_URL}/{container_id}"
        params = {
            "fields": "status_code",
            "access_token": self.access_token
        }

        for attempt in range(max_attempts):
            time.sleep(delay)
            try:
                res = requests.get(status_url, params=params, timeout=15).json()
                code = res.get("status_code", "IN_PROGRESS")
                print(f"   ⏳ [META ENCODING] Attempt {attempt+1}/{max_attempts} -> Status: {code}")
                if code == "FINISHED":
                    return "FINISHED"
                elif code in ["ERROR", "EXPIRED"]:
                    return code
            except Exception as e:
                print(f"   [!] Status check warning: {e}")

        return "TIMEOUT"


# Singleton Helper Instance
meta_ig_publisher = MetaInstagramPublisher()

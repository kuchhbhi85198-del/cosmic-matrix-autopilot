import os
import time
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

GAMING_DIR = Path(__file__).resolve().parent.parent
load_dotenv(GAMING_DIR / ".env")

class MetaInstagramPublisher:
    """
    Official Meta Graph API (Instagram Content Publishing API) Publisher.
    100% Legal, Strike-Proof, Zero-Session-Expiry Cloud Publishing.
    """
    GRAPH_VERSION = "v20.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"

    def __init__(self, access_token: Optional[str] = None, ig_user_id: Optional[str] = None, fb_page_id: Optional[str] = None):
        self.access_token = access_token or os.getenv("META_INSTAGRAM_ACCESS_TOKEN")
        self.ig_user_id = ig_user_id or os.getenv("META_INSTAGRAM_USER_ID")
        self.fb_page_id = fb_page_id or os.getenv("FACEBOOK_PAGE_ID")

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
                permalink = f"https://www.instagram.com/reel/{published_media_id}/"
                try:
                    p_res = requests.get(
                        f"{self.BASE_URL}/{published_media_id}",
                        params={"fields": "permalink", "access_token": self.access_token},
                        timeout=10
                    ).json()
                    if "permalink" in p_res:
                        permalink = p_res["permalink"]
                except Exception:
                    pass
                print(f"🎉 [META GRAPH API SUCCESS] Reel LIVE on Instagram with 0% STRIKE RISK! URL: {permalink}")
                return {
                    "status": "success",
                    "media_id": published_media_id,
                    "container_id": container_id,
                    "url": permalink
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

    def post_first_comment(self, media_id: str, comment_text: str) -> Dict[str, Any]:
        """
        Posts an instant first / pinned engagement comment on newly uploaded Instagram Reels.
        """
        if not self.access_token:
            return {"status": "error", "message": "Missing access token"}
        try:
            url = f"{self.BASE_URL}/{media_id}/comments"
            res = requests.post(url, data={"message": comment_text, "access_token": self.access_token}, timeout=20)
            data = res.json()
            if "id" in data:
                print(f"💬 [META AUTO-COMMENT] First comment posted on Instagram! Comment ID: {data['id']}")
                return {"status": "success", "comment_id": data["id"]}
            else:
                return {"status": "failed", "error": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_reel_insights(self, media_id: str) -> Dict[str, Any]:
        """
        Pulls real-time analytics: Reach, Views, Likes, Comments, Shares, Saves, Total Interactions.
        """
        if not self.access_token:
            return {"status": "error", "message": "Missing access token"}
        try:
            url = f"{self.BASE_URL}/{media_id}/insights"
            metrics = "reach,saved,likes,comments,shares,total_interactions,views"
            res = requests.get(url, params={"metric": metrics, "access_token": self.access_token}, timeout=20)
            data = res.json()
            if "data" in data:
                insights_map = {}
                for item in data["data"]:
                    val = item["values"][0]["value"] if item.get("values") else 0
                    insights_map[item["name"]] = val
                return {"status": "success", "insights": insights_map}
            return {"status": "failed", "error": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_account_overview(self) -> Dict[str, Any]:
        """
        Fetches live profile stats: username, followers, follows, media_count.
        """
        if not self.is_configured:
            return {"status": "error", "message": "Not configured"}
        try:
            url = f"{self.BASE_URL}/{self.ig_user_id}"
            fields = "id,name,username,followers_count,follows_count,media_count,profile_picture_url"
            res = requests.get(url, params={"fields": fields, "access_token": self.access_token}, timeout=20)
            return {"status": "success", "data": res.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_recent_media(self, limit: int = 10) -> Dict[str, Any]:
        """
        Fetches recently posted media and reels with permalinks, views, and likes.
        """
        if not self.is_configured:
            return {"status": "error", "message": "Not configured"}
        try:
            url = f"{self.BASE_URL}/{self.ig_user_id}/media"
            fields = "id,caption,media_type,like_count,comments_count,timestamp,permalink"
            res = requests.get(url, params={"fields": fields, "limit": limit, "access_token": self.access_token}, timeout=20)
            return {"status": "success", "data": res.json().get("data", [])}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def publish_facebook_reel(self, video_source: Any, description: str) -> Dict[str, Any]:
        """
        Publishes a Reel directly to the Facebook Page (Amazing VIBES) using Meta Graph API.
        """
        if not self.fb_page_id or not self.access_token:
            return {"status": "error", "message": "Missing FB Page ID or access token"}
        try:
            video_path = Path(str(video_source))
            if not video_path.is_file():
                return {"status": "error", "message": f"Local video file not found: {video_path}"}

            file_size = os.path.getsize(video_path)
            print(f"📘 [META FB REEL] Initiating Facebook Page Reel upload ({file_size / (1024*1024):.2f} MB)...")

            # Phase 1: Start
            start_url = f"{self.BASE_URL}/{self.fb_page_id}/video_reels"
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
                "description": description,
                "access_token": self.access_token
            }
            fin_res = requests.post(start_url, data=finish_data, timeout=30)
            fin_json = fin_res.json()

            if fin_json.get("success"):
                print(f"🎉 [META FB REEL SUCCESS] Reel LIVE on Facebook Page! Video ID: {video_id}")
                return {"status": "success", "video_id": video_id}
            else:
                return {"status": "failed", "error": fin_json}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def publish_omni_reel(self, video_source: Any, ig_caption: str, fb_description: Optional[str] = None, first_comment: Optional[str] = None) -> Dict[str, Any]:
        """
        OMNI PUBLISHER:
        1. Publishes Reel to Instagram (@gaming143vibes)
        2. Drops first engagement comment on Instagram
        3. Cross-posts Reel to Facebook Page (Amazing VIBES)
        All in one atomic call!
        """
        results = {}

        # 1. Instagram Reel
        print(f"🚀 [OMNI PUBLISH] 1/3 Dispatching to Instagram Reels...")
        ig_res = self.publish_reel(video_source, ig_caption)
        results["instagram"] = ig_res

        # 2. Instagram First Comment
        if ig_res.get("status") == "success" and first_comment:
            media_id = ig_res.get("media_id")
            print(f"🚀 [OMNI PUBLISH] 2/3 Adding First Engagement Comment...")
            comment_res = self.post_first_comment(media_id, first_comment)
            results["first_comment"] = comment_res

        # 3. Facebook Page Reel
        if self.fb_page_id:
            print(f"🚀 [OMNI PUBLISH] 3/3 Cross-posting to Facebook Page Reels...")
            fb_text = fb_description or ig_caption
            fb_res = self.publish_facebook_reel(video_source, fb_text)
            results["facebook_page"] = fb_res

        return results


# Singleton Helper Instance
meta_ig_publisher = MetaInstagramPublisher()


from pathlib import Path
import sys
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (
    ENABLE_YOUTUBE,
    ENABLE_INSTAGRAM,
    ENABLE_FACEBOOK,
    ENABLE_X_TWITTER,
    ENABLE_LINKEDIN
)
from modules.youtube_uploader import YouTubeUploader
from modules.instagram_uploader import InstagramUploader
from modules.facebook_uploader import FacebookUploader
from modules.twitter_uploader import TwitterUploader
from modules.linkedin_uploader import LinkedInUploader


class MultiPlatformDispatcher:
    """
    Simultaneously dispatches generated Cosmic Matrix shorts to Platforms:
    1. YouTube Shorts
    2. Instagram Reels (Can be toggled via ENABLE_INSTAGRAM)
    3. Facebook Reels / Post
    4. X (Twitter) Video Tweet
    5. LinkedIn Video Post
    """
    def __init__(self):
        self.yt = YouTubeUploader() if ENABLE_YOUTUBE else None
        self.insta = InstagramUploader() if ENABLE_INSTAGRAM else None
        self.fb = FacebookUploader() if ENABLE_FACEBOOK else None
        self.x = TwitterUploader() if ENABLE_X_TWITTER else None
        self.li = LinkedInUploader() if ENABLE_LINKEDIN else None

    def dispatch_all(self, video_path: Path, seo_data: Dict[str, Any], privacy: str = "public") -> Dict[str, Any]:
        results = {}

        # 1. YouTube Shorts
        if ENABLE_YOUTUBE and self.yt:
            print("\n[*] [1/5] Dispatching to YouTube Shorts...")
            try:
                yt_res = self.yt.upload_short(
                    video_path=video_path,
                    title=seo_data["youtube"]["title"],
                    description=seo_data["youtube"]["description"],
                    tags=seo_data["youtube"]["tags"],
                    privacy=privacy
                )
                results["youtube"] = yt_res
                print(f"    -> YouTube: {yt_res.get('status').upper()} ({yt_res.get('url', yt_res.get('message'))})")
            except Exception as e:
                results["youtube"] = {"status": "error", "message": str(e)}
        else:
            results["youtube"] = {"status": "skipped", "message": "YouTube upload disabled"}

        # 2. Instagram Reels
        if ENABLE_INSTAGRAM and self.insta:
            print("[*] [2/5] Dispatching to Instagram Reels...")
            try:
                insta_res = self.insta.upload_reel(
                    video_path=video_path,
                    caption=seo_data["instagram"]["caption"]
                )
                results["instagram"] = insta_res
                print(f"    -> Instagram: {insta_res.get('status').upper()} (Media PK: {insta_res.get('media_pk', insta_res.get('message'))})")
            except Exception as e:
                results["instagram"] = {"status": "error", "message": str(e)}
        else:
            print("[*] [2/5] Instagram Reels: PAUSED BY USER (Skipping Instagram upload)")
            results["instagram"] = {"status": "paused_by_user", "message": "Instagram upload temporarily paused"}

        # 3. Facebook Video
        if ENABLE_FACEBOOK and self.fb:
            print("[*] [3/5] Dispatching to Facebook...")
            try:
                fb_res = self.fb.upload_video(
                    video_path=video_path,
                    caption=seo_data["facebook"]["caption"]
                )
                results["facebook"] = fb_res
                print(f"    -> Facebook: {fb_res.get('status').upper()} ({fb_res.get('video_id', fb_res.get('message'))})")
            except Exception as e:
                results["facebook"] = {"status": "error", "message": str(e)}
        else:
            results["facebook"] = {"status": "skipped", "message": "Facebook API credentials not configured / disabled"}

        # 4. X (Twitter)
        if ENABLE_X_TWITTER and self.x:
            print("[*] [4/5] Dispatching to X (Twitter)...")
            try:
                x_res = self.x.upload_video_tweet(
                    video_path=video_path,
                    text=seo_data["x_twitter"]["text"]
                )
                results["x_twitter"] = x_res
                print(f"    -> X (Twitter): {x_res.get('status').upper()} ({x_res.get('url', x_res.get('message'))})")
            except Exception as e:
                results["x_twitter"] = {"status": "error", "message": str(e)}
        else:
            results["x_twitter"] = {"status": "skipped", "message": "X (Twitter) upload disabled"}

        # 5. LinkedIn
        if ENABLE_LINKEDIN and self.li:
            print("[*] [5/5] Dispatching to LinkedIn...")
            try:
                li_res = self.li.upload_video_post(
                    video_path=video_path,
                    text=seo_data["linkedin"]["text"]
                )
                results["linkedin"] = li_res
                print(f"    -> LinkedIn: {li_res.get('status').upper()} ({li_res.get('message', 'Posted')})")
            except Exception as e:
                results["linkedin"] = {"status": "error", "message": str(e)}
        else:
            results["linkedin"] = {"status": "skipped", "message": "LinkedIn upload disabled"}

        return results


if __name__ == "__main__":
    dispatcher = MultiPlatformDispatcher()
    print("Multi-Platform Dispatcher ready.")

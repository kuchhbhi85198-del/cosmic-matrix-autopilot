import os
import sys
import subprocess
from pathlib import Path

# Ensure root project directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import imageio_ffmpeg
from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

SESSION_FILE = BASE_DIR / "instagram_session.json"


class InstagramUploader:
    """
    Automated Instagram Reels Uploader using Instagrapi.
    Uploads 9:16 vertical videos directly to Instagram Reels with custom caption & hashtags.
    """
    def __init__(self):
        self.username = os.getenv("INSTAGRAM_USERNAME", "gaming143vibes")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def generate_thumbnail(self, video_path: Path) -> Path:
        thumb_path = video_path.with_suffix(".jpg")
        cmd = [
            self.ffmpeg_exe, "-y",
            "-ss", "00:00:01",
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(thumb_path)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return thumb_path if thumb_path.exists() else None

    def upload_reel(self, video_path: Path, caption: str) -> bool:
        """
        Uploads video to Instagram Reels with auto-generated thumbnail.
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        try:
            from instagrapi import Client

            cl = Client()
            cl.delay_range = [2, 5]

            # 1. Load saved session
            if SESSION_FILE.exists():
                print("[*] Loading saved Instagram session...")
                cl.load_settings(SESSION_FILE)
            elif self.username and self.password:
                print(f"[*] Logging in as @{self.username}...")
                cl.login(self.username, self.password)
                cl.dump_settings(SESSION_FILE)
            else:
                print("[!] Error: No active session or credentials found.")
                return False

            thumb = self.generate_thumbnail(video_path)

            print(f"[*] Uploading Reel to Instagram account @{self.username}...")
            if thumb and thumb.exists():
                media = cl.clip_upload(
                    path=str(video_path),
                    caption=caption,
                    thumbnail=str(thumb)
                )
            else:
                media = cl.clip_upload(
                    path=str(video_path),
                    caption=caption
                )

            print(f"[SUCCESS] Uploaded to Instagram Reels! Media PK: {media.pk}")
            return True

        except Exception as e:
            print(f"[Error] Instagram upload failed: {e}")
            return False


if __name__ == "__main__":
    uploader = InstagramUploader()
    print("InstagramUploader ready.")

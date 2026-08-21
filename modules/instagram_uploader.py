from pathlib import Path
import sys
from instagrapi import Client

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import INSTAGRAM_SESSION_FILE


class InstagramUploader:
    def __init__(self):
        self.cl = Client()
        self.authenticated = self._authenticate()

    def _authenticate(self) -> bool:
        if INSTAGRAM_SESSION_FILE.exists():
            try:
                self.cl.load_settings(INSTAGRAM_SESSION_FILE)
                return True
            except Exception as e:
                print(f"[!] Instagram load session notice: {e}")
        return False

    def upload_reel(self, video_path: Path, caption: str) -> dict:
        if not self.authenticated:
            return {"status": "skipped", "message": "Instagram not authenticated (instagram_session.json missing)"}

        try:
            # Generate thumbnail
            import subprocess
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            thumb_path = video_path.with_suffix(".jpg")
            subprocess.run([ffmpeg_exe, "-y", "-ss", "00:00:01", "-i", str(video_path), "-vframes", "1", str(thumb_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            media = self.cl.clip_upload(
                path=video_path,
                caption=caption,
                thumbnail=thumb_path if thumb_path.exists() else None
            )
            return {
                "status": "success",
                "media_pk": str(media.pk),
                "media_id": str(media.id)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

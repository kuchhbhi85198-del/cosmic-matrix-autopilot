import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

GAMING_DIR = Path(__file__).resolve().parent
BASE_DIR = GAMING_DIR.parent

if str(GAMING_DIR) not in sys.path:
    sys.path.insert(0, str(GAMING_DIR))

from modules.viral_reels_manager import ViralReelsManager
from modules.uploader import YouTubeUploader
from modules.instagram_uploader import InstagramUploader

LOGS_DIR = GAMING_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = LOGS_DIR / "upload_history.json"


from datetime import datetime, timezone, timedelta

def get_ist_now() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

def get_current_slot() -> str:
    current_hour = get_ist_now().hour
    if 4 <= current_hour < 12:
        return "slot_morning"
    elif 12 <= current_hour < 17:
        return "slot_afternoon"
    elif 17 <= current_hour < 19:
        return "slot_evening"
    else:
        return "slot_night"


def has_slot_posted_today() -> bool:
    if not HISTORY_FILE.exists():
        return False
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        ist_now = get_ist_now()
        today_str = ist_now.strftime("%Y-%m-%d")
        current_slot = get_current_slot()
        
        for item in history:
            ts_str = item.get("timestamp", "")
            if ts_str.startswith(today_str):
                try:
                    dt = datetime.fromisoformat(ts_str)
                    # Convert to IST if timezone naive or stored
                    hour = dt.hour
                    if 4 <= hour < 12:
                        item_slot = "slot_morning"
                    elif 12 <= hour < 17:
                        item_slot = "slot_afternoon"
                    elif 17 <= hour < 19:
                        item_slot = "slot_evening"
                    else:
                        item_slot = "slot_night"
                    
                    if item_slot == current_slot:
                        return True
                except Exception:
                    pass
    except Exception:
        pass
    return False



class GamingAutopilotEngine:
    def __init__(self, privacy_status: str = "public"):
        self.reels_mgr = ViralReelsManager()
        self.yt_uploader = YouTubeUploader()
        self.ig_uploader = InstagramUploader()
        self.privacy_status = privacy_status

    def run_cycle(self, force: bool = False, retries: int = 3) -> dict:
        slot_name = get_current_slot()
        print("\n" + "=" * 65)
        print(f"🎮 [3X DAILY GAMING/VIRAL AUTOPILOT] Slot: {slot_name.upper()} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)

        for attempt in range(retries):
            try:
                reel_data = self.reels_mgr.get_next_viral_reel()
                if not reel_data:
                    raise RuntimeError("No viral reels available.")

                raw_path = reel_data["raw_video_path"]
                video_path = reel_data["video_path"]
                print(f"[1/4] Selected Raw Reel: {raw_path.name}")
                print(f"      Web-Ready H.264 Video: {video_path.name} ({round(video_path.stat().st_size / (1024*1024), 2)} MB)")
                print(f"      Category: {reel_data['category'].upper()}")

                print(f"[2/4] Title: {reel_data['yt_title']}")
                print(f"      SEO Keywords: {', '.join(reel_data['yt_tags'][:8])}")

                print(f"[3/4] Uploading to YouTube Shorts ({self.privacy_status})...")
                yt_success = self.yt_uploader.upload_short(
                    video_path=video_path,
                    title=reel_data["yt_title"],
                    description=reel_data["description"],
                    tags=reel_data["yt_tags"],
                    privacy_status=self.privacy_status
                )

                print(f"[4/4] Uploading to Instagram Reels (@gaming143vibes)...")
                ig_success = self.ig_uploader.upload_reel(
                    video_path=video_path,
                    caption=reel_data["ig_caption"]
                )

                self.reels_mgr.mark_as_posted(raw_path.name)

                record = {
                    "timestamp": datetime.now().isoformat(),
                    "slot": slot_name,
                    "category": reel_data["category"],
                    "source_clip": str(raw_path),
                    "title": reel_data["yt_title"],
                    "description": reel_data["description"],
                    "tags": reel_data["yt_tags"],
                    "uploaded_youtube": yt_success,
                    "uploaded_instagram": ig_success
                }

                history = []
                if HISTORY_FILE.exists():
                    try:
                        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                            history = json.load(f)
                    except Exception:
                        history = []
                history.append(record)
                with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=2)

                try:
                    if video_path.exists():
                        video_path.unlink()
                except Exception:
                    pass

                print("=" * 65)
                print(f"🎉 [VIRAL AUTOPILOT CYCLE COMPLETE] YouTube & Instagram LIVE!\n👉 Raw Reel: {raw_path.name}")
                print("=" * 65 + "\n")
                return record

            except Exception as e:
                print(f"[!] Error during attempt {attempt+1}: {e}")
                time.sleep(2)
                continue

        return {"status": "failed"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="3X Daily Viral Reels Dual Autopilot")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "private", "unlisted"])
    parser.add_argument("--force", action="store_true", help="Force upload even if slot already posted today")

    args = parser.parse_args()

    if not args.force and has_slot_posted_today():
        print(f"[*] [AUTO-SLOT CHECK] Current slot ({get_current_slot()}) already posted today! Exiting cleanly.")
        sys.exit(0)

    autopilot = GamingAutopilotEngine(privacy_status=args.privacy)
    autopilot.run_cycle(force=args.force)

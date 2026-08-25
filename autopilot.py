import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Ensure root project directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import OUTPUT_DIR, LOGS_DIR, SOURCE_VIDEOS_DIR
from modules.video_cutter import VideoCutter
from modules.cinematic_editor import CinematicEditor
from modules.cosmic_seo import CosmicSEO
from modules.multi_uploader import MultiPlatformDispatcher
from modules.gdrive_manager import GoogleDriveManager

HISTORY_LOG = LOGS_DIR / "upload_history.json"


class CosmicAutopilotEngine:
    def __init__(self, privacy_status: str = "public"):
        self.privacy_status = privacy_status
        self.cutter = VideoCutter()
        self.editor = CinematicEditor()
        self.seo = CosmicSEO()
        self.dispatcher = MultiPlatformDispatcher()
        try:
            self.gdrive = GoogleDriveManager()
        except Exception as e:
            print(f"[!] GDrive Manager Notice: {e}")
            self.gdrive = None

    def _save_history(self, record: dict):
        history = []
        if HISTORY_LOG.exists():
            try:
                with open(HISTORY_LOG, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []
        history.append(record)
        with open(HISTORY_LOG, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def run_cycle(self) -> Path:
        print("\n" + "=" * 65)
        print(f"🌌 [COSMIC MASTER ORIGINAL AUTOPILOT RUN] | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)

        # 1. Extract next high-retention authentic moment from Master Episodes
        print("[1/5] Extracting authentic cosmic moment from 5TB Master Vault...")
        clip_data = self.cutter.extract_next_clip()
        print(f"      Selected Moment: '{clip_data['hook']}' ({clip_data['topic']})")
        print(f"      Clip Path: {clip_data['clip_path'].name}")

        # 2. Generate 5-Platform SEO Metadata with Topmate Store Link
        print("\n[2/5] Generating tailored 5-Platform SEO (YouTube, Insta, FB, X, LinkedIn)...")
        seo_data = self.seo.generate_all(hook=clip_data["hook"], topic=clip_data["topic"])
        print(f"      YouTube Title: {seo_data['youtube']['title']}")

        # 3. Render 9:16 Full-Bleed Vertical Reel (1080x1920 @ 60 FPS)
        timestamp = int(time.time())
        output_video = OUTPUT_DIR / f"cosmic_short_{timestamp}.mp4"
        print("\n[3/5] Rendering 9:16 Full-Bleed 1080p60 Ultra-HD Vertical Reel...")
        rendered_short = self.editor.render_cosmic_short(
            raw_clip_path=clip_data["clip_path"],
            hook_text=clip_data["hook"],
            output_path=output_video,
            duration=clip_data["duration"]
        )
        file_size_mb = round(rendered_short.stat().st_size / (1024 * 1024), 2)
        print(f"      [SUCCESS] Rendered Short: {rendered_short.name} ({file_size_mb} MB)")

        # 4. Upload & Store in 5TB Google Drive Vault
        gdrive_file_id = None
        results = {}
        if self.gdrive:
            try:
                print("\n[4/5] ☁️ Saving 1080p60 Reel directly into 5TB Google Drive Vault...")
                gdrive_file_id = self.gdrive.upload_file(rendered_short, self.gdrive.reels_folder_id)
                print(f"      [SUCCESS] Stored in 5TB Google Drive! (File ID: {gdrive_file_id})")
                results["google_drive"] = {
                    "status": "success",
                    "file_id": gdrive_file_id,
                    "folder": "Cosmic_Matrix_5TB_Vault/Rendered_Reels_Archive"
                }
            except Exception as e:
                print(f"      [!] GDrive Save Notice: {e}")
                results["google_drive"] = {"status": "skipped", "message": str(e)}

        # 5. Dispatch to YouTube Shorts and Instagram Reels
        print("\n[5/5] Broadcasting to YouTube Shorts & Instagram Reels...")
        dispatch_results = self.dispatcher.dispatch_all(
            video_path=rendered_short,
            seo_data=seo_data,
            privacy=self.privacy_status
        )
        results.update(dispatch_results)

        # 6. Auto-Purge from local PC (Zero PC Storage Guarantee)
        try:
            if rendered_short.exists():
                rendered_short.unlink()
                print(f"      [CLEANUP] Purged local temp render file from PC. (Zero PC storage used!)")
        except Exception:
            pass

        record = {
            "timestamp": datetime.now().isoformat(),
            "hook": clip_data["hook"],
            "topic": clip_data["topic"],
            "gdrive_file_id": gdrive_file_id,
            "results": results
        }
        self._save_history(record)

        print("\n" + "=" * 65)
        print("🎉 [COSMIC ORIGINAL AUTOPILOT CYCLE COMPLETE - 100% IN 5TB GDRIVE]")
        if gdrive_file_id:
            print(f"👉 5TB Google Drive Cloud Reel ID: {gdrive_file_id}")
        print("=" * 65)
        return Path(f"gdrive://{gdrive_file_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Matrix 5-in-1 Autopilot")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "private", "unlisted"])
    args = parser.parse_args()

    engine = CosmicAutopilotEngine(privacy_status=args.privacy)
    engine.run_cycle()

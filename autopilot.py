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

from config import OUTPUT_DIR, LOGS_DIR
from modules.video_cutter import VideoCutter
from modules.cinematic_editor import CinematicEditor
from modules.cosmic_seo import CosmicSEO
from modules.multi_uploader import MultiPlatformDispatcher

HISTORY_LOG = LOGS_DIR / "upload_history.json"


class CosmicAutopilotEngine:
    def __init__(self, privacy_status: str = "public"):
        self.privacy_status = privacy_status
        self.cutter = VideoCutter()
        self.editor = CinematicEditor()
        self.seo = CosmicSEO()
        self.dispatcher = MultiPlatformDispatcher()

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
        print(f"🌌 [COSMIC MATRIX 5-IN-1 AUTOPILOT RUN] | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)

        # 1. Extract next deep moment
        print("[1/4] Extracting high-retention cosmic moment from master video...")
        clip_data = self.cutter.extract_next_clip()
        print(f"      Selected Moment: '{clip_data['hook']}' ({clip_data['topic']})")
        print(f"      Clip Path: {clip_data['clip_path']}")

        # 2. Generate 5-Platform SEO Metadata
        print("\n[2/4] Generating tailored 5-Platform SEO (YouTube, Insta, FB, X, LinkedIn)...")
        seo_data = self.seo.generate_all(hook=clip_data["hook"], topic=clip_data["topic"])
        print(f"      YouTube Title: {seo_data['youtube']['title']}")
        print(f"      X Text: {seo_data['x_twitter']['text'][:60]}...")

        # 3. Render 9:16 Cinematic Short
        timestamp = int(time.time())
        output_video = OUTPUT_DIR / f"cosmic_short_{timestamp}.mp4"
        print("\n[3/4] Rendering 9:16 Cinematic 4K Short with Golden Hook & Progress Bar...")
        rendered_short = self.editor.render_cosmic_short(
            raw_clip_path=clip_data["clip_path"],
            hook_text=clip_data["hook"],
            output_path=output_video,
            duration=clip_data["duration"]
        )
        file_size_mb = round(rendered_short.stat().st_size / (1024 * 1024), 2)
        print(f"      [SUCCESS] Rendered Short: {rendered_short.name} ({file_size_mb} MB)")

        # 4. Dispatch to all 5 platforms
        print("\n[4/4] Broadcasting to YouTube, Instagram, Facebook, X (Twitter), LinkedIn...")
        results = self.dispatcher.dispatch_all(
            video_path=rendered_short,
            seo_data=seo_data,
            privacy=self.privacy_status
        )

        record = {
            "timestamp": datetime.now().isoformat(),
            "hook": clip_data["hook"],
            "topic": clip_data["topic"],
            "video_path": str(rendered_short),
            "results": results
        }
        self._save_history(record)

        print("\n" + "=" * 65)
        print("🎉 [COSMIC 5-IN-1 CYCLE COMPLETE]")
        print(f"👉 Rendered Video: {rendered_short}")
        print("=" * 65)
        return rendered_short


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Matrix 5-in-1 Autopilot")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "private", "unlisted"])
    args = parser.parse_args()

    engine = CosmicAutopilotEngine(privacy_status=args.privacy)
    engine.run_cycle()

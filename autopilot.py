import argparse
import json
import sys
import time
import subprocess
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

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

from config import OUTPUT_DIR, LOGS_DIR, ASSETS_DIR
from modules.script_engine import CosmicScriptEngine
from modules.voice_generator import ElevenLabsVoiceEngine
from modules.video_cutter import VideoCutter
from modules.cinematic_editor import CinematicEditor
from modules.cosmic_seo import CosmicSEO
from modules.multi_uploader import MultiPlatformDispatcher
from modules.gdrive_manager import GoogleDriveManager

HISTORY_LOG = LOGS_DIR / "upload_history.json"


class CosmicAutopilotEngine:
    def __init__(self, privacy_status: str = "public"):
        self.privacy_status = privacy_status
        self.script_engine = CosmicScriptEngine()
        self.voice_engine = ElevenLabsVoiceEngine()
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

    def _get_audio_duration(self, file_path: Path) -> float:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        try:
            return float(res.stdout.strip())
        except Exception:
            return 30.0

    def run_cycle(self) -> Path:
        timestamp = int(time.time())
        print("\n" + "=" * 65)
        print(f"🌌 [COSMIC MASTER AUTOPILOT RUN] | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)

        # 1. Extract Next Deep Script from 726 Original Library
        print("[1/6] 📜 Extracting high-impact script from 726 Master Library...")
        script_data = self.script_engine.get_next_pro_script()
        print(f"      Source File: {script_data['source_file']}")
        print(f"      Top Hook: {script_data['top_hook']}")
        print(f"      Topic: {script_data['topic_tag']}")
        print(f"      Narration: {script_data['narration'][:70]}...")

        # 2. Synthesize Deep Emotional ElevenLabs Voice (Multi-Key Rotating)
        print("\n[2/6] 🎙️ Synthesizing Deep Emotional Voice (ElevenLabs Multilingual V2)...")
        voice_file = ASSETS_DIR / f"voice_{timestamp}.mp3"
        self.voice_engine.generate_speech(script_data["narration"], voice_file)
        duration = self._get_audio_duration(voice_file)
        print(f"      [SUCCESS] Voice Duration: {duration:.2f}s")

        # 3. Fetch 4K Visual Scenes from Master Vault
        print("\n[3/6] 🎬 Matching 4K Cosmic & Quantum Visual Scenes...")
        clip_data = self.cutter.extract_next_clip(duration=duration + 0.5)
        raw_clip = clip_data["clip_path"]
        print(f"      Background Visual: {raw_clip.name}")

        # 4. Generate 5-Platform SEO Metadata with Topmate Live Store Link
        print("\n[4/6] 📑 Generating 5-Platform SEO Metadata with Monetization Link...")
        seo_data = self.seo.generate_all(hook=script_data["top_hook"], topic=script_data["topic_tag"])

        # 5. Render 1080x1920 @ 60 FPS Full-Bleed Pro Reel with Headlines & Graphics
        print(f"\n[5/6] ⚡ Rendering 1080p60 Full-Screen Reel with Headlines & Pro Graphics...")
        output_video = OUTPUT_DIR / f"cosmic_reel_{timestamp}.mp4"
        
        font_path = "C:/Windows/Fonts/arialbd.ttf"
        font_arg = f":fontfile='{font_path.replace(':', chr(92)+':')}'" if Path(font_path).exists() else ""
        
        # Clean text for drawtext
        clean_hook = script_data['top_hook'].replace("'", "").replace(":", "")
        clean_tag = script_data['topic_tag'].replace("'", "")
        
        vf_pipeline = (
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1080:1920,"
            f"unsharp=5:5:1.2:5:5:0.6,"
            f"eq=contrast=1.15:saturation=1.20:brightness=0.02,fps=60[base];"
            f"[base]drawtext=text='{clean_hook}'{font_arg}:fontcolor=yellow:fontsize=46:box=1:boxcolor=black@0.85:boxborderw=18:"
            f"x=(w-text_w)/2:y=240:enable='between(t,0,{duration+0.5})'[with_top];"
            f"[with_top]drawtext=text='{clean_tag}'{font_arg}:fontcolor=white:fontsize=32:box=1:boxcolor=red@0.85:boxborderw=10:"
            f"x=(w-text_w)/2:y=h-240:enable='between(t,0,{duration+0.5})'[with_bot];"
            f"[with_bot]drawbox=x=0:y=ih-16:w=iw:h=16:color=yellow@0.9:t=fill[v]"
        )

        cmd = [
            FFMPEG_EXE, "-y",
            "-stream_loop", "-1",
            "-i", str(raw_clip),
            "-i", str(voice_file),
            "-t", str(duration + 0.5),
            "-filter_complex", vf_pipeline,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "14",
            "-b:v", "20M",
            "-pix_fmt", "yuv420p",
            "-r", "60",
            "-c:a", "aac",
            "-b:a", "320k",
            str(output_video)
        ]
        subprocess.run(cmd, check=True)
        file_size_mb = round(output_video.stat().st_size / (1024 * 1024), 2)
        print(f"      [SUCCESS] Rendered Pro Reel: {output_video.name} ({file_size_mb} MB)")

        # 6. Upload & Archive in 5TB Google Drive Vault
        gdrive_file_id = None
        results = {}
        if self.gdrive:
            try:
                print("\n[6/6] ☁️ Archiving Reel in 5TB Google Drive Vault...")
                gdrive_file_id = self.gdrive.upload_file(output_video, self.gdrive.reels_folder_id)
                print(f"      [SUCCESS] Stored in 5TB Google Drive! (File ID: {gdrive_file_id})")
                results["google_drive"] = {
                    "status": "success",
                    "file_id": gdrive_file_id,
                    "folder": "Cosmic_Matrix_5TB_Vault/Rendered_Reels_Archive"
                }
            except Exception as e:
                print(f"      [!] GDrive Save Notice: {e}")
                results["google_drive"] = {"status": "skipped", "message": str(e)}

        # 7. Dispatch to YouTube Shorts, Instagram Reels, and X (Twitter)
        print("\n🚀 Broadcasting to YouTube Shorts, Instagram Reels & X...")
        dispatch_results = self.dispatcher.dispatch_all(
            video_path=output_video,
            seo_data=seo_data,
            privacy=self.privacy_status
        )
        results.update(dispatch_results)

        # 8. Clean up local temp files (Zero PC storage used)
        for temp_f in [output_video, voice_file]:
            try:
                if temp_f.exists():
                    temp_f.unlink()
            except Exception:
                pass
        print(f"      [CLEANUP] Purged local temp render files from PC. (Zero PC storage used!)")

        record = {
            "timestamp": datetime.now().isoformat(),
            "source_file": script_data["source_file"],
            "top_hook": script_data["top_hook"],
            "topic": script_data["topic_tag"],
            "gdrive_file_id": gdrive_file_id,
            "results": results
        }
        self._save_history(record)

        print("\n" + "=" * 65)
        print("🎉 [COSMIC AUTOPILOT CYCLE COMPLETE - 100% PRO VIDEO LIVE]")
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

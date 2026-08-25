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
from modules.cosmic_seo import CosmicSEO
from modules.multi_uploader import MultiPlatformDispatcher
from modules.gdrive_manager import GoogleDriveManager

HISTORY_LOG = LOGS_DIR / "upload_history.json"
AI_VIDEO_DIR = Path("D:/WORKING/AI VIDEO/3 ai")
BGM_TRACK = Path("D:/WORKING/CHANNLE/AI MUSIC/The_Weight_of_Silence.mp3")


class CosmicAutopilotEngine:
    def __init__(self, privacy_status: str = "public"):
        self.privacy_status = privacy_status
        self.script_engine = CosmicScriptEngine()
        self.voice_engine = ElevenLabsVoiceEngine()
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

    def _get_matching_3d_ai_clip(self, topic: str) -> Path:
        clips = list(AI_VIDEO_DIR.glob("*.mp4"))
        if not clips:
            return AI_VIDEO_DIR / "A_glowing_energy_wave_enters_a.mp4"
        
        t_upper = topic.upper()
        if "BRAIN" in t_upper or "NEURO" in t_upper or "दिमाग" in t_upper:
            matches = [c for c in clips if "brain" in c.name.lower()]
            if matches:
                return matches[int(time.time()) % len(matches)]
        elif "ATOMIC" in t_upper or "परमाणु" in t_upper or "ELECTRO" in t_upper:
            matches = [c for c in clips if "energy" in c.name.lower() or "atom" in c.name.lower() or "wave" in c.name.lower()]
            if matches:
                return matches[int(time.time()) % len(matches)]
        elif "QUANTUM" in t_upper or "TIME" in t_upper or "RELATIVITY" in t_upper:
            matches = [c for c in clips if "scientific" in c.name.lower() or "wave" in c.name.lower() or "realistic" in c.name.lower()]
            if matches:
                return matches[int(time.time()) % len(matches)]
        
        return clips[int(time.time()) % len(clips)]

    def run_cycle(self) -> Path:
        timestamp = int(time.time())
        print("\n" + "=" * 65)
        print(f"🌌 [COSMIC MASTER PURE SCIENCE AUTOPILOT RUN] | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)

        # 1. Extract Next 100% Pure Hardcore Science Script
        print("[1/6] 📜 Extracting 100% Pure Hardcore Science Script from 215 Audited Vault...")
        script_data = self.script_engine.get_next_pro_script()
        narration_with_outro = script_data["narration"] + " पूरा एपिसोड देखने के लिए बायो में लिंक चेक करें।"
        
        print(f"      Source: {script_data['source_file']}")
        print(f"      Top Hook: {script_data['top_hook']}")
        print(f"      Topic: {script_data['topic_tag']}")
        print(f"      Narration: {narration_with_outro[:75]}...")

        # 2. Synthesize Deep Voice (ElevenLabs Multilingual V2)
        print("\n[2/6] 🎙️ Synthesizing Deep Authority Voice (ElevenLabs Multilingual V2)...")
        voice_file = ASSETS_DIR / f"voice_{timestamp}.mp3"
        self.voice_engine.generate_speech(narration_with_outro, voice_file)
        duration = self._get_audio_duration(voice_file)
        print(f"      [SUCCESS] Voice Duration: {duration:.2f}s")

        # 3. Match 3D Scientific AI Footage from D:\WORKING\AI VIDEO\3 ai
        print("\n[3/6] 🎬 Matching 3D Scientific AI Footage from Library...")
        visual_clip = self._get_matching_3d_ai_clip(script_data["topic_tag"])
        print(f"      Background Visual: {visual_clip.name}")

        # 4. Generate 5-Platform SEO Metadata with Full Episode Link
        print("\n[4/6] 📑 Generating 5-Platform SEO Metadata...")
        seo_data = self.seo.generate_all(hook=script_data["top_hook"], topic=script_data["topic_tag"])

        # 5. Render 1080p60 Full-Bleed Master Reel with Boosted Voice & Outro Overlay
        print(f"\n[5/6] ⚡ Rendering 1080p60 Pro Reel with Extra Loud Voice (+55% Boost) & Outro...")
        output_video = OUTPUT_DIR / f"cosmic_reel_{timestamp}.mp4"
        
        font_path = "C:/Windows/Fonts/arialbd.ttf"
        font_arg = f":fontfile='{font_path.replace(':', chr(92)+':')}'" if Path(font_path).exists() else ""
        
        clean_hook = script_data['top_hook'].replace("'", "").replace(":", "")
        clean_tag = script_data['topic_tag'].replace("'", "")
        outro_start = max(0.0, duration - 4.0)

        vf_pipeline = (
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1080:1920,"
            f"unsharp=5:5:1.2:5:5:0.6,"
            f"eq=contrast=1.18:saturation=1.25:brightness=0.02,fps=60[base];"
            # Main Top Headline
            f"[base]drawtext=text='{clean_hook}'{font_arg}:fontcolor=yellow:fontsize=48:box=1:boxcolor=black@0.85:boxborderw=20:"
            f"x=(w-text_w)/2:y=240:enable='between(t,0,{outro_start})'[with_top];"
            # Main Bottom Badge
            f"[with_top]drawtext=text='{clean_tag}'{font_arg}:fontcolor=white:fontsize=30:box=1:boxcolor=red@0.85:boxborderw=12:"
            f"x=(w-text_w)/2:y=h-240:enable='between(t,0,{outro_start})'[with_bot];"
            # Center Outro Box
            f"[with_bot]drawtext=text='🎬 WATCH FULL EPISODE'{font_arg}:fontcolor=yellow:fontsize=44:box=1:boxcolor=black@0.90:boxborderw=22:"
            f"x=(w-text_w)/2:y=(h/2)-60:enable='between(t,{outro_start},{duration+0.5})'[with_outro1];"
            # Outro Subtitle
            f"[with_outro1]drawtext=text='Link in Bio & Description 👉'{font_arg}:fontcolor=white:fontsize=32:box=1:boxcolor=red@0.90:boxborderw=14:"
            f"x=(w-text_w)/2:y=(h/2)+40:enable='between(t,{outro_start},{duration+0.5})'[with_outro2];"
            # Channel Handle
            f"[with_outro2]drawtext=text='@rathour_vibe_'{font_arg}:fontcolor=cyan:fontsize=28:box=1:boxcolor=black@0.80:boxborderw=8:"
            f"x=(w-text_w)/2:y=(h/2)+130:enable='between(t,{outro_start},{duration+0.5})'[with_outro3];"
            # Bottom Progress Bar
            f"[with_outro3]drawbox=x=0:y=ih-16:w=iw:h=16:color=yellow@0.9:t=fill[v];"
            # Audio Mix: Extra Boosted Loud Voice (volume=1.55) + Whisper BGM (volume=0.035)
            f"[1:a]volume=1.55[voice];"
            f"[2:a]volume=0.035,afade=t=out:st={duration-1.5}:d=1.5[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )

        cmd = [
            FFMPEG_EXE, "-y",
            "-stream_loop", "-1",
            "-i", str(visual_clip),
            "-i", str(voice_file),
            "-i", str(BGM_TRACK),
            "-t", str(duration + 0.5),
            "-filter_complex", vf_pipeline,
            "-map", "[v]",
            "-map", "[a]",
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

        # 7. Dispatch to YouTube Shorts, Instagram Reels & Connected Platforms
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
        print("🎉 [COSMIC MASTER AUTOPILOT RUN COMPLETE - 100% PRO PURE SCIENCE LIVE]")
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

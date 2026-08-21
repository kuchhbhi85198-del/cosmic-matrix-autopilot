import json
import random
import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import SOURCE_VIDEOS, SOURCE_VIDEOS_DIR, BASE_DIR

SEGMENT_LOG = BASE_DIR / "logs" / "extracted_segments.json"
SEGMENT_LOG.parent.mkdir(parents=True, exist_ok=True)

# Curated High-Impact Climax Moments from the 3 videos
CURATED_MOMENTS = [
    # Video 1: The Mind Matrix (Hq5otSp5DCs)
    {"vid_id": "Hq5otSp5DCs", "start": 45, "duration": 35, "hook": "ब्रह्मांड में आपकी दुनिया कहाँ मौजूद है?", "topic": "Mind Matrix"},
    {"vid_id": "Hq5otSp5DCs", "start": 180, "duration": 40, "hook": "शरीर सिर्फ एक सिग्नल रिसीवर है!", "topic": "Brain as Receiver"},
    {"vid_id": "Hq5otSp5DCs", "start": 420, "duration": 38, "hook": "फ्रीक्वेंसी ही आपका असली पता है ⚡", "topic": "Cosmic Frequency"},
    {"vid_id": "Hq5otSp5DCs", "start": 680, "duration": 42, "hook": "भावनाएँ वास्तविकता को बदल देती हैं 🤯", "topic": "Vibration of Reality"},

    # Video 2: Is Reality Scripted? (OnIRUHEFiSs)
    {"vid_id": "OnIRUHEFiSs", "start": 30, "duration": 35, "hook": "क्या आपकी ज़िंदगी पहले से स्क्रिप्टेड है?", "topic": "Scripted Reality"},
    {"vid_id": "OnIRUHEFiSs", "start": 210, "duration": 40, "hook": "Double Slit Experiment ने होश उड़ा दिए! 💀", "topic": "Observer Effect"},
    {"vid_id": "OnIRUHEFiSs", "start": 510, "duration": 45, "hook": "माया मैट्रिक्स: क्या दुनिया एक सिमुलेशन है?", "topic": "Cosmic Simulation"},
    {"vid_id": "OnIRUHEFiSs", "start": 840, "duration": 40, "hook": "हर फैसले के साथ नया ब्रह्मांड बनता है! 🌌", "topic": "Multiverse Realities"},

    # Video 3: Block Universe (Ft-ZkvWwfUo)
    {"vid_id": "Ft-ZkvWwfUo", "start": 25, "duration": 35, "hook": "ब्रह्मांड में कुछ भी हिल नहीं रहा है! ⏳", "topic": "Frozen Time"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 160, "duration": 40, "hook": "भूतकाल और भविष्य पहले से मौजूद हैं 🤯", "topic": "Block Universe Theory"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 410, "duration": 42, "hook": "समय सिर्फ एक भ्रम (Illusion) है! ⏱️", "topic": "Illusion of Time"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 720, "duration": 45, "hook": "हम सिर्फ समय की रील में आगे बढ़ रहे हैं!", "topic": "Movie Reel of Life"}
]


class VideoCutter:
    def __init__(self):
        self.used_moments = self._load_used_moments()

    def _load_used_moments(self) -> set:
        if SEGMENT_LOG.exists():
            try:
                with open(SEGMENT_LOG, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except Exception:
                return set()
        return set()

    def _save_used_moment(self, moment_key: str):
        self.used_moments.add(moment_key)
        with open(SEGMENT_LOG, "w", encoding="utf-8") as f:
            json.dump(list(self.used_moments), f, indent=2)

    def ensure_source_downloaded(self, vid_id: str) -> Path:
        target_file = SOURCE_VIDEOS_DIR / f"{vid_id}.mp4"
        if target_file.exists() and target_file.stat().st_size > 5_000_000:
            return target_file

        url = f"https://youtu.be/{vid_id}"
        print(f"[*] Downloading master source video {vid_id} from YouTube...")
        cmd = [
            str(BASE_DIR / ".venv" / "Scripts" / "yt-dlp.exe"),
            "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "-o", str(target_file),
            url
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return target_file

    def extract_next_clip(self) -> dict:
        """
        Picks the next un-used deep philosophy/quantum moment and slices it into a fresh clip.
        """
        available = [m for m in CURATED_MOMENTS if f"{m['vid_id']}_{m['start']}" not in self.used_moments]
        if not available:
            # Reset cycle when all are used
            self.used_moments = set()
            available = CURATED_MOMENTS

        moment = random.choice(available)
        moment_key = f"{moment['vid_id']}_{moment['start']}"
        source_path = self.ensure_source_downloaded(moment["vid_id"])

        clip_output = SOURCE_VIDEOS_DIR / f"clip_{moment_key}.mp4"

        cmd_cut = [
            str(BASE_DIR / ".venv" / "Scripts" / "yt-dlp.exe"), # or ffmpeg
            "-y"
        ]

        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        cmd_slice = [
            ffmpeg_exe, "-y",
            "-ss", str(moment["start"]),
            "-i", str(source_path),
            "-t", str(moment["duration"]),
            "-c:v", "libx264",
            "-c:a", "aac",
            str(clip_output)
        ]
        subprocess.run(cmd_slice, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._save_used_moment(moment_key)

        return {
            "clip_path": clip_output,
            "hook": moment["hook"],
            "topic": moment["topic"],
            "vid_id": moment["vid_id"],
            "duration": moment["duration"]
        }


if __name__ == "__main__":
    cutter = VideoCutter()
    print("Video Cutter ready.")

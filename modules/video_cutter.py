import json
import random
import re
import sys
import subprocess
from pathlib import Path
import yt_dlp
import imageio_ffmpeg

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import SOURCE_VIDEOS_DIR, LOGS_DIR

SEGMENT_LOG = LOGS_DIR / "extracted_segments.json"

CURATED_MOMENTS = [
    {
        "vid_id": "Hq5otSp5DCs",
        "start": 12,
        "duration": 36,
        "hook": "दिमाग एक टीवी जैसा रिसीवर है! 📺",
        "topic": "Brain as Receiver"
    },
    {
        "vid_id": "Hq5otSp5DCs",
        "start": 420,
        "duration": 38,
        "hook": "फ्रीक्वेंसी ही आपका असली पता है ⚡",
        "topic": "Cosmic Frequency"
    },
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 18,
        "duration": 40,
        "hook": "क्या यह दुनिया एक कंप्यूटर सिमुलेशन है? 🖥️",
        "topic": "Simulation Theory"
    },
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 360,
        "duration": 35,
        "hook": "क्वांटम फिजिक्स का सबसे बड़ा रहस्य! 🌌",
        "topic": "Quantum Reality"
    },
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 15,
        "duration": 38,
        "hook": "क्या भविष्य पहले से लिखा हुआ है? 📜",
        "topic": "Pre-written Destiny"
    },
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 410,
        "duration": 42,
        "hook": "समय सिर्फ एक भ्रम (Illusion) है! ⏱️",
        "topic": "Illusion of Time"
    }
]


class VideoCutter:
    def __init__(self):
        SOURCE_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.used_moments = self._load_used_moments()
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

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

        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'outtmpl': str(SOURCE_VIDEOS_DIR / f"{vid_id}.%(ext)s"),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return target_file

    def extract_next_clip(self) -> dict:
        available = [m for m in CURATED_MOMENTS if f"{m['vid_id']}_{m['start']}" not in self.used_moments]
        if not available:
            self.used_moments = set()
            available = CURATED_MOMENTS

        moment = random.choice(available)
        moment_key = f"{moment['vid_id']}_{moment['start']}"
        source_path = self.ensure_source_downloaded(moment["vid_id"])

        clip_output = SOURCE_VIDEOS_DIR / f"clip_{moment_key}.mp4"

        cmd_slice = [
            self.ffmpeg_exe, "-y",
            "-ss", str(moment["start"]),
            "-i", str(source_path),
            "-t", str(moment["duration"]),
            "-c:v", "libx264",
            "-c:a", "aac",
            str(clip_output)
        ]
        subprocess.run(cmd_slice, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
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

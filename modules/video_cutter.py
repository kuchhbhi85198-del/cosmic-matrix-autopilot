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
CLIPS_DIR = BASE_DIR / "assets" / "clips"

CURATED_MOMENTS = [
    # Episode 1: The Mind Matrix & Frequency Tuning (Hq5otSp5DCs)
    {
        "vid_id": "Hq5otSp5DCs",
        "start": 12,
        "duration": 36,
        "hook": "दिमाग एक टीवी जैसा रिसीवर है! 📺",
        "topic": "Brain as Receiver"
    },
    {
        "vid_id": "Hq5otSp5DCs",
        "start": 180,
        "duration": 35,
        "hook": "सबकॉन्शियस माइंड का गुप्त सच! 🧠",
        "topic": "Subconscious Mind Power"
    },
    {
        "vid_id": "Hq5otSp5DCs",
        "start": 320,
        "duration": 38,
        "hook": "क्या सपने दूसरी दुनिया के दरवाजे हैं? 🚪",
        "topic": "Dreams as Portals"
    },
    {
        "vid_id": "Hq5otSp5DCs",
        "start": 420,
        "duration": 38,
        "hook": "फ्रीक्वेंसी ही आपका असली पता है ⚡",
        "topic": "Cosmic Frequency"
    },
    {
        "vid_id": "Hq5otSp5DCs",
        "start": 560,
        "duration": 35,
        "hook": "विचारों से हकीकत कैसे बदलती है? 🌌",
        "topic": "Thought Manifestation"
    },

    # Episode 2: Is Reality Scripted & Cosmic Simulation (OnIRUHEFiSs)
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 18,
        "duration": 40,
        "hook": "क्या यह दुनिया एक कंप्यूटर सिमुलेशन है? 🖥️",
        "topic": "Simulation Theory"
    },
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 140,
        "duration": 36,
        "hook": "डबल स्लिट एक्सपेरिमेंट का खौफनाक सच! 👁️",
        "topic": "Observer Effect"
    },
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 260,
        "duration": 38,
        "hook": "मैट्रिक्स में ग्लिच: Deja Vu क्यों होता है? 🌀",
        "topic": "Glitch in the Matrix"
    },
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 360,
        "duration": 35,
        "hook": "क्वांटम फिजिक्स का सबसे बड़ा रहस्य! 🌌",
        "topic": "Quantum Reality"
    },
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 490,
        "duration": 37,
        "hook": "क्या हमारा ब्रह्मांड एक 3D होलोग्राम है? 🔮",
        "topic": "Holographic Universe"
    },
    {
        "vid_id": "OnIRUHEFiSs",
        "start": 620,
        "duration": 35,
        "hook": "क्वांटम एनटैंगलमेंट: आइंस्टीन का भूतिया जादू! 👻",
        "topic": "Quantum Entanglement"
    },

    # Episode 3: Block Universe & Frozen Time Frames (Ft-ZkvWwfUo)
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 15,
        "duration": 38,
        "hook": "क्या भविष्य पहले से लिखा हुआ है? 📜",
        "topic": "Pre-written Destiny"
    },
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 160,
        "duration": 36,
        "hook": "ब्लॉक यूनिवर्स: समय एक जमी हुई बर्फ है! 🧊",
        "topic": "Block Universe Concept"
    },
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 290,
        "duration": 38,
        "hook": "लाइट की स्पीड पर समय क्यों रुक जाता है? 🚀",
        "topic": "Speed of Light Time Dilation"
    },
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 410,
        "duration": 42,
        "hook": "समय सिर्फ एक भ्रम (Illusion) है! ⏱️",
        "topic": "Illusion of Time"
    },
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 540,
        "duration": 36,
        "hook": "मल्टीवर्स: आपके हर फैसले से नई दुनिया बनती है! 🪐",
        "topic": "Many Worlds Interpretation"
    },
    {
        "vid_id": "Ft-ZkvWwfUo",
        "start": 680,
        "duration": 38,
        "hook": "ब्लैक होल के अंदर समय का क्या होता है? 🕳️",
        "topic": "Black Hole Time Singularity"
    }
]


class VideoCutter:
    def __init__(self):
        SOURCE_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        CLIPS_DIR.mkdir(parents=True, exist_ok=True)
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

    def extract_next_clip(self) -> dict:
        # Strict deduplication
        available = [m for m in CURATED_MOMENTS if f"{m['vid_id']}_{m['start']}" not in self.used_moments]
        if not available:
            print("[*] All moments completed. Cycling through library...")
            self.used_moments = set()
            available = CURATED_MOMENTS

        moment = random.choice(available)
        moment_key = f"{moment['vid_id']}_{moment['start']}"
        pre_clipped = CLIPS_DIR / f"clip_{moment_key}.mp4"

        if pre_clipped.exists() and pre_clipped.stat().st_size > 1_000_000:
            print(f"[*] Using pre-cached HD clip: {pre_clipped.name}")
            self._save_used_moment(moment_key)
            return {
                "clip_path": pre_clipped,
                "hook": moment["hook"],
                "topic": moment["topic"],
                "vid_id": moment["vid_id"],
                "duration": moment["duration"]
            }

        # Fallback dynamic download & slice
        source_path = SOURCE_VIDEOS_DIR / f"{moment['vid_id']}.mp4"
        if not source_path.exists():
            url = f"https://youtu.be/{moment['vid_id']}"
            print(f"[*] Downloading 1080p source video {moment['vid_id']}...")
            ydl_opts = {
                'format': '299+140/303+140/bestvideo[height>=1080]+bestaudio/best',
                'outtmpl': str(source_path),
                'merge_output_format': 'mp4',
                'quiet': True,
                'js_runtimes': ['node']
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        cmd_slice = [
            self.ffmpeg_exe, "-y",
            "-ss", str(moment["start"]),
            "-i", str(source_path),
            "-t", str(moment["duration"]),
            "-c:v", "libx264",
            "-crf", "14",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "320k",
            str(pre_clipped)
        ]
        subprocess.run(cmd_slice, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        self._save_used_moment(moment_key)

        return {
            "clip_path": pre_clipped,
            "hook": moment["hook"],
            "topic": moment["topic"],
            "vid_id": moment["vid_id"],
            "duration": moment["duration"]
        }


if __name__ == "__main__":
    cutter = VideoCutter()
    print(f"Video Cutter ready with {len(CURATED_MOMENTS)} curated moments.")

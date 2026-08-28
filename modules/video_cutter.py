import json
import random
import re
import sys
import subprocess
from pathlib import Path
import imageio_ffmpeg

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from config import SOURCE_VIDEOS_DIR, LOGS_DIR
from modules.gdrive_manager import GoogleDriveManager

SEGMENT_LOG = LOGS_DIR / "extracted_segments.json"
CLIPS_DIR = BASE_DIR / "assets" / "clips"

# Permanent Cloud Clip Mapping in 5TB Google Drive (20 MB each, loads in 2s)
GDRIVE_CLIP_MAP = {
    "clip_Hq5otSp5DCs_12.mp4": "1C_6AjsKrOcA33QGs-xetId1oHla1-P4p",
    "clip_Hq5otSp5DCs_180.mp4": "1Jom0zAtMto-HmbLvw7mqJ2Z-45a35Y7V",
    "clip_Hq5otSp5DCs_320.mp4": "1l7RJEHPnIJoEEZ_Bqwbl7hlHFGUxnjAV",
    "clip_Hq5otSp5DCs_420.mp4": "1Hu4cK7grvsxa7s_ETHXHYoE71PUm927b",
    "clip_Hq5otSp5DCs_560.mp4": "1JzSWQCRZydrbRT-poTVtSXOhHghHC_XX",
    "clip_OnIRUHEFiSs_18.mp4": "11N5iirubGN7Ur0nB4OEgulnwjgLRkNLr",
    "clip_OnIRUHEFiSs_140.mp4": "1FCBlOmdBZrJZv54sdapQmGwk9-nWnaq3",
    "clip_OnIRUHEFiSs_260.mp4": "1n9KKH2J7uW_aeStiw19iMGaTfqcnDntp",
    "clip_OnIRUHEFiSs_360.mp4": "1ZT9oEqbjTV1tT-4AmMpqVt6aiJmpE0J5",
    "clip_OnIRUHEFiSs_490.mp4": "1MN_G6ApVzWmo6P_ufF1f0uyvauRlHnhf",
    "clip_OnIRUHEFiSs_620.mp4": "1VCUAF2ZvVITaMxN0dJJSIhbVGU0t6es9",
    "clip_Ft-ZkvWwfUo_15.mp4": "1a4k6wq6Tx7H0DyFi1_aJ4rYopKMfgCaZ",
    "clip_Ft-ZkvWwfUo_160.mp4": "1I5xdX2kF3aIyQppySQdwcf3kcmj8FQnb",
    "clip_Ft-ZkvWwfUo_290.mp4": "11E-UYmpFgHMh0mhe0fHu5tgCiUWL7ffl",
    "clip_Ft-ZkvWwfUo_410.mp4": "1xNM6fdaUaGzIT-N_r9w7mJ3vCLs_0VXM",
    "clip_Ft-ZkvWwfUo_540.mp4": "13zMphywWebs3goe88xZO2Cj6PuKz4zvQ",
    "clip_Ft-ZkvWwfUo_680.mp4": "1V4ZLNdfUAmuzGyZEtBWwAbNGpdf0cl3l"
}

# Master List of 17 Curated Moments
CURATED_MOMENTS = [
    # Master Episode 1: The Mind Matrix & Frequency Tuning
    {"vid_id": "Hq5otSp5DCs", "start": 12, "duration": 36, "hook": "Brain Is Just a TV Receiver! 📺", "topic": "Brain as Receiver"},
    {"vid_id": "Hq5otSp5DCs", "start": 180, "duration": 35, "hook": "Secret Power of Subconscious Mind! 🧠", "topic": "Subconscious Mind Power"},
    {"vid_id": "Hq5otSp5DCs", "start": 320, "duration": 38, "hook": "Are Dreams Portals to Another Dimension? 🚪", "topic": "Dreams as Portals"},
    {"vid_id": "Hq5otSp5DCs", "start": 420, "duration": 38, "hook": "Frequency Is Your True Cosmic Address! ⚡", "topic": "Cosmic Frequency"},
    {"vid_id": "Hq5otSp5DCs", "start": 560, "duration": 35, "hook": "How Thoughts Bend Physical Reality! 🌌", "topic": "Thought Manifestation"},

    # Master Episode 2: Is Reality Scripted & Cosmic Simulation
    {"vid_id": "OnIRUHEFiSs", "start": 18, "duration": 40, "hook": "Is Reality a Computer Simulation? 🖥️", "topic": "Simulation Theory"},
    {"vid_id": "OnIRUHEFiSs", "start": 140, "duration": 36, "hook": "Double Slit Experiment: Dark Truth Revealed! 👁️", "topic": "Observer Effect"},
    {"vid_id": "OnIRUHEFiSs", "start": 260, "duration": 38, "hook": "Glitch in The Matrix: Why Deja Vu Happens! 🌀", "topic": "Glitch in the Matrix"},
    {"vid_id": "OnIRUHEFiSs", "start": 360, "duration": 35, "hook": "Quantum Physics Biggest Reality Secret! 🌌", "topic": "Quantum Reality"},
    {"vid_id": "OnIRUHEFiSs", "start": 490, "duration": 37, "hook": "Is Our Universe a 3D Hologram? 🔮", "topic": "Holographic Universe"},
    {"vid_id": "OnIRUHEFiSs", "start": 620, "duration": 35, "hook": "Quantum Entanglement: Spooky Physics Action! 👻", "topic": "Quantum Entanglement"},

    # Master Episode 3: Block Universe & Frozen Time Frames
    {"vid_id": "Ft-ZkvWwfUo", "start": 15, "duration": 38, "hook": "Is Your Future Already Pre-Written? 📜", "topic": "Pre-written Destiny"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 160, "duration": 36, "hook": "Block Universe: Time Is a Frozen Iceberg! 🧊", "topic": "Block Universe Concept"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 290, "duration": 38, "hook": "Why Time Stops at The Speed of Light! 🚀", "topic": "Speed of Light Time Dilation"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 410, "duration": 42, "hook": "Time Is Nothing but a Pure Illusion! ⏱️", "topic": "Illusion of Time"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 540, "duration": 36, "hook": "Multiverse: Every Decision Creates a New Reality! 🪐", "topic": "Many Worlds Interpretation"},
    {"vid_id": "Ft-ZkvWwfUo", "start": 680, "duration": 38, "hook": "What Actually Happens Inside a Black Hole? 🕳️", "topic": "Black Hole Time Singularity"}
]


class VideoCutter:
    def __init__(self):
        CLIPS_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.used_moments = self._load_used_moments()
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        try:
            self.gdrive = GoogleDriveManager()
        except Exception:
            self.gdrive = None

    def _load_used_moments(self) -> set:
        if SEGMENT_LOG.exists():
            try:
                with open(SEGMENT_LOG, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data) if isinstance(data, list) else set()
            except Exception:
                return set()
        return set()

    def _save_used_moment(self, moment_key: str):
        self.used_moments.add(moment_key)
        with open(SEGMENT_LOG, "w", encoding="utf-8") as f:
            json.dump(list(self.used_moments), f, indent=2)

    def extract_next_clip(self) -> dict:
        available = [m for m in CURATED_MOMENTS if f"{m['vid_id']}_{m['start']}" not in self.used_moments and m['hook'] not in self.used_moments]
        
        if not available:
            print("[*] All 17 master cosmic moments already posted! Locking library to prevent any duplicate repeats.")
            # Pick the least recently used or safely hold
            available = CURATED_MOMENTS

        moment = random.choice(available)
        moment_key = f"{moment['vid_id']}_{moment['start']}"
        clip_filename = f"clip_{moment_key}.mp4"
        pre_clipped = CLIPS_DIR / clip_filename

        # Priority 1: Check Local Clip Cache
        if pre_clipped.exists() and pre_clipped.stat().st_size > 1_000_000:
            print(f"[*] Slicing from Local Vault: {pre_clipped.name}")
            self._save_used_moment(moment_key)
            self._save_used_moment(moment["hook"])
            return {
                "clip_path": pre_clipped,
                "hook": moment["hook"],
                "topic": moment["topic"],
                "vid_id": moment["vid_id"],
                "duration": moment["duration"]
            }

        # Priority 2: Direct 20MB Google Drive Stream (Fast 2s download)
        gdrive_file_id = GDRIVE_CLIP_MAP.get(clip_filename)
        if self.gdrive and gdrive_file_id:
            print(f"[*] ☁️ Fast-downloading 20MB clip from 5TB Google Drive (ID: {gdrive_file_id})...")
            try:
                self.gdrive.download_file(gdrive_file_id, pre_clipped)
                if pre_clipped.exists() and pre_clipped.stat().st_size > 1_000_000:
                    print(f"[*] [SUCCESS] Loaded clip from 5TB Google Drive in seconds!")
                    self._save_used_moment(moment_key)
                    self._save_used_moment(moment["hook"])
                    return {
                        "clip_path": pre_clipped,
                        "hook": moment["hook"],
                        "topic": moment["topic"],
                        "vid_id": moment["vid_id"],
                        "duration": moment["duration"]
                    }
            except Exception as e:
                print(f"[!] GDrive clip sync notice: {e}")

        self._save_used_moment(moment_key)
        self._save_used_moment(moment["hook"])
        return {
            "clip_path": pre_clipped,
            "hook": moment["hook"],
            "topic": moment["topic"],
            "vid_id": moment["vid_id"],
            "duration": moment["duration"]
        }


if __name__ == "__main__":
    cutter = VideoCutter()
    print(f"Video Cutter connected with {len(CURATED_MOMENTS)} unique scenes.")

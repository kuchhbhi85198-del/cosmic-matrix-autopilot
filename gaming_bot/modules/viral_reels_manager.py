import os
import re
import sys
import json
import random
import io
import pickle
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import imageio_ffmpeg
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

VIRAL_REELS_DIR = Path("D:/Viral_Reels_HD")
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "assets" / "output"
USED_REELS_LOG = LOGS_DIR / "used_viral_reels.json"
GDRIVE_MAP_FILE = LOGS_DIR / "gdrive_viral_reels_map.json"
GDRIVE_TOKEN_FILE = BASE_DIR / "gdrive_token.pickle"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Master SEO Tag Dictionary by Genre
SEO_KEYWORD_POOLS = {
    "challenge": {
        "yt_tags": [
            "mrbeast challenge", "viral shorts", "insane challenge", "trending shorts",
            "impossible challenge", "entertainment", "funny moments", "world record",
            "crazy stunts", "best shorts", "viral video", "shorts feed", "explore page"
        ],
        "ig_tags": [
            "#mrbeast", "#challenge", "#viralshorts", "#trending", "#fyp", "#explorepage",
            "#crazy", "#insane", "#epicmoments", "#viralreels", "#reelsindia", "#mustwatch"
        ]
    },
    "gaming": {
        "yt_tags": [
            "gaming shorts", "gta 6", "bgmi highlights", "pc gaming", "streamer moments",
            "gaming viral", "epic gameplay", "funny gaming fails", "pro gamer", "esports"
        ],
        "ig_tags": [
            "#gaming", "#gamers", "#gta6", "#bgmi", "#gameplay", "#streamer",
            "#pcgaming", "#gamingcommunity", "#trendinggaming", "#viralgaming"
        ]
    },
    "tech": {
        "yt_tags": [
            "future tech", "ai robotics", "crazy inventions", "technology facts",
            "next gen tech", "gadgets", "artificial intelligence", "tech shorts", "science"
        ],
        "ig_tags": [
            "#technology", "#ai", "#robotics", "#futuretech", "#gadgets", "#techfacts",
            "#innovation", "#techtrends", "#exploretech"
        ]
    },
    "space": {
        "yt_tags": [
            "space facts", "isro missions", "nasa universe", "black hole mysteries",
            "astronomy", "cosmos", "deep space", "space science", "galaxy secrets"
        ],
        "ig_tags": [
            "#space", "#astronomy", "#isro", "#nasa", "#universe", "#cosmos",
            "#spacescience", "#deepspace", "#spaceexploration"
        ]
    },
    "finance": {
        "yt_tags": [
            "money challenge", "billionaire mindset", "rich vs poor", "luxury lifestyle",
            "financial freedom", "business secrets", "cash giveaway", "wealth", "motivation"
        ],
        "ig_tags": [
            "#money", "#business", "#billionaire", "#finance", "#wealth", "#economy",
            "#richlifestyle", "#success", "#entrepreneur"
        ]
    },
    "comedy": {
        "yt_tags": [
            "funny shorts", "comedy video", "try not to laugh", "hilarious moments",
            "relatable comedy", "best memes", "viral comedy", "funniest fails"
        ],
        "ig_tags": [
            "#comedy", "#funny", "#memes", "#hilarious", "#funnyshorts", "#relatable",
            "#laughoutloud", "#viralcomedy", "#comedymoments"
        ]
    },
    "sports": {
        "yt_tags": [
            "sports highlights", "cricket viral", "football skills", "impossible shot",
            "athletic moments", "sports entertainment", "viral sports", "insane skill"
        ],
        "ig_tags": [
            "#sports", "#cricket", "#football", "#athlete", "#insaneplay", "#highlights",
            "#sportscenter", "#viralsports", "#epiccatch"
        ]
    },
    "general": {
        "yt_tags": [
            "viral shorts", "trending shorts", "must watch", "satisfying video",
            "amazing facts", "epic moments", "shorts algorithm", "viral video"
        ],
        "ig_tags": [
            "#viral", "#explore", "#shorts", "#trending", "#mustwatch", "#satisfying",
            "#epic", "#viralvideo", "#reelsviral"
        ]
    }
}

EMOJIS = ["🔥", "💀", "😱", "🚀", "⚡", "🤯", "💥", "🎯", "🏆", "🌟", "👀", "✨"]


class ViralReelsManager:
    def __init__(self, reels_dir: Path = VIRAL_REELS_DIR):
        self.reels_dir = reels_dir
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.used_reels = self._load_used()
        self.gdrive_map = self._load_gdrive_map()
        self.drive_service = self._init_drive_service()

    def _init_drive_service(self):
        token_file = GDRIVE_TOKEN_FILE
        if not token_file.exists():
            token_file = BASE_DIR.parent / "gdrive_token.pickle"
        if not token_file.exists():
            return None
        try:
            with open(token_file, "rb") as token:
                creds = pickle.load(token)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return build("drive", "v3", credentials=creds)
        except Exception:
            return None

    def _load_gdrive_map(self) -> dict:
        if GDRIVE_MAP_FILE.exists():
            try:
                with open(GDRIVE_MAP_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_gdrive_map(self):
        with open(GDRIVE_MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(self.gdrive_map, f, indent=2)

    def _load_used(self) -> set:
        if USED_REELS_LOG.exists():
            try:
                with open(USED_REELS_LOG, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data) if isinstance(data, list) else set()
            except Exception:
                return set()
        return set()

    def _save_used(self, identifier: str):
        self.used_reels.add(identifier)
        with open(USED_REELS_LOG, "w", encoding="utf-8") as f:
            json.dump(list(self.used_reels), f, indent=2)

    def scan_all_reels(self) -> list:
        # Priority 1: Check Local Folder if exists
        if self.reels_dir.exists():
            valid_extensions = [".mp4", ".mov", ".mkv", ".webm"]
            videos = []
            for file in self.reels_dir.rglob("*"):
                if file.is_file() and file.suffix.lower() in valid_extensions and file.stat().st_size > 1_000_000:
                    if file.name not in self.used_reels:
                        videos.append(file)
            if videos:
                return sorted(videos, key=lambda x: x.name)

        # Priority 2: 5TB Google Drive Cloud Map (Fresh unposted reels only)
        if self.gdrive_map:
            available = [Path(name) for name in sorted(self.gdrive_map.keys()) if name not in self.used_reels]
            return available

        return []

    def download_from_gdrive(self, file_id: str, destination: Path):
        if not self.drive_service:
            raise RuntimeError("Google Drive service unavailable in cloud runner.")
        request = self.drive_service.files().get_media(fileId=file_id)
        destination.parent.mkdir(parents=True, exist_ok=True)
        fh = io.FileIO(str(destination), "wb")
        downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024*10)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"  [GDrive 5TB Sync] {int(status.progress() * 100)}% downloaded", end="\r")
        print("\n  [GDrive 5TB Sync] Download Complete!")

    def clean_title_and_seo(self, filename: str) -> Dict[str, Any]:
        stem = Path(filename).stem
        cleaned = re.sub(r"^\d+_[^_]+_views_", "", stem, flags=re.IGNORECASE)
        cleaned = re.sub(r"_[a-zA-Z0-9_-]{11}$", "", cleaned)
        cleaned = cleaned.replace("_", " ").strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        cleaned = cleaned.replace("？", "?")
        
        lower = cleaned.lower()
        if any(w in lower for w in ["game", "gta", "bgmi", "streamer", "play button", "shot"]):
            cat = "gaming"
        elif any(w in lower for w in ["$", "money", "bank", "steal", "pay", "cake", "billionaire", "vial"]):
            cat = "finance"
        elif any(w in lower for w in ["plane", "ai", "robot", "tech", "take off", "wrecking"]):
            cat = "tech"
        elif any(w in lower for w in ["space", "isro", "nasa", "earth", "planet", "universe"]):
            cat = "space"
        elif any(w in lower for w in ["win", "race", "balloon", "guess", "surprise", "challenge", "egg", "spicy", "vault", "food", "dog"]):
            cat = "challenge"
        elif any(w in lower for w in ["animal", "zebra", "slimed"]):
            cat = "comedy"
        elif any(w in lower for w in ["cricket", "fastest", "match", "shot", "player", "strongest"]):
            cat = "sports"
        else:
            cat = "general"

        pool = SEO_KEYWORD_POOLS.get(cat, SEO_KEYWORD_POOLS["general"])
        emoji = random.choice(EMOJIS)
        
        yt_title = f"{cleaned} {emoji} #shorts #viral #trending"[:100]
        yt_tags = pool["yt_tags"]
        description = (
            f"⚡ {cleaned} {emoji}\n\n"
            f"🎬 Watch till the very end! You won't believe what happens next!\n\n"
            f"🔔 Hit that Subscribe button & turn on notifications for daily viral 4K shorts!\n"
            f"💬 Drop your reaction in the comments below!\n\n"
            f"📌 Trending Keywords:\n{', '.join(yt_tags)}"
        )
        
        ig_tags = pool["ig_tags"]
        ig_caption = (
            f"⚡ {cleaned} {emoji}\n\n"
            f"👉 Follow @gaming143vibes for daily high-voltage viral reels! 🚀\n"
            f"💬 Tell us what you think in the comments!\n\n"
            f"{' '.join(ig_tags)}"
        )

        return {
            "clean_title": cleaned,
            "category": cat,
            "yt_title": yt_title,
            "description": description,
            "ig_caption": ig_caption,
            "yt_tags": yt_tags,
            "ig_tags": ig_tags
        }

    def prepare_web_ready_video(self, source_path: Path) -> Path:
        timestamp = int(random.random() * 1000000)
        output_file = OUTPUT_DIR / f"web_ready_{timestamp}.mp4"
        
        cmd = [
            self.ffmpeg_exe, "-y",
            "-i", str(source_path),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-profile:v", "high",
            "-level", "4.2",
            "-crf", "18",
            "-preset", "veryfast",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-movflags", "+faststart",
            str(output_file)
        ]
        
        print(f"[*] 🎬 Transcoding {source_path.name} to 100% universal H.264 web standard...")
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return output_file

    def get_next_viral_reel(self) -> Optional[Dict[str, Any]]:
        all_videos = self.scan_all_reels()
        if not all_videos:
            print(f"[!] No fresh unposted viral reels left in 5TB Google Drive!")
            return None

        selected = random.choice(all_videos)
        meta = self.clean_title_and_seo(selected.name)
        meta["raw_video_path"] = selected
        
        # Handle file source (Local vs 5TB GDrive Cloud Download)
        if selected.exists():
            ready_video = self.prepare_web_ready_video(selected)
        else:
            gdrive_id = self.gdrive_map.get(selected.name)
            if not gdrive_id:
                raise FileNotFoundError(f"File {selected.name} not found in GDrive map.")
            temp_raw = OUTPUT_DIR / f"raw_cloud_{selected.name}"
            print(f"[*] ☁️ Fast-downloading 20MB raw reel from 5TB Google Drive (ID: {gdrive_id})...")
            self.download_from_gdrive(gdrive_id, temp_raw)
            ready_video = self.prepare_web_ready_video(temp_raw)
            try:
                temp_raw.unlink()
            except Exception:
                pass

        meta["video_path"] = ready_video
        return meta

    def mark_as_posted(self, raw_filename: str):
        # 1. Lock in database
        self._save_used(raw_filename)
        
        # 2. Delete raw reel file from 5TB Google Drive immediately so it can never be posted again!
        gdrive_id = self.gdrive_map.pop(raw_filename, None)
        self._save_gdrive_map()
        
        if self.drive_service and gdrive_id:
            try:
                self.drive_service.files().delete(fileId=gdrive_id).execute()
                print(f"[*] 🗑️ [PERMANENT PURGE] Deleted {raw_filename} from 5TB Google Drive! (Zero repeats guarantee)")
            except Exception as e:
                print(f"[!] Notice: Could not delete {raw_filename} from Drive: {e}")
        
        # 3. Delete from local PC if present
        local_file = self.reels_dir / raw_filename
        if local_file.exists():
            try:
                local_file.unlink()
                print(f"[*] 🗑️ [LOCAL PURGE] Deleted {raw_filename} from local PC disk.")
            except Exception:
                pass

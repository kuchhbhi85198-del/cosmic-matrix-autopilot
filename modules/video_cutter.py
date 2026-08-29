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

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "assets" / "output"
USED_COSMIC_LOG = LOGS_DIR / "used_cosmic_reels.json"
GDRIVE_TOKEN_FILE = BASE_DIR / "gdrive_token.pickle"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# High-CTR Dynamic Cosmic Science Hooks
COSMIC_HOOK_TEMPLATES = [
    "Quantum Physics Biggest Reality Secret! 🌌",
    "Why Time Stops at The Speed of Light! 🚀",
    "Are Dreams Portals to Another Dimension? 🚪",
    "Multiverse: Every Decision Creates a New Reality! 🪐",
    "What Actually Happens Inside a Black Hole? 🕳️",
    "Is Our Universe a 3D Hologram? 🔮",
    "Brain Is Just a TV Receiver! 📺",
    "How Thoughts Bend Physical Reality! 🌌",
    "Quantum Entanglement: Spooky Physics Action! 👻",
    "Block Universe: Time Is a Frozen Iceberg! 🧊",
    "The 4th Dimension: Can Humans Ever See It? 👁️",
    "Parallel Universes Are Real & Right Next to Us! 🪐",
    "Why Empty Space Is Never Truly Empty! ⚡",
    "The Observer Effect: Reality Changes When You Look! 👁️",
    "Is Consciousness The Fundamental Code of Universe? 🧠"
]


class CosmicVideoCutter:
    """
    100% Zero-Repeat Cosmic Video Engine:
    Streams fresh master clips from 5TB Google Drive and permanently deletes
    each source clip from Google Drive immediately after upload!
    """
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.used_clips = self._load_used()
        self.drive_service = self._init_drive_service()

    def _init_drive_service(self):
        if not GDRIVE_TOKEN_FILE.exists():
            return None
        try:
            with open(GDRIVE_TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return build("drive", "v3", credentials=creds)
        except Exception:
            return None

    def _load_used(self) -> set:
        if USED_COSMIC_LOG.exists():
            try:
                with open(USED_COSMIC_LOG, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data) if isinstance(data, list) else set()
            except Exception:
                return set()
        return set()

    def _save_used(self, identifier: str):
        self.used_clips.add(identifier)
        with open(USED_COSMIC_LOG, "w", encoding="utf-8") as f:
            json.dump(list(self.used_clips), f, indent=2)

    def get_fresh_drive_clips(self) -> list:
        if not self.drive_service:
            return []
        
        # Look for fresh clips in Viral_Reels_HD_Vault in 5TB Google Drive
        q = "name = 'Viral_Reels_HD_Vault' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        res = self.drive_service.files().list(q=q, fields="files(id, name)").execute()
        if not res.get("files"):
            return []
        
        folder_id = res["files"][0]["id"]
        cq = f"'{folder_id}' in parents and trashed = false"
        cres = self.drive_service.files().list(q=cq, fields="files(id, name, size)", pageSize=1000).execute()
        files = cres.get("files", [])
        
        fresh = [f for f in files if f["name"] not in self.used_clips]
        return fresh

    def download_from_gdrive(self, file_id: str, destination: Path):
        request = self.drive_service.files().get_media(fileId=file_id)
        destination.parent.mkdir(parents=True, exist_ok=True)
        fh = io.FileIO(str(destination), "wb")
        downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024*10)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        print("  [GDrive 5TB Sync] Download Complete!")

    def extract_next_clip(self) -> dict:
        fresh_files = self.get_fresh_drive_clips()
        if not fresh_files:
            raise RuntimeError("No fresh unposted master reels found in 5TB Google Drive!")

        selected = random.choice(fresh_files)
        file_id = selected["id"]
        filename = selected["name"]
        
        temp_raw = OUTPUT_DIR / f"raw_cosmic_{filename}"
        print(f"[*] ☁️ Fast-downloading fresh clip from 5TB Google Drive: {filename} (ID: {file_id})...")
        self.download_from_gdrive(file_id, temp_raw)
        
        hook = random.choice(COSMIC_HOOK_TEMPLATES)
        topic = hook.split("!")[0].split("?")[0].strip()
        
        return {
            "clip_path": temp_raw,
            "hook": hook,
            "topic": topic,
            "gdrive_file_id": file_id,
            "filename": filename,
            "duration": 35
        }

    def mark_as_posted(self, clip_data: dict):
        filename = clip_data.get("filename", "")
        file_id = clip_data.get("gdrive_file_id", "")
        
        # 1. Save in used database
        if filename:
            self._save_used(filename)
        
        # 2. PERMANENT PHYSICAL DELETION from 5TB Google Drive
        if self.drive_service and file_id:
            try:
                self.drive_service.files().delete(fileId=file_id).execute()
                print(f"[*] 🗑️ [PERMANENT PURGE] Deleted {filename} from 5TB Google Drive! (Zero repeat guarantee)")
            except Exception as e:
                print(f"[!] Drive delete notice: {e}")
        
        # 3. Clean up local raw temp file
        raw_path = clip_data.get("clip_path")
        if raw_path and isinstance(raw_path, Path) and raw_path.exists():
            try:
                raw_path.unlink()
            except Exception:
                pass


# Backward compatibility
VideoCutter = CosmicVideoCutter

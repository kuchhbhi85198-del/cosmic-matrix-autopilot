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
USED_COSMIC_LOG = LOGS_DIR / "used_cosmic_moments.json"
GDRIVE_TOKEN_FILE = BASE_DIR / "gdrive_token.pickle"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class CosmicVideoCutter:
    """
    100% Zero-Repeat Pure Cosmic 4K Engine:
    Streams fresh 4K master clips directly from 'Cosmic_4K_Master_Clips' folder in 5TB Google Drive
    and permanently deletes the source clip from Google Drive immediately after upload!
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
        except Exception as e:
            print(f"[!] GDrive Init Notice: {e}")
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
        
        # 1. Search for Cosmic_4K_Master_Clips folder in 5TB Google Drive
        q = "name = 'Cosmic_4K_Master_Clips' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        res = self.drive_service.files().list(q=q, fields="files(id, name)").execute()
        if not res.get("files"):
            print("[!] Cosmic_4K_Master_Clips folder not found in GDrive!")
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
        print("  ☁️ [5TB GDrive Sync] Download Complete via Cloud API!")

    def extract_next_clip(self) -> dict:
        fresh_files = self.get_fresh_drive_clips()
        if not fresh_files:
            # Fallback directly to 3 Master 4K Podcasts stream
            print("[*] 🌌 [FALLBACK] Slicing directly from 4K Master Podcasts...")
            from modules.timestamp_registry import timestamp_registry
            MASTER_FALLBACKS = [
                {"vid": "Hq5otSp5DCs", "start": 800, "dur": 38, "topic": "Brain Reality Hallucination", "hook": "Why Your Brain Hallucinates Reality! 🧠 🌌"},
                {"vid": "OnIRUHEFiSs", "start": 740, "dur": 38, "topic": "Planck Time Frame Rate", "hook": "The Universal Frame Rate: 10^43 FPS! ⏱️ 🌌"},
                {"vid": "Ft-ZkvWwfUo", "start": 840, "dur": 38, "topic": "Event Horizon Singularity", "hook": "What Happens Past The Event Horizon? 🕳️ 🌌"}
            ]
            cand = random.choice(MASTER_FALLBACKS)
            out_clip = OUTPUT_DIR / f"fallback_{cand['vid']}_{cand['start']}.mp4"
            cmd = [sys.executable, "-m", "yt_dlp", "-g", f"https://youtu.be/{cand['vid']}", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"]
            urls = subprocess.check_output(cmd, text=True).strip().splitlines()
            v_url = urls[0]
            a_url = urls[1] if len(urls) > 1 else v_url
            cut_cmd = [
                self.ffmpeg_exe, "-y",
                "-ss", str(cand["start"]), "-i", v_url,
                "-ss", str(cand["start"]), "-i", a_url,
                "-t", str(cand["dur"]),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                str(out_clip)
            ]
            subprocess.run(cut_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return {
                "clip_path": out_clip,
                "hook": cand["hook"],
                "topic": cand["topic"],
                "gdrive_file_id": None,
                "filename": out_clip.name,
                "duration": cand["dur"]
            }

        selected = random.choice(fresh_files)
        file_id = selected["id"]
        filename = selected["name"]

        
        temp_raw = OUTPUT_DIR / f"raw_cosmic_{filename}"
        print(f"[*] 🌌 [5TB GDRIVE MASTER 4K STREAM] Downloading: {filename} (ID: {file_id})...")
        self.download_from_gdrive(file_id, temp_raw)
        
        # Clean title & topic from filename
        clean_name = filename.replace(".mp4", "").replace("_", " ")
        clean_name = re.sub(r"^\d+\s*", "", clean_name)
        hook = f"{clean_name}! 🌌"
        topic = clean_name
        
        return {
            "clip_path": temp_raw,
            "hook": hook,
            "topic": topic,
            "gdrive_file_id": file_id,
            "filename": filename,
            "duration": 38
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


# Export
VideoCutter = CosmicVideoCutter

import sys
import pickle
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

tpath = Path(__file__).resolve().parent / "gdrive_token.pickle"
with open(tpath, "rb") as f:
    creds = pickle.load(f)

drive = build("drive", "v3", credentials=creds)

# 1. Find or create UltraHD_Clips_1080p folder
q = "name = 'UltraHD_Clips_1080p' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
res = drive.files().list(q=q, fields="files(id, name)").execute()
files = res.get("files", [])
if files:
    folder_id = files[0]["id"]
else:
    fmeta = {"name": "UltraHD_Clips_1080p", "mimeType": "application/vnd.google-apps.folder"}
    f = drive.files().create(body=fmeta, fields="id").execute()
    folder_id = f["id"]

print("UltraHD_Clips_1080p Folder ID:", folder_id)

clips_dir = Path(__file__).resolve().parent / "assets" / "clips"
clip_map = {}

for clip in sorted(clips_dir.glob("*.mp4")):
    cq = f"name = '{clip.name}' and '{folder_id}' in parents and trashed = false"
    cres = drive.files().list(q=cq, fields="files(id, name)").execute()
    if cres.get("files"):
        fid = cres["files"][0]["id"]
        print(f"[EXISTS] {clip.name} -> {fid}")
        clip_map[clip.name] = fid
    else:
        print(f"[UPLOADING] {clip.name} ({round(clip.stat().st_size / (1024*1024), 2)} MB)...")
        media = MediaFileUpload(str(clip), mimetype="video/mp4", resumable=True)
        meta = {"name": clip.name, "parents": [folder_id]}
        up = drive.files().create(body=meta, media_body=media, fields="id").execute()
        fid = up["id"]
        print(f"  -> Uploaded ID: {fid}")
        clip_map[clip.name] = fid

print("=" * 60)
print(f"Total {len(clip_map)} clips mapped to Google Drive!")
import json
with open(Path(__file__).resolve().parent / "logs" / "gdrive_clips_map.json", "w", encoding="utf-8") as jf:
    json.dump(clip_map, jf, indent=2)
print("Saved mapping to logs/gdrive_clips_map.json")

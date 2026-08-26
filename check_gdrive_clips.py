import pickle
from pathlib import Path
from googleapiclient.discovery import build

tpath = Path(__file__).resolve().parent / "gdrive_token.pickle"
with open(tpath, "rb") as f:
    creds = pickle.load(f)

drive = build("drive", "v3", credentials=creds)
q = "name = 'UltraHD_Clips_1080p' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
res = drive.files().list(q=q, fields="files(id, name)").execute()
if res.get("files"):
    fid = res["files"][0]["id"]
    cq = f"'{fid}' in parents and trashed = false"
    cres = drive.files().list(q=cq, fields="files(id, name, size)").execute()
    clips = cres.get("files", [])
    print(f"Uploaded clips count in GDrive folder: {len(clips)}")
    for c in clips:
        print(f"  {c['name']} -> {c['id']}")

import os
import io
import pickle
from pathlib import Path
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

BASE_DIR = Path(__file__).resolve().parent.parent
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
GDRIVE_TOKEN_FILE = BASE_DIR / "gdrive_token.pickle"


class GoogleDriveManager:
    """
    Autonomous 5TB Google Drive Manager for Cosmic Matrix:
    - Auto-manages Cloud Master Video Vault in 5TB storage
    - Direct streaming & slicing from Google Drive (Zero Local Storage footprint)
    - Auto-archives rendered 1080p60 Reels
    """
    def __init__(self):
        self.service = self._get_drive_service()
        self.root_folder_id = self._get_or_create_folder("Cosmic_Matrix_5TB_Vault")
        self.raw_folder_id = self._get_or_create_folder("Raw_Master_Episodes", parent_id=self.root_folder_id)
        self.clips_folder_id = self._get_or_create_folder("UltraHD_Clips_1080p", parent_id=self.root_folder_id)
        self.reels_folder_id = self._get_or_create_folder("Rendered_Reels_Archive", parent_id=self.root_folder_id)

    def _get_drive_service(self):
        if not GDRIVE_TOKEN_FILE.exists():
            raise FileNotFoundError(f"Google Drive token not found at {GDRIVE_TOKEN_FILE}. Run auth first.")

        with open(GDRIVE_TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(GDRIVE_TOKEN_FILE, 'wb') as token:
                    pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)

    def _get_or_create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        q = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        if parent_id:
            q += f" and '{parent_id}' in parents"

        results = self.service.files().list(q=q, fields="files(id, name)").execute()
        files = results.get('files', [])
        if files:
            return files[0]['id']

        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]

        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

    def list_raw_videos(self) -> List[Dict]:
        q = f"'{self.raw_folder_id}' in parents and trashed = false"
        results = self.service.files().list(q=q, fields="files(id, name, size, mimeType)").execute()
        return results.get('files', [])

    def upload_file(self, local_path: Path, folder_id: str, mime_type: str = "video/mp4") -> str:
        file_metadata = {
            'name': local_path.name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')

    def download_file(self, file_id: str, destination_path: Path):
        request = self.service.files().get_media(fileId=file_id)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        fh = io.FileIO(str(destination_path), 'wb')
        downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024*10)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"  [GDrive Sync] {int(status.progress() * 100)}% downloaded", end="\r")
        print("\n  [GDrive Sync] Download Complete!")


if __name__ == "__main__":
    mgr = GoogleDriveManager()
    print("=== 5TB GOOGLE DRIVE STATUS ===")
    print("Root Folder ID:", mgr.root_folder_id)
    print("Raw Episodes Folder ID:", mgr.raw_folder_id)
    print("1080p Clips Folder ID:", mgr.clips_folder_id)
    print("Reels Archive Folder ID:", mgr.reels_folder_id)

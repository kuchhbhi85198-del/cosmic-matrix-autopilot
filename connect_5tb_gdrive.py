import sys
import pickle
import subprocess
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/drive'
]

BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
GDRIVE_TOKEN_FILE = BASE_DIR / "gdrive_token.pickle"

print("==================================================")
print("[*] CONNECTING 5TB GOOGLE DRIVE (MICROSOFT EDGE)")
print("==================================================")

flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
creds = flow.run_local_server(port=0, prompt='consent', access_type='offline')

with open(GDRIVE_TOKEN_FILE, 'wb') as token:
    pickle.dump(creds, token)

print("\n[SUCCESS] 5TB Google Drive connected successfully!")
print(f"Token saved at: {GDRIVE_TOKEN_FILE}")

import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/drive'
]

CLIENT_SECRET_FILE = Path("client_secret.json")
TOKEN_FILE = Path("token.pickle")

print("==================================================")
print("🔑 CONNECTING BOT TO 5TB GOOGLE DRIVE + YOUTUBE")
print("==================================================")
print("Opening your browser to link your 5TB Google Account...")

flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
creds = flow.run_local_server(port=0)

with open(TOKEN_FILE, 'wb') as token:
    pickle.dump(creds, token)

print("\n🎉 SUCCESS! Bot is now directly connected to your 5TB Google Drive!")
print("Scopes Granted:", creds.scopes)

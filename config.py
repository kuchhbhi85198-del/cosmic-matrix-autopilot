import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Assets & Output Directories
ASSETS_DIR = BASE_DIR / "assets"
SOURCE_VIDEOS_DIR = ASSETS_DIR / "source_videos"
OUTPUT_DIR = ASSETS_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

for d in [SOURCE_VIDEOS_DIR, OUTPUT_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Master Video Sources
SOURCE_VIDEOS = [
    {"id": "Hq5otSp5DCs", "url": "https://youtu.be/Hq5otSp5DCs", "topic": "The Mind Matrix & Frequency Tuning"},
    {"id": "OnIRUHEFiSs", "url": "https://youtu.be/OnIRUHEFiSs", "topic": "Is Reality Scripted & Cosmic Simulation"},
    {"id": "Ft-ZkvWwfUo", "url": "https://youtu.be/Ft-ZkvWwfUo", "topic": "Block Universe & Frozen Time Frames"}
]

# Video Dimensions (Ultra 4K Vertical 9:16)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 60

# Platform Activation Toggles
ENABLE_YOUTUBE = True
ENABLE_INSTAGRAM = False  # PAUSED on user request (Set to True to resume)
ENABLE_FACEBOOK = False
ENABLE_X_TWITTER = False
ENABLE_LINKEDIN = False

# Auth Credentials Files
INSTAGRAM_SESSION_FILE = BASE_DIR / "instagram_session.json"
YOUTUBE_CLIENT_SECRET = BASE_DIR / "client_secret.json"
YOUTUBE_TOKEN_PICKLE = BASE_DIR / "token.pickle"

# Social API Credentials (Loaded from .env)
X_API_KEY = os.getenv("X_API_KEY", "")
X_API_SECRET = os.getenv("X_API_SECRET", "")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN", "")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET", "")

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")

FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")

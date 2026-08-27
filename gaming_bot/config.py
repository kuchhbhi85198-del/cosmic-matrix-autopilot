import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
FONTS_DIR = ASSETS_DIR / "fonts"
RAW_VIDEOS_DIR = ASSETS_DIR / "raw_videos"
OUTPUT_DIR = ASSETS_DIR / "output"

# Ensure directories exist
for folder in [ASSETS_DIR, MUSIC_DIR, FONTS_DIR, RAW_VIDEOS_DIR, OUTPUT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
VIDEO_ASPECT_RATIO = "9:16"

# TTS Voices (Edge-TTS voices)
# English: "en-US-ChristopherNeural" (Deep Male), "en-US-GuyNeural", "en-US-JennyNeural"
# Hindi: "hi-IN-MadhurNeural" (Male), "hi-IN-SwaraNeural" (Female)
DEFAULT_VOICE_EN = "en-US-ChristopherNeural"
DEFAULT_VOICE_HI = "hi-IN-MadhurNeural"

# Subtitle Styling
DEFAULT_FONT_SIZE = 60
DEFAULT_FONT_COLOR = "&H0000FFFF"  # Yellow in ASS format
DEFAULT_STROKE_COLOR = "&H00000000" # Black in ASS format
DEFAULT_STROKE_WIDTH = 3

# YouTube Settings
YOUTUBE_CLIENT_SECRETS_FILE = BASE_DIR / "client_secret.json"
YOUTUBE_OAUTH_TOKEN_FILE = BASE_DIR / "token.pickle"

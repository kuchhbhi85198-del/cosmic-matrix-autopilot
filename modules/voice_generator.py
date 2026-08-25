import os
import requests
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger("VoiceGenerator")

class ElevenLabsVoiceEngine:
    def __init__(self):
        raw_keys = os.getenv("ELEVENLABS_API_KEYS", "")
        self.api_keys = [k.strip() for k in raw_keys.split(",") if k.strip()]
        self.current_key_idx = 0
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb") # George (Deep, Philosophical)
        self.model_id = "eleven_multilingual_v2"

    def get_current_key(self) -> str:
        if not self.api_keys:
            raise ValueError("No ElevenLabs API keys configured in .env!")
        return self.api_keys[self.current_key_idx % len(self.api_keys)]

    def rotate_key(self):
        if len(self.api_keys) > 1:
            self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
            logger.info(f"Rotated to ElevenLabs Key #{self.current_key_idx + 1}")

    def generate_speech(self, text: str, output_path: Path) -> Path:
        """
        Generates deep, emotional Hindi audio with automatic multi-key failover.
        """
        attempts = len(self.api_keys)
        for attempt in range(attempts):
            api_key = self.get_current_key()
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            payload = {
                "text": text,
                "model_id": self.model_id,
                "voice_settings": {
                    "stability": 0.40,
                    "similarity_boost": 0.85,
                    "style": 0.45,
                    "use_speaker_boost": True
                }
            }

            try:
                resp = requests.post(tts_url, json=payload, headers=headers, timeout=45)
                if resp.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(resp.content)
                    logger.info(f"Speech synthesized successfully using Key #{self.current_key_idx + 1} -> {output_path.name}")
                    return output_path
                else:
                    logger.warning(f"Key #{self.current_key_idx + 1} failed ({resp.status_code}): {resp.text}. Rotating key...")
                    self.rotate_key()
            except Exception as e:
                logger.error(f"Error on Key #{self.current_key_idx + 1}: {e}. Rotating key...")
                self.rotate_key()

        raise RuntimeError("All ElevenLabs API keys exhausted or failed!")

# Singleton instance
voice_engine = ElevenLabsVoiceEngine()

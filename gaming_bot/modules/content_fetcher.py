import random
from pathlib import Path
from config import RAW_VIDEOS_DIR

DESKTOP_NEW_FOLDER = Path(r"C:\Users\EDITI\OneDrive\Desktop\New folder")


class ContentFetcher:
    def __init__(self):
        pass

    def get_next_video(self) -> Path:
        """
        Picks a video from assets/raw_videos or Desktop folder.
        """
        # First priority: assets/raw_videos
        clips = list(RAW_VIDEOS_DIR.glob("*.mp4"))
        
        # Second priority: Desktop New folder
        if not clips and DESKTOP_NEW_FOLDER.exists():
            clips = list(DESKTOP_NEW_FOLDER.glob("*.mp4"))

        if clips:
            return random.choice(clips)

        return None


if __name__ == "__main__":
    fetcher = ContentFetcher()
    chosen = fetcher.get_next_video()
    print("Chosen clip:", chosen)

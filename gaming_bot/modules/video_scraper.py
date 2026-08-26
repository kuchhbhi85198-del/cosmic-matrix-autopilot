import json
import random
import subprocess
import shutil
import sys
from pathlib import Path
from config import BASE_DIR, RAW_VIDEOS_DIR

DOWNLOADS_DIR = RAW_VIDEOS_DIR / "scraped"
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
SCRAPED_LOG = BASE_DIR / "logs" / "scraped_ids.json"
SCRAPED_LOG.parent.mkdir(parents=True, exist_ok=True)
CLIPS_DIR = BASE_DIR / "assets" / "clips"
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

SEARCH_QUERIES = {
    "gta6": [
        "gta 6 ultra realistic graphics 4k 60fps gameplay",
        "gta 6 vice city hyper realistic driving moments",
        "gta 6 ray tracing graphics comparison 60fps",
        "gta 6 police chase insane physics moments 4k",
        "gta 6 supercar speed run vice city 60fps",
        "gta 6 next gen graphics mod gameplay 4k",
        "gta 5 ultra graphics mod photorealistic 4k 60fps",
        "gta 6 leak official gameplay showcase 60fps",
        "best gta 6 clips viral 4k 60fps",
        "gta 6 stunt driving vice city 4k"
    ]
}


class VideoScraper:
    """
    24/7 Autonomous Internet Scraper:
    1. Searches YouTube for fresh viral 4K/1080p gaming moments dynamically in the cloud.
    2. Enforces strict deduplication (never re-uses previously scraped videos).
    3. Seamlessly falls back to pre-cached offline clips if internet scraping is unavailable.
    """
    def __init__(self):
        self.downloaded_ids = self._load_downloaded_ids()
        self.yt_dlp_cmd = self._detect_ytdlp()

    def _detect_ytdlp(self) -> str:
        # Check system PATH first
        sys_ytdlp = shutil.which("yt-dlp")
        if sys_ytdlp:
            return sys_ytdlp
        
        # Check local venvs
        win_venv = BASE_DIR / ".venv" / "Scripts" / "yt-dlp.exe"
        if win_venv.exists():
            return str(win_venv)
        
        linux_venv = BASE_DIR / ".venv" / "bin" / "yt-dlp"
        if linux_venv.exists():
            return str(linux_venv)

        return sys.executable + " -m yt_dlp"

    def _load_downloaded_ids(self) -> set:
        if SCRAPED_LOG.exists():
            try:
                with open(SCRAPED_LOG, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except Exception:
                return set()
        return set()

    def _save_downloaded_id(self, vid_id: str):
        self.downloaded_ids.add(vid_id)
        with open(SCRAPED_LOG, "w", encoding="utf-8") as f:
            json.dump(list(self.downloaded_ids), f, indent=2)

    def _get_video_height(self, file_path: Path) -> int:
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=height",
                "-of", "csv=p=0",
                str(file_path)
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            return int(res.stdout.strip())
        except Exception:
            return 0

    def fetch_viral_clip(self, category: str = "gta6", max_retries: int = 3) -> Path:
        """
        Dynamically finds and scrapes fresh viral clips from the internet.
        """
        print(f"[*] [AUTONOMOUS SCRAPER] Searching internet for fresh viral {category.upper()} clips...")

        for attempt in range(max_retries):
            queries = SEARCH_QUERIES.get(category, SEARCH_QUERIES["gta6"])
            query = random.choice(queries)
            print(f"[*] [Scrape Attempt {attempt+1}/{max_retries}] Searching: '{query}'...")

            search_target = f"ytsearch20:{query}"
            cmd_search = [
                "yt-dlp",
                "--dump-json",
                "--flat-playlist",
                "--no-playlist",
                "--extractor-args", "youtube:player_client=android,web",
                search_target
            ]

            try:
                res = subprocess.run(cmd_search, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=35)
            except Exception:
                continue

            candidates = []
            for line in res.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    vid_id = data.get("id")
                    if vid_id and vid_id not in self.downloaded_ids:
                        candidates.append((vid_id, data.get("title", "")))
                except Exception:
                    continue

            if not candidates:
                continue

            # Pick a fresh unused video
            selected_id, selected_title = random.choice(candidates[:8])
            video_url = f"https://www.youtube.com/watch?v={selected_id}"
            target_file = DOWNLOADS_DIR / f"{category}_{selected_id}.mp4"

            print(f"[*] Found fresh viral video: '{selected_title}' ({selected_id})")
            print("[*] Downloading 15-second high-energy HD/4K segment...")

            cmd_download = [
                "yt-dlp",
                "-f", "bestvideo[height>=1080]+bestaudio/bestvideo[height>=720]+bestaudio/best[height>=720]/best",
                "--merge-output-format", "mp4",
                "--download-sections", "*15-30",
                "--force-overwrites",
                "--extractor-args", "youtube:player_client=android,web",
                "-o", str(target_file),
                video_url
            ]

            try:
                subprocess.run(cmd_download, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
                if target_file.exists() and target_file.stat().st_size > 1_000_000:
                    height = self._get_video_height(target_file)
                    if height >= 720:
                        self._save_downloaded_id(selected_id)
                        print(f"[SUCCESS] Scraped fresh {height}p footage: {target_file.name}")
                        return target_file
                    else:
                        target_file.unlink(missing_ok=True)
            except Exception:
                continue

        # Emergency Fallback to local cached clips library
        print("[!] Internet search yielded no new clips. Using pre-cached master safety library...")
        cached_clips = list(CLIPS_DIR.glob("*.mp4"))
        if cached_clips:
            unused = [c for c in cached_clips if c.name not in self.downloaded_ids]
            selected = random.choice(unused) if unused else random.choice(cached_clips)
            self._save_downloaded_id(selected.name)
            print(f"[SAFETY NET] Using master clip: {selected.name}")
            return selected

        return None


if __name__ == "__main__":
    scraper = VideoScraper()
    print("Autonomous Scraper initialized.")

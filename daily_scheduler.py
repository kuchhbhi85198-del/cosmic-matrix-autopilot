import argparse
import sys
import time
import schedule
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from autopilot import CosmicAutopilotEngine


def run_job(privacy: str = "public", slot_name: str = "Daily"):
    print(f"\n" + "=" * 65)
    print(f"⏰ [{slot_name.upper()} COSMIC MULTI-UPLOAD TRIGGERED] at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    engine = CosmicAutopilotEngine(privacy_status=privacy)
    engine.run_cycle()


def start_scheduler(morning_time: str = "09:00", evening_time: str = "18:00", privacy: str = "public", test_now: bool = False):
    print("=" * 65)
    print("🌌 24/7 COSMIC MATRIX 5-IN-1 SCHEDULER (2 POSTS EVERY DAY)")
    print("=" * 65)
    print(f"[*] Slot 1 (Morning): {morning_time} AM daily")
    print(f"[*] Slot 2 (Evening): {evening_time} (6:00 PM) daily")
    print(f"[*] Target Platforms: YouTube, Instagram, Facebook, X (Twitter), LinkedIn")
    print("=" * 65)

    if test_now:
        print("[*] Running 1 immediate test cycle...")
        run_job(privacy=privacy, slot_name="Immediate Test")

    schedule.every().day.at(morning_time).do(run_job, privacy=privacy, slot_name="Morning Post")
    schedule.every().day.at(evening_time).do(run_job, privacy=privacy, slot_name="Evening Post")

    print("\n[*] Waiting for scheduled slots... (Press Ctrl+C to stop)")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Matrix 24/7 Daily Multi-Platform Scheduler")
    parser.add_argument("--morning", type=str, default="09:00")
    parser.add_argument("--evening", type=str, default="18:00")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "private", "unlisted"])
    parser.add_argument("--test-now", action="store_true")

    args = parser.parse_args()
    start_scheduler(
        morning_time=args.morning,
        evening_time=args.evening,
        privacy=args.privacy,
        test_now=args.test_now
    )

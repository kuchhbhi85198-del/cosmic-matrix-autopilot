import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent


def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)


def run_bot(force: bool = False):
    log("[TRIGGER] Executing Cosmic Matrix Autopilot cycle...")
    try:
        cmd = [sys.executable, str(BASE_DIR / "autopilot.py"), "--privacy", "public"]
        if force:
            cmd.append("--force")
        res = subprocess.run(cmd, cwd=str(BASE_DIR), text=True)
        log(f"[FINISHED] Autopilot cycle finished with exit code: {res.returncode}")
    except Exception as e:
        log(f"[ERROR] Exception during autopilot execution: {e}")


def main():
    log("==========================================================")
    log("☁️ 24/7 DEDICATED CLOUD AUTOPILOT WORKER ONLINE (RENDER.COM)")
    log("==========================================================")
    log("Scheduled publishing slots:")
    log("  - Morning Slot: 09:00 AM IST (03:30 UTC)")
    log("  - Evening Slot: 06:00 PM IST (12:30 UTC)")

    last_slot = None

    while True:
        try:
            now = datetime.now()
            # Calculate IST Hour & Minute
            # If server is in UTC, add 5 hours 30 mins
            utc_ts = datetime.utcnow()
            ist_minutes_total = utc_ts.hour * 60 + utc_ts.minute + 330
            ist_hour = (ist_minutes_total // 60) % 24
            ist_min = ist_minutes_total % 60
            today_str = datetime.now().strftime("%Y-%m-%d")

            # Morning Slot Trigger (09:00 - 09:05 IST)
            if ist_hour == 9 and 0 <= ist_min <= 5:
                slot_key = f"{today_str}_morning"
                if last_slot != slot_key:
                    log(f"[CRON] ⏰ 09:00 AM IST Morning Slot Triggered!")
                    run_bot(force=False)
                    last_slot = slot_key

            # Evening Slot Trigger (18:00 - 18:05 IST)
            elif ist_hour == 18 and 0 <= ist_min <= 5:
                slot_key = f"{today_str}_evening"
                if last_slot != slot_key:
                    log(f"[CRON] ⏰ 06:00 PM IST Evening Slot Triggered!")
                    run_bot(force=False)
                    last_slot = slot_key

        except Exception as e:
            log(f"[LOOP ERROR] {e}")

        time.sleep(30)


if __name__ == "__main__":
    main()

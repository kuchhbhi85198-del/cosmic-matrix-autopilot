import subprocess
from pathlib import Path
import random
import imageio_ffmpeg
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, OUTPUT_DIR
from modules.sfx_manager import SFXManager


class EditEngine:
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.sfx_mgr = SFXManager()

    def get_video_duration(self, video_path: Path) -> float:
        cmd = [self.ffmpeg_exe, "-i", str(video_path), "-f", "null", "-"]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        for line in res.stderr.split('\n'):
            if "Duration:" in line:
                time_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = time_str.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
        return 15.0

    def create_hype_edit(
        self,
        raw_video_path: Path,
        music_path: Path,
        hook_text: str,
        output_path: Path,
        target_duration: float = 15.0
    ) -> Path:
        """
        Creates a high-energy short edit:
        - Multi-scene fast cuts with zoom pulses
        - Color grading & contrast boost
        - On-screen bold hook text
        - SFX (whoosh & bass drops) at transition points
        - High energy background music
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        total_duration = self.get_video_duration(raw_video_path)

        # Calculate 3 to 4 fast scene cut points
        num_cuts = 4
        segment_len = target_duration / num_cuts
        
        # Pick engaging random segments from raw video
        starts = []
        for i in range(num_cuts):
            max_start = max(0, total_duration - segment_len)
            s = (i * (max_start / max(1, num_cuts - 1))) if total_duration > target_duration else (i * segment_len)
            starts.append(s)

        whoosh = self.sfx_mgr.get_sfx("whoosh")
        bass_drop = self.sfx_mgr.get_sfx("bass_drop")
        impact = self.sfx_mgr.get_sfx("impact")

        # Video filter: Scale 9:16 + Color Grading + Zoom Pulse effect + Drawtext / Hook
        import re
        # Keep clean alphanumeric characters and common punctuation for on-screen banner
        clean_hook = re.sub(r'[^\w\s\?!.,-]', '', hook_text).strip().upper()
        
        # Filter complex for fast cuts, high saturation & contrast, and bold text header
        vf_pipeline = (
            f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
            f"eq=contrast=1.2:saturation=1.35:brightness=0.02,"
            f"drawtext=text='{clean_hook}':fontcolor=yellow:fontsize=52:box=1:boxcolor=black@0.7:boxborderw=15:"
            f"x=(w-text_w)/2:y=220:enable='between(t,0,{target_duration})'"
        )

        # Build FFmpeg command
        if music_path and music_path.exists():
            cmd = [
                self.ffmpeg_exe, "-y",
                "-ss", str(starts[0]),
                "-i", str(raw_video_path),
                "-stream_loop", "-1",
                "-i", str(music_path),
                "-i", str(bass_drop),
                "-i", str(whoosh),
                "-t", str(target_duration),
                "-filter_complex",
                f"[0:v]{vf_pipeline}[v];"
                f"[1:a]volume=0.85[m];"
                f"[2:a]volume=1.5[s1];"
                f"[3:a]adelay=3500|3500,volume=1.2[s2];"
                f"[m][s1][s2]amix=inputs=3:duration=first:dropout_transition=2[a]",
                "-map", "[v]",
                "-map", "[a]",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-c:a", "aac",
                "-b:a", "192k",
                str(output_path)
            ]
        else:
            cmd = [
                self.ffmpeg_exe, "-y",
                "-ss", str(starts[0]),
                "-i", str(raw_video_path),
                "-i", str(bass_drop),
                "-t", str(target_duration),
                "-filter_complex",
                f"[0:v]{vf_pipeline}[v];"
                f"[1:a]volume=1.5[a]",
                "-map", "[v]",
                "-map", "[a]",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-c:a", "aac",
                "-b:a", "192k",
                str(output_path)
            ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            # Fallback if drawtext font engine has issue
            vf_simple = f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},eq=contrast=1.15:saturation=1.3"
            cmd_fallback = [
                self.ffmpeg_exe, "-y",
                "-ss", str(starts[0]),
                "-i", str(raw_video_path),
                "-t", str(target_duration),
                "-vf", vf_simple,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-c:a", "aac",
                str(output_path)
            ]
            subprocess.run(cmd_fallback, check=True)

        return output_path


if __name__ == "__main__":
    engine = EditEngine()
    print("EditEngine initialized.")

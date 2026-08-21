import re
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import imageio_ffmpeg
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, OUTPUT_DIR


class CinematicEditor:
    """
    Cosmic Matrix 9:16 Ultra 4K 60FPS Cinematic Editor:
    - Ambient Cosmic Blur-Pad background
    - Crisp centered high-definition foreground
    - Golden/Cyan Neon Hook Badge + Glowing Progress Bar
    - Mastered high-clarity voice audio
    """
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def render_cosmic_short(self, raw_clip_path: Path, hook_text: str, output_path: Path, duration: float) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        clean_hook = re.sub(r'[^\w\s\?!.,-]', '', hook_text).strip().upper()
        if not clean_hook:
            clean_hook = "THE COSMIC MATRIX"

        # 9:16 Cinematic Canvas Pipeline
        vf_pipeline = (
            f"[0:v]split=2[v_bg][v_fg];"
            f"[v_bg]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
            f"boxblur=24:12,eq=brightness=-0.35:contrast=1.2,fps=60[bg];"
            f"[v_fg]scale={VIDEO_WIDTH}:-2,"
            f"unsharp=5:5:1.1:5:5:0.5,"
            f"eq=contrast=1.2:saturation=1.25,fps=60[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"
            f"[base]drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{clean_hook}':fontcolor=yellow:fontsize=46:box=1:boxcolor=black@0.85:boxborderw=16:"
            f"x=(w-text_w)/2:y=240:enable='between(t,0,{duration})'[with_top];"
            f"[with_top]drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='DEEP REALITY DECODED...':fontcolor=white:fontsize=32:box=1:boxcolor=red@0.85:boxborderw=10:"
            f"x=(w-text_w)/2:y=h-240:enable='between(t,0,{duration})'[with_bot];"
            f"[with_bot]drawbox=x=0:y=h-14:w='w*(t/{duration})':h=14:color=yellow@1.0:t=fill[v]"
        )

        cmd = [
            self.ffmpeg_exe, "-y",
            "-i", str(raw_clip_path),
            "-t", str(duration),
            "-filter_complex", vf_pipeline,
            "-map", "[v]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "16",
            "-b:v", "18M",
            "-maxrate", "25M",
            "-bufsize", "40M",
            "-pix_fmt", "yuv420p",
            "-r", "60",
            "-c:a", "aac",
            "-b:a", "320k",
            str(output_path)
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"[!] Rendering fallback: {res.stderr[:200]}")
            # Fallback simple scale
            cmd_fb = [
                self.ffmpeg_exe, "-y",
                "-i", str(raw_clip_path),
                "-t", str(duration),
                "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},unsharp=5:5:1.0,fps=60",
                "-c:v", "libx264",
                "-crf", "17",
                "-b:v", "15M",
                "-c:a", "aac",
                "-b:a", "256k",
                str(output_path)
            ]
            subprocess.run(cmd_fb, check=True)

        return output_path


if __name__ == "__main__":
    editor = CinematicEditor()
    print("Cinematic Editor ready.")

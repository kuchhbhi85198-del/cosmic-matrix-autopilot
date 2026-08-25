import re
import sys
import subprocess
from pathlib import Path
import imageio_ffmpeg

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, OUTPUT_DIR


def get_system_font() -> str:
    """Returns accessible bold font path across Windows and Linux."""
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf"),
        Path("C:/Windows/Fonts/seguiemj.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf")
    ]
    for c in candidates:
        if c.exists():
            return str(c).replace("\\", "/").replace(":", "\\:")
    return ""


class CinematicEditor:
    """
    Cosmic Matrix 9:16 Ultra 4K 60FPS Cinematic Editor:
    - Ambient Cosmic Blur-Pad background with dark aesthetic
    - Crystal-Clear 1080p Full HD centered foreground (Lanczos scaling + Sharpening)
    - Golden Neon Hook Badge + Glowing Bottom Border
    - Mastered studio audio (320 kbps AAC)
    """
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.font_path = get_system_font()

    def render_cosmic_short(self, raw_clip_path: Path, hook_text: str, output_path: Path, duration: float) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        clean_hook = re.sub(r'[^\w\s\?!.,-]', '', hook_text).strip().upper()
        if not clean_hook:
            clean_hook = "THE COSMIC MATRIX"

        font_arg = f":fontfile='{self.font_path}'" if self.font_path else ""

        vf_pipeline = (
            f"[0:v]split=2[v_bg][v_fg];"
            f"[v_bg]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:flags=lanczos:force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
            f"boxblur=22:11,eq=brightness=-0.30:contrast=1.15,fps=60[bg];"
            f"[v_fg]scale={VIDEO_WIDTH}:-2:flags=lanczos,"
            f"unsharp=5:5:1.2:5:5:0.6,"
            f"eq=contrast=1.15:saturation=1.20,fps=60[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"
            f"[base]drawtext=text='{clean_hook}'{font_arg}:fontcolor=yellow:fontsize=46:box=1:boxcolor=black@0.85:boxborderw=16:"
            f"x=(w-text_w)/2:y=240:enable='between(t,0,{duration})'[with_top];"
            f"[with_top]drawtext=text='DEEP REALITY DECODED...'{font_arg}:fontcolor=white:fontsize=32:box=1:boxcolor=red@0.85:boxborderw=10:"
            f"x=(w-text_w)/2:y=h-240:enable='between(t,0,{duration})'[with_bot];"
            f"[with_bot]drawbox=x=0:y=ih-16:w=iw:h=16:color=yellow@0.9:t=fill[v]"
        )

        cmd = [
            self.ffmpeg_exe, "-y",
            "-i", str(raw_clip_path),
            "-t", str(duration),
            "-filter_complex", vf_pipeline,
            "-map", "[v]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "14",
            "-b:v", "22M",
            "-maxrate", "30M",
            "-bufsize", "50M",
            "-pix_fmt", "yuv420p",
            "-r", "60",
            "-c:a", "aac",
            "-b:a", "320k",
            str(output_path)
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"[!] Primary render failed: {res.stderr[:200]}")
            vf_fb = (
                f"[0:v]split=2[v_bg][v_fg];"
                f"[v_bg]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:flags=lanczos:force_original_aspect_ratio=increase,"
                f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
                f"boxblur=22:11,eq=brightness=-0.30,fps=60[bg];"
                f"[v_fg]scale={VIDEO_WIDTH}:-2:flags=lanczos,unsharp=5:5:1.2,fps=60[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,drawbox=x=0:y=ih-16:w=iw:h=16:color=yellow@0.9:t=fill"
            )
            cmd_fb = [
                self.ffmpeg_exe, "-y",
                "-i", str(raw_clip_path),
                "-t", str(duration),
                "-filter_complex", vf_fb,
                "-map", "0:a",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "15",
                "-b:v", "20M",
                "-pix_fmt", "yuv420p",
                "-r", "60",
                "-c:a", "aac",
                "-b:a", "320k",
                str(output_path)
            ]
            subprocess.run(cmd_fb, check=True)

        return output_path


if __name__ == "__main__":
    editor = CinematicEditor()
    print(f"Cinematic Editor ready. Font: {editor.font_path}")

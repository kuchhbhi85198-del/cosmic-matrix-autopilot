import subprocess
from pathlib import Path
import imageio_ffmpeg
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, RAW_VIDEOS_DIR


class VideoEngine:
    def __init__(self):
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def get_background_clip(self, preferred_path: Path = None) -> Path:
        """
        Returns a background clip from assets/raw_videos or the specified path.
        """
        if preferred_path and preferred_path.exists():
            return preferred_path
        
        # Check raw_videos directory
        video_files = list(RAW_VIDEOS_DIR.glob("*.mp4"))
        if video_files:
            return video_files[0]
            
        return None

    def create_placeholder_background(self, duration: float, output_path: Path) -> Path:
        """
        Generates a stylish dark gaming background with animated gradient if no raw video is found.
        """
        cmd = [
            self.ffmpeg_exe,
            "-y",
            "-f", "lavfi",
            "-i", f"mptestsrc=rate={VIDEO_FPS}:duration={duration}:size={VIDEO_WIDTH}x{VIDEO_HEIGHT}",
            "-vf", "eq=contrast=1.3:brightness=-0.2:saturation=1.5,boxblur=10:5",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return output_path

    def prepare_vertical_video(self, input_video: Path, duration: float, output_path: Path) -> Path:
        """
        Crops/scales input video to 9:16 (1080x1920) and loops/trims it to match required duration.
        """
        filter_complex = (
            f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
            f"fps={VIDEO_FPS},format=yuv420p[v]"
        )

        cmd = [
            self.ffmpeg_exe,
            "-y",
            "-stream_loop", "-1",
            "-i", str(input_video),
            "-t", str(duration),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-c:v", "libx264",
            "-preset", "fast",
            str(output_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg error preparing video: {res.stderr}")
            
        return output_path


if __name__ == "__main__":
    v_engine = VideoEngine()
    print("VideoEngine initialized. FFmpeg path:", v_engine.ffmpeg_exe)

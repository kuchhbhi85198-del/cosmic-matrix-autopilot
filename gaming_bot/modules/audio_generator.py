import asyncio
from pathlib import Path
import edge_tts
from config import DEFAULT_VOICE_EN, DEFAULT_VOICE_HI, OUTPUT_DIR


class AudioGenerator:
    def __init__(self, voice: str = None):
        self.voice = voice

    async def generate_audio_async(self, text: str, output_path: Path, vtt_path: Path = None, voice: str = None) -> Path:
        """
        Generates audio file and optionally VTT subtitle timings using edge-tts.
        """
        selected_voice = voice or self.voice or DEFAULT_VOICE_HI
        communicate = edge_tts.Communicate(text, selected_voice)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if vtt_path:
            vtt_path.parent.mkdir(parents=True, exist_ok=True)
            submaker = edge_tts.SubMaker()
            with open(output_path, "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        submaker.feed(chunk)
            
            with open(vtt_path, "w", encoding="utf-8") as file:
                file.write(submaker.get_srt())
        else:
            await communicate.save(str(output_path))
            
        return output_path

    def generate_audio(self, text: str, output_path: Path, vtt_path: Path = None, voice: str = None) -> Path:
        """Synchronous wrapper for generate_audio_async."""
        return asyncio.run(self.generate_audio_async(text, output_path, vtt_path, voice))


if __name__ == "__main__":
    audio_gen = AudioGenerator()
    out = OUTPUT_DIR / "test_voice.mp3"
    srt_out = OUTPUT_DIR / "test_subs.srt"
    test_text = "GTA 6 ke bare me ye secret leaks aapko kisi ne nahi bataye!"
    audio_gen.generate_audio(test_text, out, srt_out, DEFAULT_VOICE_HI)
    print(f"Generated test audio at {out} and subs at {srt_out}")

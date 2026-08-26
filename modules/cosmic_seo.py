import random
from typing import Dict, Any
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


class CosmicSEO:
    """
    Supercharged High-Retention Viral Cosmic SEO Engine:
    - High-CTR English/Hinglish Titles with Intriguing Emojis & Search Hooks
    - Algorithmic Search Tags for YouTube Shorts & Instagram Explore
    - Direct Traffic Funnel from LinkedIn & X to YouTube Channel
    """

    YT_TAGS_POOL = [
        "mind matrix", "quantum physics in hindi", "reality of universe in hindi",
        "frequency and vibration hindi", "how brain filters reality", "simulation theory hindi",
        "block universe theory", "observer effect in hindi", "multiverse theory in hindi",
        "holographic universe", "nikola tesla 369 secret", "illusion of time hindi",
        "consciousness hindi", "parallel universe facts", "space secrets hindi",
        "astrophysics facts", "quantum entanglement hindi", "matrix glitch",
        "science facts in hindi", "cosmic mysteries"
    ]

    INSTA_TAGS_POOL = [
        "#mindmatrix", "#quantumphysics", "#simulationtheory", "#cosmicsecrets",
        "#universefacts", "#frequency", "#vibration", "#illusionoftime",
        "#reelsinstagram", "#explorepage", "#viralreels", "#blockuniverse",
        "#multiverse", "#sciencefacts", "#space", "#deepfacts",
        "#quantummechanics", "#trendingreels", "#fyp"
    ]

    def generate_all(self, hook: str, topic: str, youtube_url: str = "") -> Dict[str, Any]:
        # 1. YouTube Shorts Metadata (High-CTR English/Hinglish Title)
        yt_tags = random.sample(self.YT_TAGS_POOL, k=min(15, len(self.YT_TAGS_POOL)))
        yt_title = f"{hook} 🌌 #shorts #mindmatrix #quantum #viral"[:100]
        yt_description = (
            f"🌌 {hook}\n\n"
            f"🧠 Concept: {topic}\n\n"
            f"Exploring the deepest mysteries of quantum mechanics, block universe theory, and cosmic reality.\n\n"
            f"🔔 Subscribe to our channel for daily mind-bending science facts!\n"
            f"💬 Drop a comment with your thoughts!\n\n"
            f"📌 Trending Tags:\n{', '.join(yt_tags)}"
        )

        # 2. Instagram Reels Metadata (Viral Explore Ranker)
        insta_tags = random.sample(self.INSTA_TAGS_POOL, k=min(14, len(self.INSTA_TAGS_POOL)))
        insta_caption = (
            f"🌌 {hook}\n\n"
            f"🧠 Did you know? Exploring {topic} will completely shift how you perceive reality!\n\n"
            f"👉 Follow @rathour_vibe_ for daily mind-blowing science reels! 🚀\n"
            f"💬 Tell us in the comments: What do you think?\n\n"
            f"{' '.join(insta_tags)}"
        )

        # 3. Facebook Post/Reels Metadata (With YouTube Video Link)
        yt_link_line = f"\n\n🎬 Watch Full HD Video on YouTube: {youtube_url}" if youtube_url else ""
        fb_caption = (
            f"🌌 {hook}\n\n"
            f"The deepest secret of the quantum universe: {topic}!"
            f"{yt_link_line}\n\n"
            f"Share this with someone who loves deep science & space secrets! 🚀\n"
            f"#Universe #QuantumPhysics #MindMatrix #ScienceFacts #Viral"
        )

        # 4. X (Twitter) Post Metadata (With Direct YouTube Funnel Link)
        yt_short_link = f"\n\n🎬 Watch Video on YouTube: {youtube_url}" if youtube_url else ""
        x_post = (
            f"🌌 {hook}\n\n"
            f"Exploring {topic} and the quantum nature of reality."
            f"{yt_short_link}\n\n"
            f"#QuantumPhysics #Universe #Science #MindMatrix"
        )[:280]

        # 5. LinkedIn Post Metadata (Professional Analysis + Direct YouTube Traffic Callout)
        yt_li_line = f"\n\n🎬 Watch Full 4K Video on YouTube: {youtube_url}\n🔔 Subscribe to our YouTube Channel for daily scientific insights!" if youtube_url else ""
        linkedin_post = (
            f"🌌 The Science of Reality: {hook}\n\n"
            f"Recent breakthroughs in theoretical physics and neuroscience highlight a fascinating principle: {topic}.\n\n"
            f"Key Takeaways:\n"
            f"• Perception is an active construction of electrical neural data.\n"
            f"• Quantum mechanics demonstrates the observer's pivotal role in shaping state."
            f"{yt_li_line}\n\n"
            f"#Neuroscience #QuantumMechanics #Science #Consciousness #DeepThinking"
        )

        return {
            "hook": hook,
            "topic": topic,
            "youtube": {
                "title": yt_title,
                "description": yt_description,
                "tags": yt_tags
            },
            "instagram": {
                "caption": insta_caption,
                "hashtags": insta_tags
            },
            "facebook": {
                "caption": fb_caption
            },
            "x_twitter": {
                "text": x_post
            },
            "linkedin": {
                "text": linkedin_post
            }
        }


if __name__ == "__main__":
    seo = CosmicSEO()
    meta = seo.generate_all("Brain Is Just a TV Receiver! 📺", "Brain as Receiver", "https://youtu.be/PJjhnxWTBQY")
    print("Supercharged English Title:", meta["youtube"]["title"])
    print("YT Tags count:", len(meta["youtube"]["tags"]))

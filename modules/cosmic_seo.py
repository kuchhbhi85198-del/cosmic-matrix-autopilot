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
    Clean, Pure Science & High-Retention SEO Metadata Engine:
    - High-CTR Golden Titles & Captions
    - Pure Science / Deep Universe Explanations (Zero Book / Zero Sales links)
    - Platform-specific algorithmic tags for YouTube, Instagram, Facebook, X, and LinkedIn.
    """

    YT_TAGS_POOL = [
        "mind matrix", "quantum physics in hindi", "reality of universe in hindi",
        "frequency and vibration hindi", "how brain filters reality", "simulation theory hindi",
        "block universe theory", "observer effect in hindi", "multiverse theory",
        "holographic universe", "nikola tesla 369", "illusion of time",
        "consciousness hindi", "parallel universe", "space facts hindi"
    ]

    INSTA_TAGS_POOL = [
        "#mindmatrix", "#quantumphysics", "#simulationtheory", "#cosmicsecrets",
        "#universefacts", "#frequency", "#vibration", "#illusionoftime",
        "#reelsinstagram", "#explorepage", "#viralreels", "#blockuniverse",
        "#multiverse", "#sciencefacts", "#space"
    ]

    def generate_all(self, hook: str, topic: str) -> Dict[str, Any]:
        # 1. YouTube Shorts Metadata (Clean & Focused)
        yt_tags = random.sample(self.YT_TAGS_POOL, k=min(12, len(self.YT_TAGS_POOL)))
        yt_title = f"{hook} 🌌 #shorts #mindmatrix #universe"[:100]
        yt_description = (
            f"🌌 {hook}\n\n"
            f"🧠 विषय (Deep Concept): {topic}\n\n"
            f"क्वांटम फिजिक्स, ब्लॉक यूनिवर्स और चेतना के अनसुलझे वैज्ञानिक रहस्यों का गहन विश्लेषण।\n\n"
            f"🔔 रोज़ाना ऐसे ही गहरे वैज्ञानिक तथ्यों के लिए चैनल को सब्सक्राइब करें!\n\n"
            f"📌 Tags:\n{', '.join(yt_tags)}"
        )

        # 2. Instagram Reels Metadata (Clean & Engaging)
        insta_tags = random.sample(self.INSTA_TAGS_POOL, k=min(12, len(self.INSTA_TAGS_POOL)))
        insta_caption = (
            f"🌌 {hook}\n\n"
            f"🧠 क्या आप जानते हैं? {topic} का यह वैज्ञानिक सिद्धांत आपकी सोच को पूरी तरह बदल देगा!\n\n"
            f"👉 ऐसी और भी माइंड-ब्लोइंग रील्स के लिए फॉलो करें: @rathour_vibe_\n"
            f"💬 कमेंट में बताएं अपनी राय!\n\n"
            f"{' '.join(insta_tags)}"
        )

        # 3. Facebook Post/Reels Metadata
        fb_caption = (
            f"🌌 {hook}\n\n"
            f"विज्ञान और ब्रह्मांड का सबसे बड़ा रहस्य: {topic}!\n"
            f"क्या हमारी भौतिक वास्तविकता सच में वही है जो हमें दिखाई देती है?\n\n"
            f"Share this with someone who loves deep science & universe secrets! 🚀\n"
            f"#Universe #QuantumPhysics #MindMatrix #ScienceFacts"
        )

        # 4. X (Twitter) Post Metadata
        x_post = (
            f"🌌 {hook}\n\n"
            f"What if reality isn't what it seems? Exploring {topic} and the quantum universe.\n\n"
            f"#QuantumPhysics #Matrix #Universe #Science"
        )[:280]

        # 5. LinkedIn Post Metadata
        linkedin_post = (
            f"🌌 The Science of Reality: {hook}\n\n"
            f"Recent breakthroughs in theoretical physics and neuroscience highlight a fascinating principle: {topic}.\n\n"
            f"Key Takeaways:\n"
            f"• Perception is an active construction of electrical neural data.\n"
            f"• Quantum mechanics demonstrates the observer's pivotal role in shaping state.\n\n"
            f"#Neuroscience #QuantumMechanics #Science #Consciousness"
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
    meta = seo.generate_all("दिमाग एक टीवी जैसा रिसीवर है! 📺", "Brain as Receiver")
    print("Clean YT Description Preview:\n", meta["youtube"]["description"])
    print("\nClean Insta Caption Preview:\n", meta["instagram"]["caption"])

import random
from typing import Dict, Any
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (
    BUY_ME_A_COFFEE_URL,
    EBOOK_DOWNLOAD_URL,
    TOPMATE_CONSULT_URL,
    VIP_COMMUNITY_URL
)


class CosmicSEO:
    """
    Advanced Multi-Platform Viral SEO & Monetization Funnel Engine:
    - High-CTR Golden Titles & Descriptions
    - Embedded Monetization (E-Book, Buy Me a Coffee / Topmate, VIP Community)
    - Platform-specific algorithmic tags for YouTube, Instagram, Facebook, X, and LinkedIn.
    """

    YT_TAGS_POOL = [
        "mind matrix", "quantum physics in hindi", "reality of universe in hindi",
        "frequency and vibration hindi", "how brain filters reality", "spiritual awakening hindi",
        "simulation theory hindi", "block universe theory", "observer effect in hindi",
        "multiverse theory", "holographic universe", "nikola tesla 369", "illusion of time",
        "consciousness hindi", "maya matrix", "parallel universe"
    ]

    INSTA_TAGS_POOL = [
        "#mindmatrix", "#quantumphysics", "#simulationtheory", "#cosmicsecrets",
        "#universefacts", "#spiritualawakening", "#frequency", "#vibration",
        "#illusionoftime", "#reelsinstagram", "#explorepage", "#viralreels",
        "#blockuniverse", "#multiverse", "#consciousness"
    ]

    def generate_all(self, hook: str, topic: str) -> Dict[str, Any]:
        # 1. YouTube Shorts Metadata
        yt_tags = random.sample(self.YT_TAGS_POOL, k=min(12, len(self.YT_TAGS_POOL)))
        yt_title = f"{hook} 🌌 #shorts #mindmatrix #universe"[:100]
        yt_description = (
            f"🌌 {hook}\n\n"
            f"🧠 Deep Truth: {topic}\n"
            f"Decode the hidden secrets of Quantum Physics, Block Universe, and Consciousness.\n\n"
            f"📥 [DOWNLOAD] The Cosmic Matrix Code Secret Blueprint:\n👉 {EBOOK_DOWNLOAD_URL}\n\n"
            f"☕ [SUPPORT US] Support the Cosmic Research on Buy Me a Coffee:\n👉 {BUY_ME_A_COFFEE_URL}\n\n"
            f"🔮 [VIP GROUP] Join our Official Cosmic Tribe:\n👉 {VIP_COMMUNITY_URL}\n\n"
            f"🔔 SUBSCRIBE for daily mind-bending cosmic truths!\n\n"
            f"📌 Tags:\n{', '.join(yt_tags)}"
        )

        # 2. Instagram Reels Metadata
        insta_tags = random.sample(self.INSTA_TAGS_POOL, k=min(12, len(self.INSTA_TAGS_POOL)))
        insta_caption = (
            f"🌌 {hook}\n\n"
            f"🧠 क्या आप जानते हैं? {topic} का यह रहस्य आपकी सोच बदल देगा!\n\n"
            f"📖 'The Cosmic Matrix Code' सीक्रेट गाइड डाउनलोड करने के लिए बायो में दिए गए लिंक पर क्लिक करें! 📥\n"
            f"☕ हमारे काम को सपोर्ट करने के लिए बायो में Buy Me a Coffee लिंक देखें।\n\n"
            f"👉 Follow @rathour_vibe_ for daily deep cosmic reels!\n"
            f"💬 Comment 'COSMIC' to unlock reality.\n\n"
            f"{' '.join(insta_tags)}"
        )

        # 3. Facebook Post/Reels Metadata
        fb_caption = (
            f"🌌 {hook}\n\n"
            f"विज्ञान और ब्रह्मांड का सबसे बड़ा रहस्य: {topic}!\n"
            f"क्या हमारी वास्तविकता सच में वही है जो हमें दिखाई देती है या यह दिमाग का एक भ्रम है?\n\n"
            f"📥 पूरी रिसर्च ई-बुक डाउनलोड करें: {EBOOK_DOWNLOAD_URL}\n"
            f"☕ सपोर्ट करें: {BUY_ME_A_COFFEE_URL}\n\n"
            f"Share this with someone who loves deep science & universe secrets! 🚀\n"
            f"#Universe #QuantumPhysics #MindMatrix #ScienceFacts"
        )

        # 4. X (Twitter) Post Metadata
        x_post = (
            f"🌌 {hook}\n\n"
            f"What if reality isn't what it seems? Quantum Physics & The {topic} revealed.\n\n"
            f"📥 Download the full Cosmic Blueprint: {EBOOK_DOWNLOAD_URL}\n"
            f"☕ Support us: {BUY_ME_A_COFFEE_URL}\n\n"
            f"#QuantumPhysics #Matrix #Universe #Consciousness"
        )[:280]

        # 5. LinkedIn Post Metadata
        linkedin_post = (
            f"🌌 The Science of Perception: {hook}\n\n"
            f"Recent breakthroughs in theoretical physics and neuroscience highlight a fascinating principle: {topic}.\n\n"
            f"How does our brain filter reality, and how does internal state dictate external perception?\n\n"
            f"Key Takeaways:\n"
            f"• Perception is an active construction, not passive observation.\n"
            f"• Quantum mechanics demonstrates the observer's pivotal role in shaping state.\n\n"
            f"📖 Read our comprehensive whitepaper & guide: {EBOOK_DOWNLOAD_URL}\n\n"
            f"#Neuroscience #QuantumMechanics #PhilosophyOfMind #Consciousness #DeepThinking"
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
    print("YT Description Preview:\n", meta["youtube"]["description"])

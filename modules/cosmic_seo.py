import random
from typing import Dict, Any


class CosmicSEO:
    """
    Advanced Multi-Platform Viral SEO for Cosmic, Quantum & Reality Content.
    Generates custom metadata tailored for YouTube, Instagram, Facebook, X, and LinkedIn.
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
            f"🔔 SUBSCRIBE for daily mind-bending cosmic truths!\n\n"
            f"📌 Tags:\n{', '.join(yt_tags)}"
        )

        # 2. Instagram Reels Metadata
        insta_tags = random.sample(self.INSTA_TAGS_POOL, k=min(12, len(self.INSTA_TAGS_POOL)))
        insta_caption = (
            f"🌌 {hook}\n\n"
            f"🧠 क्या आप जानते हैं? {topic} का यह रहस्य आपकी सोच बदल देगा!\n\n"
            f"👉 Follow for daily cosmic & quantum reality reels!\n"
            f"💬 Comment your thoughts below!\n\n"
            f"{' '.join(insta_tags)}"
        )

        # 3. Facebook Post/Reels Metadata
        fb_caption = (
            f"🌌 {hook}\n\n"
            f"विज्ञान और ब्रह्मांड का सबसे बड़ा रहस्य: {topic}!\n"
            f"क्या हमारी वास्तविकता सच में वही है जो हमें दिखाई देती है या यह दिमाग का एक भ्रम है?\n\n"
            f"Share this with someone who loves deep science & universe secrets! 🚀\n"
            f"#Universe #QuantumPhysics #MindMatrix #ScienceFacts"
        )

        # 4. X (Twitter) Post Metadata
        x_post = (
            f"🌌 {hook}\n\n"
            f"What if reality isn't what it seems? Quantum Physics & The {topic} revealed.\n\n"
            f"Are we living in a cosmic simulation? 🧵👇\n"
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
            f"What are your perspectives on human consciousness and reality models?\n\n"
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
    meta = seo.generate_all("शरीर सिर्फ एक सिग्नल रिसीवर है!", "Brain as Receiver")
    print("YT Title:", meta["youtube"]["title"])
    print("\nX Post:\n", meta["x_twitter"]["text"])
    print("\nLinkedIn Post:\n", meta["linkedin"]["text"])

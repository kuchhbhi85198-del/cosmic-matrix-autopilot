import random
from typing import Dict, List


class SEOEngine:
    """
    Supercharged Viral Gaming SEO Engine for GTA 6, BGMI, and Esports:
    - High-CTR Golden Thumbnails / Titles
    - Top Algorithmic Ranking Hashtags for YouTube Shorts & Instagram Explore
    - 4K 60FPS High-Bitrate SEO Optimization
    """

    HOOK_TEMPLATES = {
        "gta6": [
            "GTA 6 Next-Gen Graphics Look UNREAL! 🤯 4K",
            "Rockstar Games Secret Physics in GTA 6! ⚡",
            "Wait For The Impossible Drift... GTA 6! 🔥",
            "This GTA 6 Stunt Broke The Internet! 💀",
            "GTA 6 Ultra-Realistic Water & Car Physics! 🌊",
            "Only 1% Gamers Know This GTA 6 Secret! 🏎️",
            "GTA 6 vs Real Life: Can You Tell The Difference? 😱"
        ],
        "bgmi": [
            "1v4 God Level BGMI Clutch in 4K! 🔥",
            "Impossible AWM Headshot Through Smoke! 🎯",
            "BGMI Pro Player Reflexes in Ultra HD! ⚡",
            "This 1v4 Rush Moment Is Insane! 💀",
            "Jonathan Level Recoil Control in BGMI! 🏆",
            "Only 0.1% Players Can Survive This Hot-Drop! 😱"
        ],
        "gaming": [
            "Top 1% Clutch Moment in Esports! 🎯",
            "Wait Till The End... Insane Gaming Reflexes! 🚨",
            "Unbelievable 1v5 Clutch in 4K 60FPS! ⚡"
        ]
    }

    TAGS_BY_CATEGORY = {
        "gta6": [
            "GTA 6", "GTA VI", "GTA 6 Gameplay", "GTA 6 Leaks", "Rockstar Games",
            "GTA 6 Graphics", "GTA 6 Trailer", "PS5 Gameplay", "4K Gaming",
            "Gaming Shorts", "GTA 6 Cars", "GTA 6 Map", "Best Gaming Clips",
            "Gaming Montage", "Viral Shorts", "Trending Gaming", "GTA 6 2026"
        ],
        "bgmi": [
            "BGMI", "BGMI Shorts", "BGMI Clutch", "BGMI 1v4", "BGMI Montage",
            "PUBG Mobile", "BGMI Highlights", "God Level Gameplay", "Jonathan Gaming",
            "Mortal", "Scout", "BGMI Viral", "Gaming Shorts", "Esports", "BGMI Gameplay"
        ],
        "gaming": [
            "Gaming", "Shorts", "Gaming Shorts", "Viral Shorts", "Esports",
            "Best Gaming Moments", "Gaming Clips", "Trending Gaming", "4K Gaming"
        ]
    }

    HASHTAGS_BY_CATEGORY = {
        "gta6": [
            "#gta6", "#gtavi", "#rockstargames", "#gta6gameplay", "#gamingshorts",
            "#gta6leaks", "#gta6graphics", "#ps5", "#viralgaming", "#shorts",
            "#trending", "#fyp", "#gamingcommunity", "#4kgaming"
        ],
        "bgmi": [
            "#bgmi", "#bgmishorts", "#bgmiclutch", "#bgmimontage", "#pubgmobile",
            "#shorts", "#gaming", "#gamingshorts", "#viral", "#esports", "#1v4clutch"
        ],
        "gaming": [
            "#shorts", "#gaming", "#gamingshorts", "#viral", "#trending", "#fyp"
        ]
    }

    def generate_metadata(self, category: str = "gta6") -> Dict[str, any]:
        cat_key = category.lower()
        if cat_key not in self.HOOK_TEMPLATES:
            cat_key = "gta6"

        title_base = random.choice(self.HOOK_TEMPLATES[cat_key])
        category_hashtags = self.HASHTAGS_BY_CATEGORY.get(cat_key, self.HASHTAGS_BY_CATEGORY["gta6"])
        selected_hashtags = random.sample(category_hashtags, k=min(6, len(category_hashtags)))
        
        # Golden Title
        title = f"{title_base} {' '.join(selected_hashtags[:3])}"[:100]

        # High-Retention Algorithmic Description
        description = (
            f"🎮 {title_base}\n\n"
            f"🔥 Experience the most insane {cat_key.upper()} 4K 60FPS moments, next-gen graphics, and viral stunts!\n\n"
            f"👍 LIKE & SUBSCRIBE for daily ultra-HD gaming shorts and leaks!\n"
            f"💬 Drop a comment: What are you most excited for in {cat_key.upper()}?\n\n"
            f"📌 Trending Tags:\n"
            f"{' '.join(selected_hashtags)}\n\n"
            f"--- Rathour Gaming Official Autopilot ---"
        )

        all_tags = self.TAGS_BY_CATEGORY.get(cat_key, self.TAGS_BY_CATEGORY["gta6"])
        tags = random.sample(all_tags, k=min(15, len(all_tags)))

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "hook_text": title_base,
            "hashtags": selected_hashtags,
            "category": cat_key
        }


if __name__ == "__main__":
    seo = SEOEngine()
    meta = seo.generate_metadata("gta6")
    print("Supercharged GTA 6 Title:", meta["title"])
    print("Tags:", meta["tags"])

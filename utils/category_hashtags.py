# Mapping categories to safe, non-spammy hashtags
CATEGORY_TAGS = {
    "wisdom": ["#Wisdom", "#LifeLessons"],
    "life": ["#Life", "#LifeQuotes"],
    "success": ["#Success", "#Motivation"],
    "courage": ["#Courage", "#BeBrave"],
    "faith": ["#Faith"],
    "happiness": ["#Happiness", "#PositiveVibes"],
    "inspirational": ["#Inspiration", "#DailyInspiration"],
    "truth": ["#Truth"],
    "love": ["#Love", "#LoveQuotes"],
    "humor": ["#Humor"],
    "leadership": ["#Leadership"],
    "nature": ["#Nature"],
    "time": ["#Time"],
    "freedom": ["#Freedom"]
}

def tags_from_categories(categories, max_tags=2):
    tags = []
    if not categories:
        return tags
    for c in categories:
        c = c.lower()
        if c in CATEGORY_TAGS:
            for t in CATEGORY_TAGS[c]:
                if t not in tags:
                    tags.append(t)
        if len(tags) >= max_tags:
            break
    return tags[:max_tags]

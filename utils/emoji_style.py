# Small mapping of categories/themes to emojis
CATEGORY_EMOJI = {
    "wisdom": "🧠",
    "life": "🌱",
    "success": "🏆",
    "courage": "🦁",
    "faith": "🙏",
    "happiness": "😊",
    "inspirational": "✨",
    "truth": "🔍",
    "love": "❤️",
    "humor": "😄",
    "leadership": "👑",
    "nature": "🌿",
    "time": "⏳",
    "freedom": "🕊️"
}

DEFAULT_EMOJIS = ["✨", "💬"]

def emojis_for(categories, keywords=None):
    """
    Return 1-3 emojis based on categories and keywords.
    categories: list of category strings
    keywords: optional list of keywords (strings)
    """
    e = []
    if categories:
        for c in categories:
            c = c.lower()
            if c in CATEGORY_EMOJI:
                e.append(CATEGORY_EMOJI[c])
    # if keywords include clear themes, add an emoji
    if keywords:
        kws = [k.lower() for k in keywords]
        if any(k in kws for k in ("love","heart","romance")):
            e.append("❤️")
        if any(k in kws for k in ("success","win","achievement")):
            e.append("🏆")
        if any(k in kws for k in ("fear","courage","brave")):
            e.append("🦁")

    # dedupe, keep order, limit 3
    seen = []
    for x in e:
        if x not in seen:
            seen.append(x)
    if not seen:
        seen = DEFAULT_EMOJIS
    return " ".join(seen[:3])

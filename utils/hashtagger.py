def generate_hashtags(quote):
    text = quote.lower()

    tags = set()

    # Keyword → Hashtag mapping  
    mapping = {
        "life": ["#Life", "#LifeLessons"],
        "love": ["#Love", "#LoveQuotes"],
        "success": ["#Success", "#Motivation"],
        "motiv": ["#Motivation", "#Inspiration"],
        "inspir": ["#Inspiration", "#DailyInspiration"],
        "wisdom": ["#Wisdom", "#Quotes"],
        "happiness": ["#Happiness", "#PositiveVibes"],
        "courage": ["#Courage", "#BeBrave"],
        "faith": ["#Faith"],
        "truth": ["#Truth"],
        "time": ["#Time"],
        "freedom": ["#Freedom"],
        "fear": ["#OvercomeFear"],
        "leadership": ["#Leadership"],
        "nature": ["#NatureQuotes"],
    }

    # Detect themes based on keywords
    for keyword, taglist in mapping.items():
        if keyword in text:
            for t in taglist:
                tags.add(t)

    # Limit to avoid spam
    tags = list(tags)[:4]

    # Default backup tags
    if len(tags) == 0:
        tags = ["#Quotes", "#Inspiration"]

    return " ".join(tags)

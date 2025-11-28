from .nlp_hashtags import extract_keywords, keywords_to_hashtags
from .category_hashtags import tags_from_categories

def generate_hashtags(quote_text, categories=None, max_total=4):
    """
    Returns final hashtags string (space-joined).
    Strategy:
      1. Start with 1-2 category tags (most relevant)
      2. Add up to (max_total - len(category_tags)) tags from NLP keywords
      3. If none found, fallback to #Quotes #Inspiration
    """
    cats = categories or []
    cat_tags = tags_from_categories(cats, max_tags=2)

    keywords = extract_keywords(quote_text, max_keywords=3)
    nlp_tags = keywords_to_hashtags(keywords)

    final = []
    # Start with category tags (keeps relevance)
    for t in cat_tags:
        if t not in final:
            final.append(t)
    # Add NLP tags next
    for t in nlp_tags:
        if t not in final:
            final.append(t)
        if len(final) >= max_total:
            break

    # fallback
    if not final:
        final = ["#Quotes", "#Inspiration"]

    return " ".join(final[:max_total])

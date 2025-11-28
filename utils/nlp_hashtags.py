import re

# Small english stopwords set (kept internal to avoid heavy libs)
STOPWORDS = {
    "the","and","a","an","in","on","of","to","for","is","are","was","were","it","by",
    "with","that","this","as","be","from","at","or","not","but","your","you","i","we",
    "they","them","he","she","his","her","its","what","who","which","when","where","how",
    "so","if","then","into","about","over","after","before","between","during","through"
}

def extract_keywords(text, max_keywords=3):
    """
    Lightweight keyword extractor:
    - Tokenize, remove punctuation and stopwords
    - Score by word length and frequency
    - Return top N keywords capitalized
    """
    if not text:
        return []

    # remove punctuation (keep apostrophes inside words)
    tokens = re.findall(r"[A-Za-z']{2,}", text)
    freq = {}
    for t in tokens:
        w = t.lower()
        if w in STOPWORDS:
            continue
        if len(w) <= 2:
            continue
        freq[w] = freq.get(w, 0) + 1

    if not freq:
        return []

    # score: frequency * length (prefer longer meaningful words)
    scored = [(word, score*len(word)) for word, score in freq.items() for score in (freq[word],)]
    scored.sort(key=lambda x: (-x[1], -len(x[0])))

    keywords = [w.capitalize() for w, _ in scored[:max_keywords]]
    return keywords

def keywords_to_hashtags(keywords):
    """
    Convert keywords list to reasonable hashtags (simple rules)
    """
    tags = []
    for k in keywords:
        # remove spaces/apostrophes and ensure camelcase style for multiword
        tag = re.sub(r"[^A-Za-z0-9]", "", k)
        if not tag:
            continue
        # common transformations
        if tag.lower() == "motivation":
            tags.append("#Motivation")
        else:
            tags.append("#" + tag)
    # limit to 3 tags
    return tags[:3]

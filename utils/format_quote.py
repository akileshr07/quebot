from .hashtagger import generate_hashtags

def format_quote(quote_dict, max_len=280):
    """
    Clean, aesthetic, minimal quote formatting.
    No emojis, no author, no quotation marks.
    Always capitalized.
    """

    if not quote_dict:
        return None

    text = quote_dict.get("quote", "").strip()
    categories = quote_dict.get("categories", []) or []

    # Remove surrounding quotes if present
    if text.startswith(("“", '"', "'")) and text.endswith(("”", '"', "'")):
        text = text[1:-1].strip()

    # Capitalize first letter always
    if text:
        text = text[0].upper() + text[1:]

    # Generate hashtags
    hashtags = generate_hashtags(text, categories=categories)

    # Base tweet body: simple & aesthetic
    base = f"{text}\n\n{hashtags}"

    # Fit into max length
    if len(base) > max_len:
        allowed = max_len - (len(hashtags) + 2)
        short = text[:allowed].rstrip()

        if " " in short:
            short = short.rsplit(" ", 1)[0]

        short += "…"
        base = f"{short}\n\n{hashtags}"

    return base

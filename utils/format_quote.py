from .hashtagger import generate_hashtags
from .emoji_style import emojis_for

def format_quote(quote_dict, max_len=280):
    """
    quote_dict: {"quote": text, "author": author, "categories": [...]}
    Returns final tweet text (string) that respects the length limit.
    """
    if not quote_dict:
        return None

    text = quote_dict.get("quote", "").strip()
    author = (quote_dict.get("author") or "").strip()
    categories = quote_dict.get("categories", []) or []

    # Build base formatted quote
    base = f"“{text}”"
    if author:
        base += f"\n\n— {author}"

    # Generate hashtags and emojis
    hashtags = generate_hashtags(text, categories=categories)
    emoji_str = emojis_for(categories, keywords=None)  # we keep keywords optional here

    # Compose final with emoji line above hashtags (emoji optional)
    # Format:
    # “quote”
    #
    # — Author
    #
    # ✨ 🧠
    # #Tag1 #Tag2
    candidate = f"{base}\n\n{emoji_str}\n{hashtags}"

    # If too long, trim the quote text elegantly
    if len(candidate) > max_len:
        # allocate some space for author + emojis + hashtags
        reserved = len(f"\n\n{author}") + len(f"\n\n{emoji_str}\n{hashtags}") + 8
        allowed_quote_len = max_len - reserved
        if allowed_quote_len < 50:
            # as a last resort, keep only shorter quote and minimal metadata
            short = (text[:max(40, allowed_quote_len - 1)].rstrip() + "…")
            base = f"“{short}”"
            if author:
                base += f"\n\n— {author}"
            candidate = f"{base}\n\n{emoji_str}\n{hashtags}"
            if len(candidate) > max_len:
                # final fallback: remove emojis
                candidate = f"{base}\n\n{hashtags}"
                # if still too long, hard trim
                if len(candidate) > max_len:
                    candidate = candidate[:max_len-1]
        else:
            short = text[:allowed_quote_len].rstrip()
            # avoid cutting mid-word too crudely
            if " " in short:
                short = short.rsplit(" ", 1)[0]
            short = short.rstrip() + "…"
            base = f"“{short}”"
            if author:
                base += f"\n\n— {author}"
            candidate = f"{base}\n\n{emoji_str}\n{hashtags}"

    return candidate

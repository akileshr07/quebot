from utils.hashtagger import generate_hashtags

def format_quote(raw_text):
    max_len = 260
    quote, author = raw_text.split(" — ")

    quote = quote.strip().strip('"').strip("“").strip("”")
    author = author.strip()

    formatted = f"“{quote}”"

    if author and author.lower() != "unknown":
        formatted += f"\n\n— {author}"

    hashtags = generate_hashtags(quote)

    # Ensure final tweet stays within limit
    final = f"{formatted}\n\n{hashtags}"
    if len(final) > 280:
        allowed = 240 - len(author)
        short = quote[:allowed].rstrip() + "…"
        formatted = f"“{short}”\n\n— {author}"
        final = f"{formatted}\n\n{hashtags}"

    return final

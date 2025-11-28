def format_quote(raw_text):
    max_len = 260  # keep safe margin below 280
    quote, author = raw_text.split(" — ")

    # Clean + beautify
    quote = quote.strip().strip('"').strip("“").strip("”")
    author = author.strip()

    # Add nice styled quotes
    formatted = f"“{quote}”"

    # Add author if available
    if author and author.lower() != "unknown":
        formatted += f"\n\n— {author}"

    # If tweet exceeds limit, trim elegantly
    if len(formatted) > max_len:
        allowed = max_len - len(author) - 5  # space for "…” — A"
        short = quote[:allowed].rstrip() + "…"
        formatted = f"“{short}”\n\n— {author}"

    return formatted

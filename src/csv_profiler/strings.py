def slugify(text: str) -> str:
    return "-".join(text.strip().casefold().split())

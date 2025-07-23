import datetime

# Store mappings
url_store = {}

# Save URL
def save_url(short_code: str, original_url: str) -> None:
    url_store[short_code] = {
        "original_url": original_url,
        "created_at": datetime.datetime.now(),
        "clicks": 0
    }

# Get URL
def get_url(short_code: str) -> dict | None:
    return url_store.get(short_code)

# Count clicks
def increment_clicks(short_code: str) -> None:
    if short_code in url_store:
        url_store[short_code]["clicks"] += 1

# Show stats
def get_stats(short_code: str) -> dict | None:
    record = url_store.get(short_code)
    if record is None:
        return None

    return {
        "url": record["original_url"],
        "created_at": record["created_at"].isoformat(),
        "clicks": record["clicks"]
    }


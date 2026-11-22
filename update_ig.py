import json
import re
import urllib.request
from datetime import datetime, timezone, timedelta

USERNAME = "d.vyoral"
STATS_FILE = "stats.json"

def format_count(num: int) -> str:
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

def fetch_followers(username: str):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Instagram 219.0.0.12.117 Android",
        "x-ig-app-id": "936619743392459",
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            count = data["data"]["user"]["edge_followed_by"]["count"]
            return format_count(int(count))
    except Exception:
        pass

    try:
        web_req = urllib.request.Request(
            f"https://www.instagram.com/{username}/",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(web_req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', html)
            if match:
                return format_count(int(match.group(1)))
    except Exception:
        pass

    return None

def main():
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            current = json.load(f)
    except Exception:
        current = {"followers": "27.8K", "updatedAt": ""}

    new_followers = fetch_followers(USERNAME)
    if new_followers:
        current["followers"] = new_followers

    cz_time = datetime.now(timezone(timedelta(hours=1))).strftime("%d.%m.%Y %H:%M")
    current["updatedAt"] = cz_time

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

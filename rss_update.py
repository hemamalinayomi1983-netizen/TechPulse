import json, hashlib, re
from pathlib import Path
from urllib.parse import urljoin
import feedparser, requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
FEEDS = ROOT / "feeds.json"
ARTICLES = ROOT / "articles.json"
MAX_ARTICLES = 120
HEADERS = {"User-Agent": "TechPulseRSSBot/1.0 (+https://techpulsenews.edgeone.dev/)"}

def read_json(path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback

def clean(value):
    return re.sub(r"\s+", " ", BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True)).strip()

def page_image(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for attrs in ({"property":"og:image"}, {"name":"twitter:image"}):
            tag = soup.find("meta", attrs=attrs)
            if tag and tag.get("content"):
                return urljoin(url, tag["content"])
    except requests.RequestException as exc:
        print("Could not inspect article image:", exc)
    return ""

def image_from_entry(entry, link):
    for field in ("media_content", "media_thumbnail"):
        for item in entry.get(field, []):
            if item.get("url"):
                return urljoin(link, item["url"])
    for item in entry.get("enclosures", []):
        url = item.get("href") or item.get("url")
        if url and item.get("type", "").startswith("image/"):
            return urljoin(link, url)
    html = entry.get("summary", "")
    if not html and entry.get("content"):
        html = entry["content"][0].get("value", "")
    img = BeautifulSoup(html, "html.parser").find("img")
    if img:
        src = img.get("src") or img.get("data-src")
        if src:
            return urljoin(link, src)
    return page_image(link)

def main():
    feeds = read_json(FEEDS, [])
    data = read_json(ARTICLES, {"articles":[]})
    items = data if isinstance(data, list) else data.get("articles", [])
    known = {a.get("url") or a.get("link") for a in items}
    added = 0

    for feed in feeds:
        url = feed.get("url", "")
        if not url:
            continue
        print("Fetching:", feed.get("name", url))
        parsed = feedparser.parse(url)
        if parsed.bozo:
            print("Feed warning:", parsed.bozo_exception)

        for entry in parsed.entries[:20]:
            title = clean(entry.get("title"))
            link = entry.get("link", "").strip()
            if not title or not link or link in known:
                continue

            summary = clean(entry.get("summary", ""))
            if not summary and entry.get("content"):
                summary = clean(entry["content"][0].get("value", ""))
            summary = summary[:450]
            image = image_from_entry(entry, link)
            article_id = hashlib.sha256(link.encode("utf-8")).hexdigest()[:16]

            # Match the TechPulse JSON field names used by the website.
            article = {
                "id": "rss-" + article_id,
                "title": title,
                "category": feed.get("category", "Technology News"),
                "excerpt": summary,
                "body": summary,
                "image": image,
                "date": entry.get("published", ""),
                "source": feed.get("name", "RSS"),
                "origin": "rss",
                "sponsored": False,
                "url": link,
                "link": link
            }
            items.insert(0, article)
            known.add(link)
            added += 1

    # Preserve manually added articles and keep latest feed entries near the top.
    data = {"articles": items[:MAX_ARTICLES]}
    ARTICLES.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done. Added {added} new articles. Total saved: {len(data['articles'])}")

if __name__ == "__main__":
    main()

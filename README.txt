TechPulse shared JSON deployment

Upload BOTH index.html and articles.json to the same folder on your static host.
Do not open index.html using file://; use your hosting site's HTTPS URL or a local web server.

Why this fixes the shared article issue:
- articles.json is a shared public data file, so all visitors receive the same initial articles.
- localStorage is only per visitor/device and is not used as the public shared article database.
- Read Story opens a configured Monetag SmartLink in a new tab and opens the article reader in the current tab.
- SmartLinks are marked as sponsored. Review ad destination suitability before publishing.

Important static hosting limitation:
A static website cannot write newly fetched RSS articles back into articles.json from a visitor's browser. The current RSS refresh/scheduler runs in each browser and its fetched posts are not globally shared. To make daily RSS updates visible to everyone, use a scheduled server-side workflow (GitHub Actions/Cloudflare Worker/Firebase/Supabase) that fetches feeds and updates articles.json, then deploys the updated JSON. Do not put private API keys or admin passwords in public JSON/HTML.

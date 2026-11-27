TECHPULSE AUTO RSS PACKAGE

This package contains your existing TechPulse static site plus scheduled RSS updater files.

FILES
- index.html and articles.json: your existing shared-site package
- feeds.json: RSS sources
- rss_update.py: fetches feed entries, deduplicates by article URL, and saves articles/images
- requirements.txt: Python dependencies
- .github/workflows/rss-update.yml: GitHub Actions schedule (every 6 hours)

IMPORTANT
1. Put these files in the root of the GitHub repository connected to your EdgeOne Pages site.
2. In GitHub: Settings > Actions > General > Workflow permissions > select Read and write permissions > Save.
3. Open Actions > TechPulse RSS Auto Update > Run workflow to test.
4. If EdgeOne is connected to this repository for deployment, its deployment should run after the JSON commit. Confirm the deployment integration in EdgeOne.
5. GitHub scheduled workflows can run late or be temporarily delayed; this is not an exact clock.
6. This package cannot sign into or publish to your GitHub/EdgeOne account. Do not share passwords or private tokens in chat.
7. RSS providers may restrict reuse. Keep article source links, use short excerpts, and check each feed's terms.
8. RSS image and Open Graph image are used where available; some sources may block image retrieval or provide no image.

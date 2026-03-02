# Gulf Watch v2

Simplified MENA security monitor using RSS feeds.

## What's Different from v1?
- **No backend** - Static site hosted on Vercel
- **No database** - JSON file updated by GitHub Actions
- **No Twitter API** - RSS feeds only (free, no rate limits)
- **Reliable** - No deployment issues

## Architecture
```
GitHub Action (hourly) → Fetch RSS → Generate JSON → Commit → Vercel Deploy
```

## Data Sources
18 MENA-focused RSS feeds:
- Reuters Middle East
- BBC Middle East
- Al Jazeera
- The National (UAE)
- Gulf News
- Times of Israel
- And more...

## Deployment

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Connect to Vercel
- Import repo on [vercel.com](https://vercel.com)
- Framework: Other
- Deploy

### 3. Enable GitHub Actions
- Go to repo Settings → Actions → General
- Allow workflows
- GitHub Action will auto-run every hour

## Local Development
```bash
# Fetch data locally
pip install feedparser
python scripts/fetch_rss.py

# Serve locally
python -m http.server 8000
```

## Configuration

### Add RSS Feeds
Edit `scripts/fetch_rss.py`:
```python
FEEDS = [
    {"name": "Source Name", "url": "https://...", "country": "UAE", "credibility": 85},
    ...
]
```

### Modify Keywords
Edit `KEYWORDS` list in `scripts/fetch_rss.py`:

## License
MIT

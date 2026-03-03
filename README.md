# Gulf Watch v2 🎯

[![Live Site](https://img.shields.io/badge/Live-gulf--watch--v2.vercel.app-blue)](https://gulf-watch-v2.vercel.app)
[![GitHub Actions](https://github.com/nKOxxx/gulf-watch-v2/workflows/Update%20RSS%20Feeds/badge.svg)](https://github.com/nKOxxx/gulf-watch-v2/actions)

**Live Site:** https://gulf-watch-v2.vercel.app

Real-time MENA (Middle East & North Africa) security and intelligence monitoring dashboard. Aggregating news from 19+ authoritative sources across the Gulf region.

![Gulf Watch Screenshot](https://gulf-watch-v2.vercel.app/Tactical%20radar%20logo%20with%20Arabian%20Peninsula.png)

## What's Different from v1?
- **No backend** - Static site hosted on Vercel
- **No database** - JSON file updated by GitHub Actions
- **No Twitter API** - RSS feeds only (free, no rate limits)
- **Reliable** - No deployment issues
- **Fast** - Global CDN via Vercel

## Features

### 📰 News Aggregation
- 19 RSS feeds from Tier 1 international and regional sources
- Auto-updates every hour via GitHub Actions
- Keyword filtering for security/threat-related content
- Last 72 hours of incidents

### 🗺️ Interactive Map
- Dark-themed tactical map (Leaflet + CARTO)
- Country filter buttons (UAE, Saudi, Qatar, etc.)
- Click markers for incident details
- Color-coded by incident type

### 📊 Market Impact Panel
- Live oil & gas prices (Brent, Natural Gas)
- Gulf stock indices (Tadawul, ADX, QE)
- Gold prices (safe haven indicator)
- Real-time updates every minute

### 🎯 Live Intelligence
- Military activity alerts
- Strait of Hormuz monitoring
- Air defense status
- Naval movement tracking

## Data Sources (19)

### Tier 1 - International
- Reuters Middle East
- BBC Middle East
- **The Guardian** Middle East
- Al Jazeera

### Tier 2 - Gulf Regional
- The National (UAE)
- Gulf News
- Khaleej Times
- Saudi Gazette
- Arab News
- Saudi Press Agency
- Bahrain News Agency
- Oman News Agency

### Tier 3 - Israel/Palestine
- Times of Israel
- Jerusalem Post
- Haaretz

### Tier 4 - Defense/Security
- Defense News
- Breaking Defense

### Tier 5 - Regional
- Egypt Today
- Daily Star Lebanon
- Jordan Times
- Morocco World News

## Architecture

```
GitHub Action (hourly)
    ↓
Fetch 19 RSS Feeds
    ↓
Parse & Filter (security keywords)
    ↓
Generate incidents.json
    ↓
Commit to GitHub
    ↓
Vercel Auto-Deploy (global CDN)
    ↓
Live Site Updated
```

## Quick Start

### View Live Site
**https://gulf-watch-v2.vercel.app**

### Run Locally
```bash
# Clone repo
git clone https://github.com/nKOxxx/gulf-watch-v2.git
cd gulf-watch-v2

# Install dependencies
pip install feedparser

# Fetch data
python scripts/fetch_rss.py

# Serve locally
cd public
python -m http.server 8000

# Open http://localhost:8000
```

## Configuration

### Add RSS Feed
Edit `scripts/fetch_rss.py`:
```python
FEEDS = [
    {"name": "Source Name", "url": "https://...", "country": "UAE", "credibility": 85},
    ...
]
```

### Modify Keywords
Edit `KEYWORDS` list in `scripts/fetch_rss.py`:
```python
KEYWORDS = [
    'missile', 'drone', 'attack', 'explosion',
    # Add your keywords
]
```

### Manual Data Refresh
1. Go to [Actions tab](https://github.com/nKOxxx/gulf-watch-v2/actions)
2. Click "Update RSS Feeds"
3. Click "Run workflow"

## Tech Stack
- **Frontend:** Vanilla HTML/CSS/JS, Leaflet Maps
- **Data:** Python, feedparser, GitHub Actions
- **Hosting:** Vercel (static site + CDN)
- **APIs:** Yahoo Finance (market data)

## Roadmap
- [ ] Push notifications
- [ ] Mobile app (PWA)
- [ ] AI summaries
- [ ] Historical archive
- [ ] User subscriptions

## License
MIT License - feel free to fork and customize!

## Credits
Built with ❤️ for the Gulf region. Data sourced from reputable international and regional news organizations.

---
**[View Live Site →](https://gulf-watch-v2.vercel.app)**

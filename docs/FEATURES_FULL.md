# Gulf Watch v2 🎯

[![Live Site](https://img.shields.io/badge/Live-gulf--watch--v2.vercel.app-blue)](https://gulf-watch-v2.vercel.app)
[![GitHub Actions](https://github.com/nKOxxx/gulf-watch-v2/workflows/Update%20RSS%20Feeds/badge.svg)](https://github.com/nKOxxx/gulf-watch-v2/actions)

**Live Site:** https://gulf-watch-v2.vercel.app

Real-time MENA (Middle East & North Africa) security and intelligence monitoring dashboard. Aggregating news from **44 authoritative sources** across the Gulf region — including **25 official government ministries and agencies**.

![Gulf Watch Screenshot](https://gulf-watch-v2.vercel.app/Tactical%20radar%20logo%20with%20Arabian%20Peninsula.png)

> *Built with love and respect for the UAE and all countries in the Gulf Region*

## What's Different from v1?
- **No backend** - Static site hosted on Vercel
- **No database** - JSON file updated by GitHub Actions
- **No Twitter API** - RSS feeds only (free, no rate limits)
- **Official sources** - 25 government ministries and agencies
- **Reliable** - No deployment issues
- **Fast** - Global CDN via Vercel

## Features

### 📰 News Aggregation
- **44 sources**: 25 official government + 19 news outlets
- Auto-updates every hour via GitHub Actions
- Keyword filtering for security/threat-related content
- **🏛️ Government badge** - Official sources clearly marked
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

---

## Data Sources (44 Total)

### 🇦🇪 UAE — Official Government (13)
| Source | Type | Handle |
|--------|------|--------|
| UAE Ministry of Interior | Government | [@moiuae](https://twitter.com/moiuae) |
| UAE NCEMA (National Emergency) | Government | [@NCEMAUAE](https://twitter.com/NCEMAUAE) |
| UAE Ministry of Defence | Government | [@modgovae](https://twitter.com/modgovae) |
| UAE National Guard | Government | [@Uaengc](https://twitter.com/Uaengc) |
| UAE Government Media Office | Government | [@UAEmediaoffice](https://twitter.com/UAEmediaoffice) |
| WAM News Agency | State Media | [@wamnews](https://twitter.com/wamnews) |
| WAM English | State Media | [@WAMNEWS_ENG](https://twitter.com/WAMNEWS_ENG) |
| Dubai Media Office | Government | [@DXBMediaOffice](https://twitter.com/DXBMediaOffice) |
| Abu Dhabi Civil Defence | Government | [@CivilDefenceAD](https://twitter.com/CivilDefenceAD) |
| Dubai Civil Defence | Government | [@DCDDubai](https://twitter.com/DCDDubai) |
| Sharjah Civil Defence | Government | [@civildefenceshj](https://twitter.com/civildefenceshj) |
| UAE GCAA (Civil Aviation) | Government | [@gcaauae](https://twitter.com/gcaauae) |
| UAE Ministry of Foreign Affairs | Government | [@mofauae](https://twitter.com/mofauae) |

**UAE News:** The National, Gulf News, Khaleej Times

### 🇸🇦 Saudi Arabia — Official Government (2)
| Source | Type | Handle |
|--------|------|--------|
| Saudi Ministry of Interior | Government | [@MOISaudiArabia](https://twitter.com/MOISaudiArabia) |
| Saudi Civil Defense | Government | [@SaudiDCD](https://twitter.com/SaudiDCD) |

**Saudi News:** Arab News, Saudi Gazette, Al Riyadh, Saudi Press Agency

### 🇶🇦 Qatar — Official Government (2)
| Source | Type | Handle |
|--------|------|--------|
| Qatar Ministry of Interior (EN) | Government | [@MOI_QatarEn](https://twitter.com/MOI_QatarEn) |
| Qatar Civil Defence | Government | [@civildefenceqa](https://twitter.com/civildefenceqa) |

**Qatar News:** Al Jazeera

### 🇰🇼 Kuwait — Official Government (2)
| Source | Type | Handle |
|--------|------|--------|
| Kuwait Ministry of Interior (EN) | Government | [@moi_kuw_en](https://twitter.com/moi_kuw_en) |
| Kuwait Fire Force | Government | [@kff_kw](https://twitter.com/kff_kw) |

### 🇧🇭 Bahrain — Official Government (1)
| Source | Type | Handle |
|--------|------|--------|
| Bahrain Ministry of Interior | Government | [@moi_bahrain](https://twitter.com/moi_bahrain) |

**Bahrain News:** Bahrain News Agency, Gulf Daily News

### 🇴🇲 Oman — Official Government (1)
| Source | Type | Handle |
|--------|------|--------|
| Royal Oman Police | Government | [@RoyalOmanPolice](https://twitter.com/RoyalOmanPolice) |

**Oman News:** Oman News Agency, Oman Daily Observer

### 🇮🇱 Israel — Official Government (4)
| Source | Type | Handle |
|--------|------|--------|
| Israel Defense Forces | Military | [@IDF](https://twitter.com/IDF) |
| Israel Ministry of Defense | Government | [@Israel_MOD](https://twitter.com/Israel_MOD) |
| Magen David Adom | Emergency Services | [@Mdais](https://twitter.com/Mdais) |
| COGAT | Military | [@cogatonline](https://twitter.com/cogatonline) |

**Israel News:** Times of Israel, Jerusalem Post, Haaretz

### 🌍 International & Regional News
- **Reuters** Middle East
- **BBC** Middle East
- **The Guardian** Middle East
- **Defense News**
- **Breaking Defense**
- **Egypt Today**
- **Daily Star Lebanon**
- **Jordan Times**
- **Morocco World News**

---

## Data Quality

### Credibility Scoring
| Score | Source Type |
|-------|-------------|
| 100% | Official Government Ministries |
| 95% | State Media, Military/Defense |
| 90% | International Wire Services |
| 85% | Major Regional News |
| 80% | National News Outlets |
| 75% | Regional/Local News |
| 70% | Independent/Specialized |

### Government Badge 🏛️
Official government sources are marked with a **gold badge** to distinguish them from news outlets. These represent the official source of truth from ministries and agencies.

---

## Architecture

```
GitHub Action (hourly)
    ↓
Fetch 44 RSS Feeds (19 news + 25 government via Nitter)
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

### Add Government Source
Edit `scripts/fetch_rss.py`:
```python
{
    "name": "Ministry Name", 
    "url": "https://nitter.net/handle/rss", 
    "country": "UAE", 
    "credibility": 100,
    "is_government": True
}
```

### Add News Source
```python
{
    "name": "News Source", 
    "url": "https://.../rss", 
    "country": "UAE", 
    "credibility": 85
}
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

---

## Tech Stack
- **Frontend:** Vanilla HTML/CSS/JS, Leaflet Maps
- **Data:** Python, feedparser, GitHub Actions
- **Hosting:** Vercel (static site + CDN)
- **APIs:** Yahoo Finance (market data)
- **Twitter Access:** Nitter RSS proxy (free, no API limits)

---

## Roadmap
- [ ] Push notifications for critical alerts
- [ ] Mobile PWA for on-the-go monitoring
- [ ] AI summaries of complex incidents
- [ ] Historical archive beyond 72h
- [ ] User subscriptions by country/topic
- [ ] Telegram bot for alerts

---

## Respect & Attribution

This project is built with **love and respect for the UAE and all countries in the Gulf Region**.

We believe in:
- **Transparency** - Open data from official sources
- **Safety** - Timely information for residents and visitors
- **Neutrality** - Aggregating facts without editorial bias
- **Accessibility** - Free, open-source, no paywalls

Data sourced from reputable international news organizations and **official government ministries** who serve their citizens with dedication.

---

## License
MIT License - feel free to fork and customize!

## Credits
Built with ❤️ for the Gulf region. Stay safe.

---
**[View Live Site →](https://gulf-watch-v2.vercel.app)**
# Cache purge Fri Mar 13 07:08:28 +04 2026

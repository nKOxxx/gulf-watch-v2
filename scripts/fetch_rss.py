#!/usr/bin/env python3
"""
Gulf Watch RSS Fetcher
Fetches MENA security news from RSS feeds
Outputs static JSON for Vercel hosting
"""
import feedparser
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# MENA-focused RSS feeds
FEEDS = [
    # Tier 1 - International
    {"name": "Reuters Middle East", "url": "https://www.reuters.com/news/archive/middleeast.rss", "country": "International", "credibility": 95},
    {"name": "BBC Middle East", "url": "http://feeds.bbci.co.uk/news/world/middle_east/rss.xml", "country": "International", "credibility": 95},
    {"name": "The Guardian", "url": "https://www.theguardian.com/world/middleeast/rss", "country": "International", "credibility": 90},
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "country": "Qatar", "credibility": 90},
    
    # Tier 2 - Gulf Regional
    {"name": "The National UAE", "url": "https://www.thenationalnews.com/arc/outboundfeeds/rss/?outputType=xml", "country": "UAE", "credibility": 85},
    {"name": "Gulf News", "url": "https://gulfnews.com/rss", "country": "UAE", "credibility": 85},
    {"name": "Khaleej Times", "url": "https://www.khaleejtimes.com/arc/outboundfeeds/rss/?outputType=xml", "country": "UAE", "credibility": 80},
    
    # Saudi Arabia
    {"name": "Arab News", "url": "https://www.arabnews.com/rss.xml", "country": "Saudi Arabia", "credibility": 80},
    {"name": "Saudi Gazette", "url": "https://saudigazette.com.sa/feed/", "country": "Saudi Arabia", "credibility": 80},
    {"name": "Al Riyadh (EN)", "url": "https://www.alriyadh.com/en/rss", "country": "Saudi Arabia", "credibility": 75},
    {"name": "Saudi Press Agency", "url": "https://www.spa.gov.sa/rss", "country": "Saudi Arabia", "credibility": 85},
    
    # Bahrain
    {"name": "Bahrain News Agency", "url": "https://www.bna.bh/en/rss", "country": "Bahrain", "credibility": 80},
    {"name": "Gulf Daily News", "url": "https://www.gdnonline.com/rss", "country": "Bahrain", "credibility": 75},
    
    # Oman
    {"name": "Oman News Agency", "url": "https://www.omanews.gov.om/rss", "country": "Oman", "credibility": 80},
    {"name": "Oman Daily Observer", "url": "https://www.omanobserver.om/rss", "country": "Oman", "credibility": 75},
    
    # Tier 3 - Israel/Palestine
    {"name": "Times of Israel", "url": "https://www.timesofisrael.com/feed/", "country": "Israel", "credibility": 85},
    {"name": "Jerusalem Post", "url": "https://www.jpost.com/Rss/RssFeedsHeadlines.aspx", "country": "Israel", "credibility": 85},
    {"name": "Haaretz", "url": "https://www.haaretz.com/rss.xml", "country": "Israel", "credibility": 85},
    
    # Tier 4 - Defense/Security
    {"name": "Defense News", "url": "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml", "country": "International", "credibility": 90},
    {"name": "Breaking Defense", "url": "https://breakingdefense.com/feed/", "country": "International", "credibility": 85},
    
    # Tier 5 - Egypt/Levant
    {"name": "Egypt Today", "url": "https://www.egypttoday.com/rss", "country": "Egypt", "credibility": 75},
    {"name": "Daily Star Lebanon", "url": "https://www.dailystar.com.lb/rss", "country": "Lebanon", "credibility": 75},
    {"name": "Jordan Times", "url": "https://jordantimes.com/rss", "country": "Jordan", "credibility": 75},
    
    # Tier 6 - North Africa
    {"name": "Morocco World News", "url": "https://www.moroccoworldnews.com/feed/", "country": "Morocco", "credibility": 70},
    {"name": "Tunisia Live", "url": "https://www.tunisia-live.net/feed/", "country": "Tunisia", "credibility": 70},
    
    # Official Government Twitter/X Accounts (via Nitter RSS)
    # UAE
    {"name": "UAE Ministry of Interior", "url": "https://nitter.net/moiuae/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "UAE NCEMA", "url": "https://nitter.net/NCEMAUAE/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "UAE Ministry of Defence", "url": "https://nitter.net/modgovae/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "UAE National Guard", "url": "https://nitter.net/Uaengc/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "UAE Government Media Office", "url": "https://nitter.net/UAEmediaoffice/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "WAM News Agency", "url": "https://nitter.net/wamnews/rss", "country": "UAE", "credibility": 95, "is_government": True},
    {"name": "WAM English", "url": "https://nitter.net/WAMNEWS_ENG/rss", "country": "UAE", "credibility": 95, "is_government": True},
    {"name": "Dubai Media Office", "url": "https://nitter.net/DXBMediaOffice/rss", "country": "UAE", "credibility": 95, "is_government": True},
    {"name": "Abu Dhabi Civil Defence", "url": "https://nitter.net/CivilDefenceAD/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "Dubai Civil Defence", "url": "https://nitter.net/DCDDubai/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "Sharjah Civil Defence", "url": "https://nitter.net/civildefenceshj/rss", "country": "UAE", "credibility": 100, "is_government": True},
    {"name": "UAE GCAA", "url": "https://nitter.net/gcaauae/rss", "country": "UAE", "credibility": 95, "is_government": True},
    {"name": "UAE Ministry of Foreign Affairs", "url": "https://nitter.net/mofauae/rss", "country": "UAE", "credibility": 100, "is_government": True},
    
    # Saudi Arabia
    {"name": "Saudi Ministry of Interior", "url": "https://nitter.net/MOISaudiArabia/rss", "country": "Saudi Arabia", "credibility": 100, "is_government": True},
    {"name": "Saudi Civil Defense", "url": "https://nitter.net/SaudiDCD/rss", "country": "Saudi Arabia", "credibility": 100, "is_government": True},
    
    # Qatar
    {"name": "Qatar Ministry of Interior EN", "url": "https://nitter.net/MOI_QatarEn/rss", "country": "Qatar", "credibility": 100, "is_government": True},
    {"name": "Qatar Civil Defence", "url": "https://nitter.net/civildefenceqa/rss", "country": "Qatar", "credibility": 100, "is_government": True},
    
    # Kuwait
    {"name": "Kuwait Ministry of Interior EN", "url": "https://nitter.net/moi_kuw_en/rss", "country": "Kuwait", "credibility": 100, "is_government": True},
    {"name": "Kuwait Fire Force", "url": "https://nitter.net/kff_kw/rss", "country": "Kuwait", "credibility": 100, "is_government": True},
    
    # Bahrain
    {"name": "Bahrain Ministry of Interior", "url": "https://nitter.net/moi_bahrain/rss", "country": "Bahrain", "credibility": 100, "is_government": True},
    
    # Oman
    {"name": "Royal Oman Police", "url": "https://nitter.net/RoyalOmanPolice/rss", "country": "Oman", "credibility": 100, "is_government": True},
    
    # Israel
    {"name": "Israel Defense Forces", "url": "https://nitter.net/IDF/rss", "country": "Israel", "credibility": 95, "is_government": True},
    {"name": "Israel Ministry of Defense", "url": "https://nitter.net/Israel_MOD/rss", "country": "Israel", "credibility": 95, "is_government": True},
    {"name": "Magen David Adom", "url": "https://nitter.net/Mdais/rss", "country": "Israel", "credibility": 95, "is_government": True},
    {"name": "COGAT", "url": "https://nitter.net/cogatonline/rss", "country": "Israel", "credibility": 95, "is_government": True},
]

# Security/threat keywords
KEYWORDS = [
    # English
    'missile', 'rocket', 'drone', 'uav', 'air defense', 'interceptor',
    'attack', 'strike', 'explosion', 'blast', 'bomb', 'shelling',
    'siren', 'alert', 'warning', 'evacuation', 'shelter',
    'hostile', 'enemy', 'threat', 'incursion', 'infiltration',
    'casualties', 'killed', 'wounded', 'injured', 'dead',
    'idf', 'gaza', 'hamas', 'hezbollah', 'houthi',
    'iran', 'israel', 'palestine', 'lebanon', 'syria',
    'gulf', 'uae', 'saudi', 'qatar', 'bahrain', 'kuwait', 'oman',
    'yemen', 'iraq', 'jordan', 'egypt', 'turkey',
    # Arabic
    'صاروخ', 'طائرة', 'مسيرة', 'هجوم', 'انفجار', 'قصف',
    'تحذير', 'إنذار', 'دفاع', 'عدو', 'معادٍ',
]

# Location extraction
CITIES = {
    'dubai': ('Dubai', 'UAE', 25.2048, 55.2708),
    'abu dhabi': ('Abu Dhabi', 'UAE', 24.4539, 54.3773),
    'riyadh': ('Riyadh', 'Saudi Arabia', 24.7136, 46.6753),
    'jeddah': ('Jeddah', 'Saudi Arabia', 21.4858, 39.1925),
    'doha': ('Doha', 'Qatar', 25.2854, 51.5310),
    'manama': ('Manama', 'Bahrain', 26.2285, 50.5860),
    'kuwait city': ('Kuwait City', 'Kuwait', 29.3759, 47.9774),
    'muscat': ('Muscat', 'Oman', 23.5880, 58.3829),
    'tel aviv': ('Tel Aviv', 'Israel', 32.0853, 34.7818),
    'jerusalem': ('Jerusalem', 'Israel', 31.7683, 35.2137),
    'gaza': ('Gaza', 'Palestine', 31.5017, 34.4668),
    'beirut': ('Beirut', 'Lebanon', 33.8938, 35.5018),
    'damascus': ('Damascus', 'Syria', 33.5138, 36.2765),
    'baghdad': ('Baghdad', 'Iraq', 33.3152, 44.3661),
    'cairo': ('Cairo', 'Egypt', 30.0444, 31.2357),
    'amman': ('Amman', 'Jordan', 31.9454, 35.9284),
    'tehran': ('Tehran', 'Iran', 35.6892, 51.3890),
    'sanaa': ('Sanaa', 'Yemen', 15.3694, 44.1910),
    'aden': ('Aden', 'Yemen', 12.7855, 45.0215),
}

def extract_location(text: str) -> Optional[Dict]:
    """Extract location from text"""
    text_lower = text.lower()
    
    for city_key, (city_name, country, lat, lng) in CITIES.items():
        if city_key in text_lower:
            return {
                'name': city_name,
                'country': country,
                'lat': lat,
                'lng': lng
            }
    
    # Check for country names
    countries = {
        'uae': ('Unknown City', 'UAE', 23.4241, 53.8478),
        'united arab emirates': ('Unknown City', 'UAE', 23.4241, 53.8478),
        'saudi': ('Unknown City', 'Saudi Arabia', 23.8859, 45.0792),
        'qatar': ('Unknown City', 'Qatar', 25.3548, 51.1839),
        'bahrain': ('Unknown City', 'Bahrain', 26.0667, 50.5577),
        'kuwait': ('Unknown City', 'Kuwait', 29.3117, 47.4818),
        'oman': ('Unknown City', 'Oman', 21.4735, 55.9754),
        'israel': ('Unknown City', 'Israel', 31.0461, 34.8516),
        'palestine': ('Unknown City', 'Palestine', 31.9522, 35.2332),
        'gaza': ('Gaza', 'Palestine', 31.5017, 34.4668),
        'lebanon': ('Unknown City', 'Lebanon', 33.8547, 35.8623),
        'syria': ('Unknown City', 'Syria', 34.8021, 38.9968),
        'iraq': ('Unknown City', 'Iraq', 33.2232, 43.6793),
        'jordan': ('Unknown City', 'Jordan', 30.5852, 36.2384),
        'egypt': ('Unknown City', 'Egypt', 26.8206, 30.8025),
        'yemen': ('Unknown City', 'Yemen', 15.5527, 48.5164),
        'iran': ('Unknown City', 'Iran', 32.4279, 53.6880),
    }
    
    for country_key, (city_name, country, lat, lng) in countries.items():
        if country_key in text_lower:
            return {
                'name': city_name,
                'country': country,
                'lat': lat,
                'lng': lng
            }
    
    return None

def classify_incident(text: str) -> str:
    """Classify incident type"""
    text_lower = text.lower()
    
    if any(k in text_lower for k in ['missile', 'rocket', 'صاروخ']):
        return 'missile'
    if any(k in text_lower for k in ['drone', 'uav', 'مسيرة', 'طائرة']):
        return 'drone'
    if any(k in text_lower for k in ['air defense', 'interceptor', 'دفاع']):
        return 'air_defense'
    if any(k in text_lower for k in ['explosion', 'blast', 'bomb', 'انفجار']):
        return 'explosion'
    if any(k in text_lower for k in ['siren', 'alert', 'warning', 'تحذير', 'إنذار']):
        return 'alert'
    if any(k in text_lower for k in ['attack', 'strike', 'هجوم', 'قصف']):
        return 'attack'
    
    return 'security'

def determine_status(text: str) -> str:
    """Determine incident status"""
    text_lower = text.lower()
    
    if any(k in text_lower for k in ['confirmed', 'official', 'verify']):
        return 'confirmed'
    if any(k in text_lower for k in ['reported', 'claim', 'alleged']):
        return 'reported'
    
    return 'unconfirmed'

def is_threat_related(text: str) -> bool:
    """Check if article is threat-related"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)

def parse_date_from_url(url: str) -> Optional[datetime]:
    """Try to extract date from URL (e.g., /2026/mar/02/)"""
    import re
    # Match patterns like /2026/mar/02/ or /2026/03/02/
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    # Try /YYYY/mon/DD/ format (Guardian style)
    match = re.search(r'/(\d{4})/(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/(\d{1,2})/', url.lower())
    if match:
        year, month_str, day = match.groups()
        month = month_map.get(month_str, 1)
        return datetime(int(year), month, int(day))
    
    # Try /YYYY/MM/DD/ format
    match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', url)
    if match:
        year, month, day = match.groups()
        return datetime(int(year), int(month), int(day))
    
    return None

def parse_date(entry) -> Optional[datetime]:
    """Parse date from RSS entry, preferring URL date if available"""
    # First try URL date (more reliable for some feeds like Guardian)
    url_date = parse_date_from_url(entry.get('link', ''))
    if url_date:
        return url_date
    
    # Fall back to RSS date
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6])
    return None

def fetch_feed(feed_info: Dict) -> List[Dict]:
    """Fetch and parse single RSS feed"""
    incidents = []
    
    try:
        print(f"📡 Fetching {feed_info['name']}...")
        feed = feedparser.parse(feed_info['url'])
        
        if hasattr(feed, 'bozo_exception'):
            print(f"   ⚠️ Feed warning: {feed.bozo_exception}")
        
        # Process last 20 entries
        for entry in feed.entries[:20]:
            title = entry.get('title', '')
            
            # Skip if not threat-related
            if not is_threat_related(title):
                continue
            
            # Parse date
            published = parse_date(entry)
            if not published:
                published = datetime.utcnow()
            
            # Skip if older than 72 hours
            if datetime.utcnow() - published > timedelta(hours=72):
                continue
            
            # Extract location
            location = extract_location(title)
            if not location:
                location = {
                    'name': 'Unknown',
                    'country': feed_info['country'],
                    'lat': 25.0,
                    'lng': 45.0
                }
            
            # Create incident
            incident = {
                'id': hash(title + feed_info['name']) % 1000000000,
                'title': title,
                'source': feed_info['name'],
                'source_url': entry.get('link', ''),
                'published': published.isoformat(),
                'type': classify_incident(title),
                'status': determine_status(title),
                'location': location,
                'credibility': feed_info['credibility'],
                'is_government': feed_info.get('is_government', False),
            }
            
            incidents.append(incident)
            print(f"   ✅ {title[:60]}...")
        
        print(f"   Found {len(incidents)} incidents")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return incidents

def fetch_all():
    """Fetch all feeds and generate output"""
    print("🔄 Gulf Watch RSS Fetcher")
    print("=" * 50)
    print(f"⏰ {datetime.utcnow().isoformat()} UTC")
    print()
    
    all_incidents = []
    
    for feed in FEEDS:
        incidents = fetch_feed(feed)
        all_incidents.extend(incidents)
    
    # Sort by published date (newest first)
    all_incidents.sort(key=lambda x: x['published'], reverse=True)
    
    # Deduplicate by title similarity
    seen_titles = set()
    unique_incidents = []
    for inc in all_incidents:
        title_key = inc['title'].lower()[:50]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_incidents.append(inc)
    
    # Generate output
    output = {
        'generated_at': datetime.utcnow().isoformat(),
        'total_incidents': len(unique_incidents),
        'incidents': unique_incidents
    }
    
    # Write to JSON
    with open('public/incidents.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 50)
    print(f"✅ Generated {len(unique_incidents)} unique incidents")
    print(f"📁 Saved to public/incidents.json")

if __name__ == '__main__':
    fetch_all()

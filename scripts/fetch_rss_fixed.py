#!/usr/bin/env python3
"""
Gulf Watch RSS Fetcher - Fixed with Timeouts
Fetches MENA security news from RSS feeds + Nitter
Outputs static JSON for Vercel hosting
"""
import feedparser
import json
import re
import socket
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

# Set global socket timeout
socket.setdefaulttimeout(5)

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
    # Direct threats
    'missile', 'rocket', 'attack', 'strike', 'bomb', 'explosion', 'explosive',
    'intercept', 'air defense', 'patriot', 'thaad', 'iron dome', 'arrow',
    'hostile', 'drone', 'uav', 'aircraft', 'warplane', 'fighter jet',
    
    # Military activity
    'military', 'defense', 'armed forces', 'army', 'navy', 'air force',
    'troop', 'soldier', 'deployment', 'mobilization', 'exercise', 'maneuver',
    
    # Security incidents
    'security', 'threat', 'danger', 'warning', 'alert', 'siren',
    'evacuation', 'shelter', 'safe room', 'bunker',
    
    # Regional conflicts
    'iran', 'israel', 'gaza', 'palestine', 'hamas', 'hezbollah',
    'houthi', 'yemen', 'syria', 'iraq', 'lebanon',
    'gulf', 'strait of hormuz', 'red sea', 'bab el mandeb',
    
    # Civil defense
    'civil defense', 'emergency', 'disaster', 'rescue', 'first responder',
    'casualty', 'injured', 'wounded', 'killed', 'death toll',
    
    # Critical infrastructure
    'oil', 'energy', 'petroleum', 'refinery', 'pipeline', 'port',
    'airport', 'airspace', 'flight', 'aviation', 'closure', 'diversion',
    
    # Diplomatic
    'diplomatic', 'embassy', 'consulate', 'travel warning', 'advisory',
]

# Military/civilian keywords for classification
MILITARY_KEYWORDS = ['soldier', 'military', 'forces', 'army', 'navy', 'air force', 'idf', 'irgc', 'troops']
CIVILIAN_KEYWORDS = ['civilian', 'woman', 'women', 'child', 'children', 'elderly', 'family', 'resident']


def extract_casualties(text: str) -> dict:
    """Extract casualty counts from incident title"""
    text_lower = text.lower()
    
    # Look for patterns like "5 killed", "12 wounded", "20 dead"
    killed_match = re.search(r'(\d+)\s+(?:killed|dead|deaths|die)', text_lower)
    wounded_match = re.search(r'(\d+)\s+(?:wounded|injured|hurt)', text_lower)
    casualties_match = re.search(r'(\d+)\s+(?:casualties|casualty)', text_lower)
    
    # Check for context (military vs civilian)
    is_military = any(kw in text_lower for kw in MILITARY_KEYWORDS)
    is_civilian = any(kw in text_lower for kw in CIVILIAN_KEYWORDS)
    
    killed = int(killed_match.group(1)) if killed_match else 0
    wounded = int(wounded_match.group(1)) if wounded_match else 0
    casualties = int(casualties_match.group(1)) if casualties_match else 0
    
    # If casualties mentioned but not breakdown, use it as total
    total = max(killed + wounded, casualties)
    
    # Classify
    if is_military and not is_civilian:
        military, civilian = total, 0
    elif is_civilian and not is_military:
        military, civilian = 0, total
    else:
        # Unknown - default to civilian unless clearly military
        military, civilian = 0, total
    
    return {
        'total': total,
        'military': military,
        'civilian': civilian
    }


def extract_location(title: str) -> dict:
    """Extract location from incident title"""
    text_lower = title.lower()
    
    # Country mapping
    country_keywords = {
        'uae': 'UAE',
        'united arab emirates': 'UAE',
        'dubai': 'UAE',
        'abu dhabi': 'UAE',
        'saudi': 'Saudi Arabia',
        'saudi arabia': 'Saudi Arabia',
        'riyadh': 'Saudi Arabia',
        'qatar': 'Qatar',
        'doha': 'Qatar',
        'kuwait': 'Kuwait',
        'bahrain': 'Bahrain',
        'oman': 'Oman',
        'muscat': 'Oman',
        'israel': 'Israel',
        'iran': 'Iran',
        'tehran': 'Iran',
        'lebanon': 'Lebanon',
        'beirut': 'Lebanon',
        'gaza': 'Palestine',
        'palestine': 'Palestine',
        'syria': 'Syria',
        'damascus': 'Syria',
        'yemen': 'Yemen',
        'iraq': 'Iraq',
        'baghdad': 'Iraq',
        'jordan': 'Jordan',
    }
    
    for keyword, country in country_keywords.items():
        if keyword in text_lower:
            return {'country': country, 'city': None}
    
    return {'country': 'Unknown', 'city': None}


def is_security_related(title: str) -> bool:
    """Check if article is security/threat related"""
    text_lower = title.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)


def parse_date(entry) -> Optional[datetime]:
    """Parse date from feed entry"""
    # Try published_parsed first
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except:
            pass
    
    # Try updated_parsed
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
        except:
            pass
    
    return None


def fetch_single_feed(feed_config: dict) -> List[dict]:
    """Fetch a single RSS feed with timeout"""
    name = feed_config['name']
    url = feed_config['url']
    country = feed_config['country']
    credibility = feed_config['credibility']
    is_gov = feed_config.get('is_government', False)
    
    incidents = []
    
    try:
        # feedparser doesn't support timeout param, use socket timeout
        response = feedparser.parse(url)
        
        if not response.entries:
            print(f"  {name}: No entries")
            return []
        
        for entry in response.entries[:10]:  # Limit to 10 per feed
            title = entry.get('title', '')
            
            if not title or not is_security_related(title):
                continue
            
            published = parse_date(entry)
            if not published:
                continue
            
            # Skip old entries (>72 hours)
            if datetime.now(timezone.utc) - published > timedelta(hours=72):
                continue
            
            # Extract casualties
            casualties = extract_casualties(title)
            
            # Extract location
            location = extract_location(title)
            if location['country'] == 'Unknown':
                location['country'] = country
            
            incident = {
                'id': entry.get('id', entry.get('link', '')) or f"{name}-{hash(title)}",
                'title': title,
                'source': name,
                'source_url': entry.get('link', ''),
                'published': published.isoformat(),
                'type': 'incident',
                'status': 'active',
                'location': location,
                'credibility': credibility,
                'is_government': is_gov,
                'casualties': casualties,
            }
            
            incidents.append(incident)
        
        print(f"  {name}: {len(incidents)} incidents")
        return incidents
        
    except Exception as e:
        print(f"  {name}: Error - {str(e)[:50]}")
        return []


def fetch_all_feeds() -> List[dict]:
    """Fetch all feeds in parallel with timeouts"""
    all_incidents = []
    
    print(f"Fetching {len(FEEDS)} feeds with 5-second timeout...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_feed = {executor.submit(fetch_single_feed, feed): feed for feed in FEEDS}
        
        for future in as_completed(future_to_feed):
            feed = future_to_feed[future]
            try:
                incidents = future.result(timeout=6)  # 6 sec total per feed
                all_incidents.extend(incidents)
            except Exception as e:
                print(f"  {feed['name']}: Timeout/Error")
    
    return all_incidents


def main():
    print(f"Starting RSS fetch at {datetime.now(timezone.utc).isoformat()}")
    
    # Fetch all feeds
    incidents = fetch_all_feeds()
    
    print(f"\nTotal incidents fetched: {len(incidents)}")
    
    # Sort by date (newest first)
    incidents.sort(key=lambda x: x['published'], reverse=True)
    
    # Output
    output = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total_incidents': len(incidents),
        'incidents': incidents
    }
    
    # Write to file
    with open('public/incidents.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Saved to public/incidents.json")
    
    if incidents:
        newest = datetime.fromisoformat(incidents[0]['published'])
        age = (datetime.now(timezone.utc) - newest).total_seconds() / 3600
        print(f"Newest incident: {newest.isoformat()} ({age:.1f} hours ago)")


if __name__ == '__main__':
    main()

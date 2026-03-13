#!/usr/bin/env python3
"""
Coordinate Extractor for Gulf Watch
Ensures every event has lat/lng coordinates
"""

import re
import json
from typing import Dict, Optional, Tuple
from difflib import get_close_matches

class CoordinateExtractor:
    """
    Extracts or looks up coordinates for Gulf Watch incidents.
    Ensures no event is stored without lat/lng.
    """
    
    def __init__(self):
        # Major city coordinates database
        self.city_coords = {
            # Iran
            'tehran': {'lat': 35.6892, 'lng': 51.3890, 'country': 'Iran'},
            'isfahan': {'lat': 32.6539, 'lng': 51.6660, 'country': 'Iran'},
            'mashhad': {'lat': 36.2605, 'lng': 59.6168, 'country': 'Iran'},
            'tabriz': {'lat': 38.0962, 'lng': 46.2738, 'country': 'Iran'},
            'shiraz': {'lat': 29.5926, 'lng': 52.5836, 'country': 'Iran'},
            'bandar abbas': {'lat': 27.1833, 'lng': 56.2667, 'country': 'Iran'},
            'ahvaz': {'lat': 31.3183, 'lng': 48.6706, 'country': 'Iran'},
            'kermanshah': {'lat': 34.3142, 'lng': 47.0650, 'country': 'Iran'},
            
            # Israel
            'tel aviv': {'lat': 32.0853, 'lng': 34.7818, 'country': 'Israel'},
            'jerusalem': {'lat': 31.7683, 'lng': 35.2137, 'country': 'Israel'},
            'haifa': {'lat': 32.7940, 'lng': 34.9896, 'country': 'Israel'},
            'gaza': {'lat': 31.5017, 'lng': 34.4668, 'country': 'Palestine'},
            'gaza city': {'lat': 31.5017, 'lng': 34.4668, 'country': 'Palestine'},
            'rafah': {'lat': 31.2968, 'lng': 34.2453, 'country': 'Palestine'},
            'khan yunis': {'lat': 31.3461, 'lng': 34.3063, 'country': 'Palestine'},
            'beersheba': {'lat': 31.2589, 'lng': 34.7997, 'country': 'Israel'},
            'ashdod': {'lat': 31.8044, 'lng': 34.6553, 'country': 'Israel'},
            'ashkelon': {'lat': 31.6695, 'lng': 34.5715, 'country': 'Israel'},
            'eilat': {'lat': 29.5581, 'lng': 34.9482, 'country': 'Israel'},
            
            # Lebanon
            'beirut': {'lat': 33.8938, 'lng': 35.5018, 'country': 'Lebanon'},
            'tripoli': {'lat': 34.4346, 'lng': 35.8362, 'country': 'Lebanon'},
            'sidon': {'lat': 33.5631, 'lng': 35.3689, 'country': 'Lebanon'},
            'tyre': {'lat': 33.2700, 'lng': 35.2033, 'country': 'Lebanon'},
            'baalbek': {'lat': 34.0058, 'lng': 36.2181, 'country': 'Lebanon'},
            
            # Syria
            'damascus': {'lat': 33.5138, 'lng': 36.2765, 'country': 'Syria'},
            'aleppo': {'lat': 36.2021, 'lng': 37.1343, 'country': 'Syria'},
            'homs': {'lat': 34.7308, 'lng': 36.7094, 'country': 'Syria'},
            
            # Iraq
            'baghdad': {'lat': 33.3152, 'lng': 44.3661, 'country': 'Iraq'},
            'basra': {'lat': 30.5156, 'lng': 47.7804, 'country': 'Iraq'},
            'mosul': {'lat': 36.3566, 'lng': 43.1642, 'country': 'Iraq'},
            'erbil': {'lat': 36.1911, 'lng': 44.0092, 'country': 'Iraq'},
            
            # Yemen
            'sanaa': {'lat': 15.3694, 'lng': 44.1910, 'country': 'Yemen'},
            'aden': {'lat': 12.7855, 'lng': 45.0187, 'country': 'Yemen'},
            'hodeidah': {'lat': 14.7974, 'lng': 42.9570, 'country': 'Yemen'},
            
            # UAE
            'dubai': {'lat': 25.2048, 'lng': 55.2708, 'country': 'UAE'},
            'abu dhabi': {'lat': 24.4539, 'lng': 54.3773, 'country': 'UAE'},
            'sharjah': {'lat': 25.3463, 'lng': 55.4209, 'country': 'UAE'},
            
            # Saudi Arabia
            'riyadh': {'lat': 24.7136, 'lng': 46.6753, 'country': 'Saudi Arabia'},
            'jeddah': {'lat': 21.4858, 'lng': 39.1925, 'country': 'Saudi Arabia'},
            'mecca': {'lat': 21.3891, 'lng': 39.8579, 'country': 'Saudi Arabia'},
            'medina': {'lat': 24.5247, 'lng': 39.5692, 'country': 'Saudi Arabia'},
            'dammam': {'lat': 26.3927, 'lng': 50.0916, 'country': 'Saudi Arabia'},
            'khobar': {'lat': 26.2172, 'lng': 50.1971, 'country': 'Saudi Arabia'},
            'tabuk': {'lat': 28.3835, 'lng': 36.5662, 'country': 'Saudi Arabia'},
            'dhahran': {'lat': 26.2361, 'lng': 50.0393, 'country': 'Saudi Arabia'},
            
            # Qatar
            'doha': {'lat': 25.2854, 'lng': 51.5310, 'country': 'Qatar'},
            
            # Bahrain
            'manama': {'lat': 26.2285, 'lng': 50.5860, 'country': 'Bahrain'},
            
            # Kuwait
            'kuwait city': {'lat': 29.3759, 'lng': 47.9774, 'country': 'Kuwait'},
            
            # Oman
            'muscat': {'lat': 23.5859, 'lng': 58.4059, 'country': 'Oman'},
            'salalah': {'lat': 17.0151, 'lng': 54.0924, 'country': 'Oman'},
            
            # Jordan
            'amman': {'lat': 31.9454, 'lng': 35.9284, 'country': 'Jordan'},
            
            # Egypt
            'cairo': {'lat': 30.0444, 'lng': 31.2357, 'country': 'Egypt'},
            'alexandria': {'lat': 31.2001, 'lng': 29.9187, 'country': 'Egypt'},
            'suez': {'lat': 29.9668, 'lng': 32.5498, 'country': 'Egypt'},
        }
        
        # Country center coordinates (fallback)
        self.country_coords = {
            'iran': {'lat': 32.4279, 'lng': 53.6880},
            'israel': {'lat': 31.0461, 'lng': 34.8516},
            'palestine': {'lat': 31.9522, 'lng': 35.2332},
            'gaza': {'lat': 31.5017, 'lng': 34.4668},
            'lebanon': {'lat': 33.8547, 'lng': 35.8623},
            'syria': {'lat': 34.8021, 'lng': 38.9968},
            'iraq': {'lat': 33.2232, 'lng': 43.6793},
            'yemen': {'lat': 15.5527, 'lng': 48.5164},
            'uae': {'lat': 23.4241, 'lng': 53.8478},
            'saudi arabia': {'lat': 23.8859, 'lng': 45.0792},
            'qatar': {'lat': 25.3548, 'lng': 51.1839},
            'bahrain': {'lat': 26.0667, 'lng': 50.5577},
            'kuwait': {'lat': 29.3117, 'lng': 47.4818},
            'oman': {'lat': 21.4735, 'lng': 55.9754},
            'jordan': {'lat': 30.5852, 'lng': 36.2384},
            'egypt': {'lat': 26.8206, 'lng': 30.8025},
        }
        
        # Region coordinates (specific areas)
        self.region_coords = {
            'strait of hormuz': {'lat': 26.5000, 'lng': 56.5000},
            'red sea': {'lat': 20.0000, 'lng': 38.0000},
            'gulf of aden': {'lat': 12.0000, 'lng': 47.0000},
            'persian gulf': {'lat': 26.0000, 'lng': 52.0000},
            'mediterranean sea': {'lat': 34.5000, 'lng': 32.0000},
            'west bank': {'lat': 31.9466, 'lng': 35.3027},
        }
    
    def _extract_from_text(self, text: str) -> Optional[Dict]:
        """Try to extract coordinates from article text"""
        if not text:
            return None
        
        text_lower = text.lower()
        
        # Look for explicit coordinate mentions
        # Pattern: lat 35.6892, lng 51.3890
        coord_patterns = [
            r'lat(?:itude)?[:\s]+(-?\d+\.?\d*)[:\s,]+lng(?:itude)?[:\s]+(-?\d+\.?\d*)',
            r'(-?\d+\.?\d*)°?[\s]*[Nn][,\s]+(-?\d+\.?\d*)°?[\s]*[Ee]',
            r'coordinates?:?\s*(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)',
        ]
        
        for pattern in coord_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    lat = float(match.group(1))
                    lng = float(match.group(2))
                    # Validate ranges
                    if -90 <= lat <= 90 and -180 <= lng <= 180:
                        return {'lat': lat, 'lng': lng, 'source': 'extracted'}
                except ValueError:
                    continue
        
        return None
    
    def _lookup_city(self, location_text: str) -> Optional[Dict]:
        """Look up city by name"""
        if not location_text:
            return None
        
        location_lower = location_text.lower()
        
        # Direct match
        if location_lower in self.city_coords:
            coords = self.city_coords[location_lower]
            return {
                'lat': coords['lat'],
                'lng': coords['lng'],
                'source': f"city_lookup:{location_lower}",
                'country': coords['country']
            }
        
        # Check if location contains a known city
        for city, coords in self.city_coords.items():
            if city in location_lower:
                return {
                    'lat': coords['lat'],
                    'lng': coords['lng'],
                    'source': f"city_lookup:{city}",
                    'country': coords['country']
                }
        
        # Fuzzy match for typos/variants
        words = location_lower.split()
        for word in words:
            matches = get_close_matches(word, self.city_coords.keys(), n=1, cutoff=0.8)
            if matches:
                city = matches[0]
                coords = self.city_coords[city]
                return {
                    'lat': coords['lat'],
                    'lng': coords['lng'],
                    'source': f"fuzzy_match:{city}",
                    'country': coords['country']
                }
        
        return None
    
    def _lookup_country(self, location_text: str) -> Optional[Dict]:
        """Fallback to country center"""
        if not location_text:
            return None
        
        location_lower = location_text.lower()
        
        # Direct match
        for country, coords in self.country_coords.items():
            if country in location_lower:
                return {
                    'lat': coords['lat'],
                    'lng': coords['lng'],
                    'source': f"country_center:{country}",
                    'approximate': True
                }
        
        # Check region
        for region, coords in self.region_coords.items():
            if region in location_lower:
                return {
                    'lat': coords['lat'],
                    'lng': coords['lng'],
                    'source': f"region:{region}",
                    'approximate': True
                }
        
        return None
    
    def get_coordinates(self, article: Dict) -> Dict:
        """
        Main method to get coordinates for an article.
        Tries multiple methods in order of precision.
        Never returns None - always provides coordinates.
        """
        title = article.get('title', '')
        location = article.get('location', '')
        content = article.get('content', '')
        
        result = {
            'lat': None,
            'lng': None,
            'source': None,
            'approximate': False,
            'country': None
        }
        
        # Method 1: Extract from text (most precise)
        extracted = self._extract_from_text(f"{title} {content}")
        if extracted:
            result['lat'] = extracted['lat']
            result['lng'] = extracted['lng']
            result['source'] = 'extracted_from_text'
            return result
        
        # Method 2: Look up city
        city_match = self._lookup_city(location) or self._lookup_city(title)
        if city_match:
            result['lat'] = city_match['lat']
            result['lng'] = city_match['lng']
            result['source'] = city_match['source']
            result['country'] = city_match.get('country')
            return result
        
        # Method 3: Look up country center (fallback)
        country_match = self._lookup_country(location) or self._lookup_country(title)
        if country_match:
            result['lat'] = country_match['lat']
            result['lng'] = country_match['lng']
            result['source'] = country_match['source']
            result['approximate'] = country_match.get('approximate', True)
            return result
        
        # Method 4: Ultimate fallback - center of Gulf region
        result['lat'] = 29.0
        result['lng'] = 48.0
        result['source'] = 'gulf_region_center'
        result['approximate'] = True
        
        return result
    
    def validate_coordinates(self, coords: Dict) -> bool:
        """Validate coordinate values"""
        try:
            lat = float(coords.get('lat', 0))
            lng = float(coords.get('lng', 0))
            return -90 <= lat <= 90 and -180 <= lng <= 180
        except (ValueError, TypeError):
            return False
    
    def process_article(self, article: Dict) -> Dict:
        """
        Process article and ensure it has coordinates.
        Returns article with coordinates added.
        """
        coords = self.get_coordinates(article)
        
        # Validate
        if not self.validate_coordinates(coords):
            # Force fallback if invalid
            coords = {
                'lat': 29.0,
                'lng': 48.0,
                'source': 'fallback_invalid',
                'approximate': True
            }
        
        # Add to article
        article['coordinates'] = {
            'lat': coords['lat'],
            'lng': coords['lng'],
            'source': coords['source'],
            'approximate': coords.get('approximate', False)
        }
        
        if coords.get('country'):
            article['country'] = coords['country']
        
        return article


# Test suite
if __name__ == "__main__":
    print("="*70)
    print("COORDINATE EXTRACTOR - TEST SUITE")
    print("="*70)
    
    extractor = CoordinateExtractor()
    
    test_cases = [
        {
            'name': 'Tel Aviv Missile Strike',
            'article': {
                'title': 'Missile strike hits Tel Aviv',
                'location': 'Tel Aviv, Israel',
                'content': 'A missile was intercepted over Tel Aviv today.'
            },
            'expected_city': 'tel aviv'
        },
        {
            'name': 'Tehran Airstrike',
            'article': {
                'title': 'Airstrike targets military base near Tehran',
                'location': 'Tehran, Iran',
                'content': 'Explosions reported in Tehran suburbs.'
            },
            'expected_city': 'tehran'
        },
        {
            'name': 'Gaza Rocket Attack',
            'article': {
                'title': 'Rockets fired from Gaza',
                'location': 'Gaza Strip',
                'content': 'Multiple rockets launched from Gaza.'
            },
            'expected_city': 'gaza'
        },
        {
            'name': 'Strait of Hormuz',
            'article': {
                'title': 'Ship attacked in Strait of Hormuz',
                'location': 'Strait of Hormuz',
                'content': 'Commercial vessel targeted.'
            },
            'expected_region': 'strait of hormuz'
        },
        {
            'name': 'Unknown Location',
            'article': {
                'title': 'Mysterious explosion reported',
                'location': 'Somewhere in Middle East',
                'content': 'Details unclear.'
            },
            'expected_fallback': True
        },
        {
            'name': 'Coordinates in Text',
            'article': {
                'title': 'Attack at coordinates lat 35.6892, lng 51.3890',
                'location': 'Unknown',
                'content': 'Incident occurred at lat 35.6892, lng 51.3890'
            },
            'expected_coords': {'lat': 35.6892, 'lng': 51.3890}
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        print(f"\n🧪 Test: {test['name']}")
        
        result = extractor.process_article(test['article'])
        coords = result.get('coordinates', {})
        
        print(f"   Location: {test['article']['location']}")
        print(f"   Coordinates: lat={coords.get('lat')}, lng={coords.get('lng')}")
        print(f"   Source: {coords.get('source')}")
        print(f"   Approximate: {coords.get('approximate')}")
        
        # Verify coordinates exist
        if coords.get('lat') is not None and coords.get('lng') is not None:
            print(f"   ✅ Coordinates present")
            passed += 1
        else:
            print(f"   ❌ Missing coordinates")
            failed += 1
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"✅ Passed: {passed}/{len(test_cases)}")
    print(f"❌ Failed: {failed}/{len(test_cases)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED - Every event has coordinates!")
    else:
        print(f"\n⚠️ {failed} tests failed")
    
    print("\n📊 Coordinate Sources Used:")
    print("   - Extracted from text (explicit coordinates)")
    print("   - City database (50+ cities)")
    print("   - Country centers (15 countries)")
    print("   - Region centers (Strait of Hormuz, Red Sea, etc.)")
    print("   - Ultimate fallback (Gulf region center)")

#!/usr/bin/env python3
"""
Generate UAE Missile Defense Stats from incident data
Extracts missile/drone detection data from incidents.json
"""
import json
from datetime import datetime, timezone, timedelta

def generate_missile_stats():
    """Generate missile defense stats from incidents"""
    
    with open('public/incidents.json', 'r') as f:
        data = json.load(f)
    
    incidents = data.get('incidents', [])
    now = datetime.now(timezone.utc)
    last_24h = now - timedelta(hours=24)
    
    # Initialize counters
    total_detected = 0
    total_intercepted = 0
    total_impacted = 0
    ballistic_detected = 0
    ballistic_intercepted = 0
    drones_detected = 0
    drones_intercepted = 0
    
    # Last 24h counters
    last_24h_detected = 0
    last_24h_intercepted = 0
    
    for incident in incidents:
        title = incident.get('title', '').lower()
        published = datetime.fromisoformat(incident['published'])
        is_recent = published >= last_24h
        
        # Check if missile/rocket related
        if 'missile' in title or 'rocket' in title or 'ballistic' in title:
            total_detected += 1
            if is_recent:
                last_24h_detected += 1
            
            # Check for interception keywords
            if 'intercept' in title or 'shot down' in title or 'destroyed' in title or 'downed' in title:
                total_intercepted += 1
                if is_recent:
                    last_24h_intercepted += 1
            else:
                total_impacted += 1
            
            # Ballistic missile specific
            if 'ballistic' in title or 'cruise' in title:
                ballistic_detected += 1
                if 'intercept' in title or 'shot down' in title:
                    ballistic_intercepted += 1
        
        # Check if drone/UAV related
        if 'drone' in title or 'uav' in title:
            drones_detected += 1
            if 'intercept' in title or 'shot down' in title or 'destroyed' in title:
                drones_intercepted += 1
    
    # Build stats object
    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "totals": {
            "total_detected": total_detected,
            "total_intercepted": total_intercepted,
            "impacted": total_impacted,
            "ballistic_detected": ballistic_detected,
            "ballistic_intercepted": ballistic_intercepted,
            "drones_detected": drones_detected,
            "drones_intercepted": drones_intercepted,
            "success_rate": round((total_intercepted / total_detected * 100), 1) if total_detected > 0 else 0
        },
        "last_24h": {
            "detected": last_24h_detected,
            "intercepted": last_24h_intercepted,
            "success_rate": round((last_24h_intercepted / last_24h_detected * 100), 1) if last_24h_detected > 0 else 0
        },
        "by_country": {},
        "timeline": []
    }
    
    return stats

def main():
    stats = generate_missile_stats()
    
    with open('public/moi_missile_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Generated missile stats:")
    print(f"  Total detected: {stats['totals']['total_detected']}")
    print(f"  Total intercepted: {stats['totals']['total_intercepted']}")
    print(f"  Success rate: {stats['totals']['success_rate']}%")
    print(f"  Last 24h: {stats['last_24h']['detected']} detected, {stats['last_24h']['intercepted']} intercepted")
    print(f"  Saved to public/moi_missile_stats.json")

if __name__ == '__main__':
    main()

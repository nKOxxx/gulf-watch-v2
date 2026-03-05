#!/usr/bin/env python3
"""
Gulf Watch Price Fetcher
Fetches commodity and market data for the finance panel
Outputs static JSON for Vercel hosting
"""
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

def fetch_yahoo_finance(symbol):
    """Fetch data from Yahoo Finance"""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('chart') and data['chart'].get('result'):
                result = data['chart']['result'][0]
                current = result['meta'].get('regularMarketPrice')
                prev = result['meta'].get('chartPreviousClose')
                
                if current and prev:
                    change_pct = ((current - prev) / prev) * 100
                    return {
                        'price': current,
                        'change': round(change_pct, 2),
                        'prev_close': prev
                    }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    
    return None

def main():
    # Symbols to fetch
    symbols = {
        'brent': {'symbol': 'BZ=F', 'name': 'Brent Oil', 'format': '${:.2f}'},
        'gas': {'symbol': 'NG=F', 'name': 'Natural Gas', 'format': '${:.3f}'},
        'gold': {'symbol': 'GC=F', 'name': 'Gold', 'format': '${:.0f}'},
        'bitcoin': {'symbol': 'BTC-USD', 'name': 'Bitcoin', 'format': '${:,.0f}'}
    }
    
    prices = {}
    
    for key, config in symbols.items():
        print(f"Fetching {config['name']}...")
        data = fetch_yahoo_finance(config['symbol'])
        
        if data:
            prices[key] = {
                'name': config['name'],
                'price': data['price'],
                'change': data['change'],
                'formatted_price': config['format'].format(data['price']),
                'formatted_change': f"{data['change']:+.2f}%",
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            print(f"  ✓ {config['name']}: {prices[key]['formatted_price']} ({prices[key]['formatted_change']})")
        else:
            print(f"  ✗ Failed to fetch {config['name']}")
    
    # Build output
    output = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'prices': prices
    }
    
    # Save to public directory
    with open('public/prices.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Saved prices for {len(prices)} items to public/prices.json")
    print(f"  Generated at: {output['generated_at']}")

if __name__ == '__main__':
    main()

"""Snapshot of ADS-B traffic for the Turkey-to-Oman box into public/flights.json.

Keyless: OpenSky's anonymous API, one bounding-box call (costs 4 of the 400 daily anonymous
credits). Set OPENSKY_USER / OPENSKY_PASS in the environment for a higher quota. The browser
cannot call OpenSky directly (no CORS), so the page reads this file instead.
"""
import base64, json, os, sys, urllib.parse, urllib.request

BOX = {"lamin": 15, "lomin": 26, "lamax": 42, "lomax": 62}
OUT = os.path.join(os.path.dirname(__file__), "..", "public", "flights.json")

req = urllib.request.Request(
    "https://opensky-network.org/api/states/all?" + urllib.parse.urlencode(BOX),
    headers={"User-Agent": "gulfwatch (+https://github.com/nKOxxx/gulf-watch-v2)"},
)
user, pw = os.environ.get("OPENSKY_USER"), os.environ.get("OPENSKY_PASS")
if user and pw:
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode())
try:
    j = json.load(urllib.request.urlopen(req, timeout=30))
except Exception as e:
    print(f"flights: upstream unavailable ({e}); keeping previous snapshot", file=sys.stderr)
    sys.exit(0)

aircraft = [
    {"hex": s[0], "flight": (s[1] or "").strip(), "lon": s[5], "lat": s[6],
     "alt": 0 if s[8] else round((s[7] if s[7] is not None else (s[13] or 0)) * 3.28084),
     "gs": round((s[9] or 0) * 1.94384), "track": s[10] or 0}
    for s in (j.get("states") or []) if s[5] is not None and s[6] is not None
]
with open(OUT, "w") as f:
    json.dump({"source": "opensky-network.org", "data_time": j.get("time"), "aircraft": aircraft}, f, separators=(",", ":"))
print(f"flights: {len(aircraft)} aircraft")

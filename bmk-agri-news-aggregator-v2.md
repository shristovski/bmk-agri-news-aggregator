Geolocation detection v2 — all fixes, enhancements, and testing utilities.

Current problem (solved):
The app was showing "The Dalles / United States / North America" for all users because it was detecting the server/hosting IP instead of the real visitor IP.

Detection priority chain (how it works now):

1. Test IP override (DEBUG mode only)
   - If GEOLOCATION_DEBUG=1 and user types an IP in the debug panel text field
   - That IP is used directly — no API calls for header extraction
   - Clearing the field reverts to real detection
   - Widget key and stored value key are separate to detect changes properly

2. Client IP from request headers (production / behind proxy)
   - Priority order:
     a. CF-Connecting-IP (Cloudflare)
     b. True-Client-IP (Akamai / some CDNs)
     c. X-Real-IP (NGINX)
     d. X-Forwarded-For (generic proxy) — first public IP, skips private ranges
   - Private IP ranges skipped: 127.x.x.x, 10.x.x.x, 172.16-31.x.x, 192.168.x.x, 169.254.x.x, 0.x.x.x
   - If all IPs in X-Forwarded-For are private, returns None

3. Server-side fallback (local dev / direct connection)
   - If no client IP extracted (no proxy headers exist), falls back to:
     a. ipapi.co/json (detects the machine's own public IP)
     b. ipinfo.io/json (backup if ipapi fails)

4. Safe default
   - If ALL detection methods fail, returns "Global Agriculture News"
   - Never defaults to USA, The Dalles, or any hardcoded location
   - Shows warning banner: "Automatic location detection is unavailable. Showing global news."

Per-session detection:
- Location is detected once per session and stored in st.session_state.user_location
- Not cached globally — each visitor gets their own detection
- If DEBUG test IP changes, location is re-detected and page re-renders

Manual override controls:
- Continent selector
- Region selector
- Country selector
- Commodity selector
- Manual selection overrides automatic IP detection for news ranking
- Session state tracks manual_continent, manual_region, manual_country
- Header text changes to "Showing manually selected ..." when overrides are active

Debug mode (GEOLOCATION_DEBUG=1):
- Expander panel shows at the top of the page
- Test IP text input — type any IP and press Enter to simulate that location
- Displays: raw headers, extracted client IP, detected country/region/continent
- Auto-detected flag, manual override status, warning status
- All debug output hidden when GEOLOCATION_DEBUG is not set

UI location text formats:
- "City / Country / Region / Continent" — auto-detected with city
- "Country / Region / Continent" — auto-detected without city
- "Showing manually selected continent/region/country: ..." — manual override
- "Showing global agriculture news" — no detection

Files modified:

src/geolocation.py:
- Added extract_client_ip(headers) — extracts real visitor IP from proxy headers
- Added is_private_ip(ip) — detects private/internal IPs
- Added detect_location(client_ip) — new chain: client IP from headers → server-side fallback
- Added detect_location_from_ip(client_ip) — queries ipapi.co/{ip}/json and ipinfo.io/{ip}/json
- Added geolocate_from_coords(lat, lng) — reverse geocoding via Nominatim (for future browser geo)
- Added get_all_continents() — returns sorted unique continents
- Added get_countries_for_continent(continent) — returns countries in a continent
- Added log_debug(msg) — debug output visible with GEOLOCATION_DEBUG=1
- Added is_autodetected flag to UserLocation dataclass
- Preserved all existing REGION_MAP, CONTINENT_MAP, SUBREGION_MAP data

src/ui/layout.py:
- render_header() accepts manual_region, manual_country, manual_continent, location_warning
- render_filters() now returns 6 values: continent, region, country, commodity, search, refresh
- Added continent selector to the filter bar
- Dynamic location text in 4 formats depending on detection/manual/global state
- Browser geolocation UI removed per user feedback

app.py:
- Added get_client_ip_from_streamlit() — extracts headers from st.context.headers
- Added detect_user_location() — handles test IP override vs real detection
- Debug expander with test IP text input (widget key separate from stored key)
- Manual override tracking in session state
- Location re-detection when test IP changes
- st.rerun() to refresh page after location change

Test file:

test_geolocation.py:
- Tests header extraction with CF-Connecting-IP, X-Real-IP, True-Client-IP, X-Forwarded-For
- Tests private IP skipping in X-Forwarded-For
- Tests no-headers scenario (returns None)
- Tests private-only IPs (returns None)
- Tests location detection with US IP (8.8.8.8), Australia IP (1.1.1.1), no IP (server-side)
- All tests pass (verified)

How to test locally:

1. Run with debug: GEOLOCATION_DEBUG=1 streamlit run app.py
2. Open http://localhost:8501
3. Expand "🌐 Geolocation Debug" panel
4. Type 1.1.1.1 and press Enter → should show Australia / Oceania
5. Type 8.8.8.8 and press Enter → should show United States / North America
6. Clear field and press Enter → should show your real location

For command-line testing: python3 test_geolocation.py

Important notes:
- Localhost + VPN does NOT work because the browser connects directly to 127.0.0.1, bypassing the VPN. No proxy headers are sent.
- Header-based detection (CF-Connecting-IP, X-Forwarded-For) only works when deployed behind Cloudflare/NGINX or similar proxy.
- Server-side fallback is essential for local development.
- Browser geolocation (navigator.geolocation) was removed per user request.

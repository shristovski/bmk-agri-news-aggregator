Fix the user geolocation detection logic.

Current problem:
The app sometimes shows "The Dalles / United States / North America" for all users, including users located in North Macedonia. This likely means the app is detecting the hosting server/proxy IP address instead of the real visitor IP, or the detected location is being cached globally.

Changes implemented:

1. Refactored the geolocation module to extract the real client IP from request headers first:
   - CF-Connecting-IP
   - True-Client-IP
   - X-Real-IP
   - X-Forwarded-For

2. For X-Forwarded-For:
   - parses the first public IP in the comma-separated list
   - ignores private/internal IPs such as 127.0.0.1, 10.x.x.x, 172.16-31.x.x, 192.168.x.x

3. Location detection is per user/session via `st.session_state`:
   - Not cached globally or reused across visitors
   - Each session detects separately

4. Safe fallback chain:
   - First: extract real client IP from headers (for production behind Cloudflare/CDN/proxy)
   - Second: if no client IP found (local dev, direct connection), fall back to server-side ipapi.co/json & ipinfo.io/json — this detects the machine's own IP
   - Third: if all providers fail, show "Global Agriculture News"
   - Never defaults to USA or The Dalles
   - Shows a warning banner: "Automatic location detection is unavailable. Showing global news."

5. Manual override controls:
   - Continent selector
   - Region selector
   - Country selector
   - Commodity selector
   - Manual selection overrides automatic IP detection
   - Session state tracks whether user has deviated from detected location

6. Browser geolocation fallback: REMOVED
   - Originally specified as optional item 7
   - Removed per user feedback: "I do not want the button 'Use Browser Location'"

7. Debugging output (hidden in production):
   - Enabled via `GEOLOCATION_DEBUG=1` environment variable
   - Shows: raw headers, selected client IP, geolocation provider response, final country/region/continent

8. Updated UI text — shows one of:
   - "City / Country / Region / Continent" (auto-detected with city)
   - "Country / Region / Continent" (auto-detected without city)
   - "Showing manually selected continent/region/country: ..." (manual override)
   - "Showing global agriculture news" (no detection)

9. Tests/debug functions verified:
   - Private IP detection: 127.0.0.1, 10.x.x.x, 192.168.x.x, localhost all correctly identified
   - Client IP extraction: CF-Connecting-IP, X-Real-IP, True-Client-IP, X-Forwarded-For all parsed
   - X-Forwarded-For with mixed private/public IPs: skips private, returns first public
   - No headers: returns None
   - Private-only IPs: returns None
   - Fallback with no client IP: server-side detection works (returns actual location)

10. Additional changes beyond original spec:
    - Added `is_autodetected` flag to `UserLocation` dataclass to distinguish auto-detected from default
    - Added `get_all_continents()` helper for the continent selector
    - Added `get_countries_for_continent()` helper for filtering countries by continent
    - `render_filters()` now returns 6 values: continent, region, country, commodity, search, refresh
    - Server-side fallback is essential for local development where proxy headers don't exist

Important:
The app never uses the hosting server IP as the default user location when a real client IP is available. Client IP from headers always takes priority. Server-side detection is only used as a fallback when no proxy headers are present (local dev).

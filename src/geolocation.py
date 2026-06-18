import os
import requests
from dataclasses import dataclass
from typing import Optional

DEBUG = os.getenv("GEOLOCATION_DEBUG", "0") == "1"


@dataclass
class UserLocation:
    city: str
    country: str
    country_code: str
    region: str
    continent: str
    latitude: float = 0.0
    longitude: float = 0.0
    is_autodetected: bool = False


_PRIVATE_IP_PREFIXES = (
    "127.", "10.", "172.16.", "172.17.", "172.18.", "172.19.",
    "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
    "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
    "172.30.", "172.31.", "192.168.", "169.254.", "0.",
)
_PRIVATE_IP_EXACT = {"127.0.0.1", "::1", "localhost"}

REGION_MAP = {
    "North Macedonia": "Balkans",
    "Serbia": "Balkans",
    "Albania": "Balkans",
    "Kosovo": "Balkans",
    "Bosnia and Herzegovina": "Balkans",
    "Montenegro": "Balkans",
    "Croatia": "Balkans",
    "Slovenia": "Balkans",
    "Bulgaria": "Balkans",
    "Romania": "Balkans",
    "Greece": "Balkans",
    "Turkey": "Balkans",
    "Germany": "Western Europe",
    "France": "Western Europe",
    "United Kingdom": "Western Europe",
    "Italy": "Western Europe",
    "Spain": "Western Europe",
    "Portugal": "Western Europe",
    "Netherlands": "Western Europe",
    "Belgium": "Western Europe",
    "Austria": "Western Europe",
    "Switzerland": "Western Europe",
    "Ireland": "Western Europe",
    "Poland": "Central Europe",
    "Czech Republic": "Central Europe",
    "Slovakia": "Central Europe",
    "Hungary": "Central Europe",
    "Ukraine": "Eastern Europe",
    "Russia": "Eastern Europe",
    "Belarus": "Eastern Europe",
    "Moldova": "Eastern Europe",
    "USA": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Brazil": "South America",
    "Argentina": "South America",
    "Chile": "South America",
    "Colombia": "South America",
    "Peru": "South America",
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "China": "East Asia",
    "India": "South Asia",
    "Japan": "East Asia",
    "South Korea": "East Asia",
    "Indonesia": "Southeast Asia",
    "Thailand": "Southeast Asia",
    "Vietnam": "Southeast Asia",
    "Philippines": "Southeast Asia",
    "Nigeria": "West Africa",
    "South Africa": "Southern Africa",
    "Kenya": "East Africa",
    "Ethiopia": "East Africa",
    "Egypt": "North Africa",
    "Morocco": "North Africa",
    "Algeria": "North Africa",
    "Tunisia": "North Africa",
    "Saudi Arabia": "Middle East",
    "UAE": "Middle East",
    "Israel": "Middle East",
    "Iran": "Middle East",
    "Iraq": "Middle East",
    "Jordan": "Middle East",
    "Pakistan": "South Asia",
    "Bangladesh": "South Asia",
}

CONTINENT_MAP = {
    "Balkans": "Europe",
    "Southeast Europe": "Europe",
    "Western Europe": "Europe",
    "Central Europe": "Europe",
    "Eastern Europe": "Europe",
    "North America": "North America",
    "South America": "South America",
    "Oceania": "Oceania",
    "East Asia": "Asia",
    "South Asia": "Asia",
    "Southeast Asia": "Asia",
    "West Africa": "Africa",
    "Southern Africa": "Africa",
    "East Africa": "Africa",
    "North Africa": "Africa",
    "Middle East": "Middle East",
}

SUBREGION_MAP = {
    "Balkans": "Southeast Europe",
    "Western Europe": "Western Europe",
    "Central Europe": "Central Europe",
    "Eastern Europe": "Eastern Europe",
    "North America": "North America",
    "South America": "South America",
    "Oceania": "Oceania",
    "East Asia": "East Asia",
    "South Asia": "South Asia",
    "Southeast Asia": "Southeast Asia",
    "West Africa": "West Africa",
    "Southern Africa": "Southern Africa",
    "East Africa": "East Africa",
    "North Africa": "North Africa",
    "Middle East": "Middle East",
}


def log_debug(msg: str):
    if DEBUG:
        import streamlit as st
        st.write(f"<div style='font-size:0.75rem;color:#888;background:#f5f5f5;padding:2px 6px;'><strong>🌐 GEO:</strong> {msg}</div>", unsafe_allow_html=True)


def is_private_ip(ip: str) -> bool:
    ip = ip.strip()
    if ip in _PRIVATE_IP_EXACT:
        return True
    for prefix in _PRIVATE_IP_PREFIXES:
        if ip.startswith(prefix):
            return True
    return False


def extract_client_ip(headers: dict) -> Optional[str]:
    debug_info = {}

    cf = headers.get("CF-Connecting-IP") or headers.get("cf-connecting-ip")
    if cf:
        debug_info["CF-Connecting-IP"] = cf
        if not is_private_ip(cf):
            log_debug(f"Using CF-Connecting-IP: {cf}")
            return cf

    tci = headers.get("True-Client-IP") or headers.get("true-client-ip")
    if tci:
        debug_info["True-Client-IP"] = tci
        if not is_private_ip(tci):
            log_debug(f"Using True-Client-IP: {tci}")
            return tci

    xri = headers.get("X-Real-IP") or headers.get("x-real-ip")
    if xri:
        debug_info["X-Real-IP"] = xri
        if not is_private_ip(xri):
            log_debug(f"Using X-Real-IP: {xri}")
            return xri

    xff = headers.get("X-Forwarded-For") or headers.get("x-forwarded-for")
    if xff:
        debug_info["X-Forwarded-For"] = xff
        ips = [ip.strip() for ip in xff.split(",")]
        for ip in ips:
            if not is_private_ip(ip):
                log_debug(f"Using X-Forwarded-For first public IP: {ip}")
                return ip
        log_debug("X-Forwarded-For contained only private IPs")

    log_debug(f"No valid client IP found in headers. Headers checked: {list(debug_info.keys()) or 'none'}")
    return None


def _parse_ipapi_response(data: dict) -> UserLocation:
    country = data.get("country_name", "Global")
    country_code = data.get("country_code", "")
    city = data.get("city", "Unknown")
    region = REGION_MAP.get(country, "Global")
    continent_code = data.get("continent_code", "")
    continent_map = {
        "EU": "Europe", "NA": "North America", "SA": "South America",
        "AS": "Asia", "AF": "Africa", "OC": "Oceania", "AN": "Antarctica",
    }
    continent = continent_map.get(continent_code, "Global")
    if region == "Global" and continent != "Global":
        region = continent
    lat = data.get("latitude", 0.0)
    lon = data.get("longitude", 0.0)
    return UserLocation(
        city=city, country=country, country_code=country_code,
        region=region, continent=continent, latitude=lat, longitude=lon,
        is_autodetected=True,
    )


def _parse_ipinfo_response(data: dict) -> UserLocation:
    country_code = data.get("country", "Global")
    country_full = {
        "US": "USA", "GB": "United Kingdom", "DE": "Germany",
        "FR": "France", "IT": "Italy", "ES": "Spain",
        "CA": "Canada", "AU": "Australia", "BR": "Brazil",
        "IN": "India", "CN": "China", "JP": "Japan",
        "RU": "Russia", "ZA": "South Africa", "MX": "Mexico",
        "AR": "Argentina", "NG": "Nigeria", "KE": "Kenya",
        "EG": "Egypt", "TR": "Turkey", "SA": "Saudi Arabia",
        "MK": "North Macedonia", "RS": "Serbia",
        "MK": "North Macedonia", "RS": "Serbia",
        "BG": "Bulgaria", "RO": "Romania", "GR": "Greece",
        "HR": "Croatia", "SI": "Slovenia", "BA": "Bosnia and Herzegovina",
        "ME": "Montenegro", "AL": "Albania", "XK": "Kosovo",
        "AT": "Austria", "CH": "Switzerland", "NL": "Netherlands",
        "BE": "Belgium", "SE": "Sweden", "NO": "Norway",
        "DK": "Denmark", "FI": "Finland", "PL": "Poland",
        "CZ": "Czech Republic", "SK": "Slovakia", "HU": "Hungary",
        "UA": "Ukraine", "BY": "Belarus", "MD": "Moldova",
    }.get(country_code, country_code)
    city = data.get("city", "Unknown")
    region = REGION_MAP.get(country_full, "Global")
    continent = CONTINENT_MAP.get(region, "Global")
    loc = data.get("loc", "0,0").split(",")
    lat = float(loc[0]) if len(loc) == 2 else 0.0
    lon = float(loc[1]) if len(loc) == 2 else 0.0
    if region == "Global" and continent != "Global":
        region = continent
    return UserLocation(
        city=city, country=country_full, country_code=country_code,
        region=region, continent=continent, latitude=lat, longitude=lon,
        is_autodetected=True,
    )


def detect_location_from_ip(client_ip: str) -> UserLocation:
    log_debug(f"Querying ipapi.co for IP: {client_ip}")
    try:
        resp = requests.get(
            f"https://ipapi.co/{client_ip}/json/",
            timeout=5,
            headers={"User-Agent": "BMKAgriNews/1.0"},
        )
        if resp.status_code == 200:
            data = resp.json()
            if not data.get("error"):
                log_debug(f"ipapi.co response: country={data.get('country_name')}, city={data.get('city')}")
                return _parse_ipapi_response(data)
    except Exception as e:
        log_debug(f"ipapi.co failed: {e}")

    log_debug(f"Falling back to ipinfo.io for IP: {client_ip}")
    try:
        resp = requests.get(
            f"https://ipinfo.io/{client_ip}/json",
            timeout=5,
            headers={"User-Agent": "BMKAgriNews/1.0"},
        )
        if resp.status_code == 200:
            data = resp.json()
            if not data.get("bogon"):
                log_debug(f"ipinfo.io response: country={data.get('country')}, city={data.get('city')}")
                return _parse_ipinfo_response(data)
    except Exception as e:
        log_debug(f"ipinfo.io failed: {e}")

    log_debug("All geolocation providers failed for client IP")
    return get_default_location()


def detect_location(client_ip: Optional[str] = None) -> UserLocation:
    if client_ip:
        log_debug(f"detect_location called with client IP: {client_ip}")
        result = detect_location_from_ip(client_ip)
        if result.country != "Global":
            log_debug(f"Successfully detected: {result.country} / {result.region} / {result.continent}")
            return result
        log_debug("Client IP lookup returned Global, falling back to server-side detection")

    log_debug("Falling back to server-side IP detection")
    try:
        resp = requests.get(
            "https://ipapi.co/json/",
            timeout=5,
            headers={"User-Agent": "BMKAgriNews/1.0"},
        )
        if resp.status_code == 200:
            data = resp.json()
            if not data.get("error"):
                log_debug(f"Server-side ipapi.co: country={data.get('country_name')}, city={data.get('city')}")
                result = _parse_ipapi_response(data)
                result.is_autodetected = True
                return result
    except Exception as e:
        log_debug(f"Server-side ipapi.co failed: {e}")

    try:
        log_debug("Falling back to server-side ipinfo.io")
        resp = requests.get(
            "https://ipinfo.io/json",
            timeout=5,
            headers={"User-Agent": "BMKAgriNews/1.0"},
        )
        if resp.status_code == 200:
            data = resp.json()
            if not data.get("bogon"):
                log_debug(f"Server-side ipinfo.io: country={data.get('country')}, city={data.get('city')}")
                result = _parse_ipinfo_response(data)
                result.is_autodetected = True
                return result
    except Exception as e:
        log_debug(f"Server-side ipinfo.io failed: {e}")

    log_debug("All detection methods failed, defaulting to Global")
    return get_default_location()


def geolocate_from_coords(lat: float, lng: float) -> Optional[UserLocation]:
    log_debug(f"Reverse geocoding coords: {lat}, {lng}")
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lng, "format": "json", "addressdetails": 1},
            timeout=5,
            headers={"User-Agent": "BMKAgriNews/1.0"},
        )
        if resp.status_code == 200:
            data = resp.json()
            address = data.get("address", {})
            country = address.get("country", "Global")
            country_code = address.get("country_code", "").upper()
            city = address.get("city") or address.get("town") or address.get("village") or "Unknown"
            region = REGION_MAP.get(country, "Global")
            continent = CONTINENT_MAP.get(region, "Global")
            if region == "Global" and continent != "Global":
                region = continent
            log_debug(f"Reverse geocode result: {country} / {region} / {continent}")
            return UserLocation(
                city=city, country=country, country_code=country_code,
                region=region, continent=continent, latitude=lat, longitude=lng,
                is_autodetected=True,
            )
    except Exception as e:
        log_debug(f"Reverse geocoding failed: {e}")
    return None


def get_default_location() -> UserLocation:
    return UserLocation(
        city="", country="Global", country_code="",
        region="Global", continent="Global",
    )


def get_all_regions() -> list[str]:
    return ["Global"] + sorted(set(REGION_MAP.values()))


def get_all_continents() -> list[str]:
    continents = sorted(set(CONTINENT_MAP.values()))
    return ["Global"] + continents


def get_countries_for_region(region: str) -> list[str]:
    if region == "Global":
        return ["Global"]
    return [c for c, r in REGION_MAP.items() if r == region]


def get_countries_for_continent(continent: str) -> list[str]:
    if continent == "Global":
        return ["Global"]
    regions = [r for r, c in CONTINENT_MAP.items() if c == continent]
    countries = [c for c, r in REGION_MAP.items() if r in regions]
    return sorted(set(countries))

import requests
from dataclasses import dataclass


@dataclass
class UserLocation:
    city: str
    country: str
    country_code: str
    region: str
    continent: str
    latitude: float = 0.0
    longitude: float = 0.0


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


def map_to_region(country: str) -> str:
    return REGION_MAP.get(country, "Global")


def map_to_continent(region: str) -> str:
    return CONTINENT_MAP.get(region, "Global")


def map_to_subregion(region: str) -> str:
    return SUBREGION_MAP.get(region, "Global")


def get_region_hierarchy(country: str) -> tuple[str, str, str, str]:
    region = map_to_region(country)
    subregion = map_to_subregion(region)
    continent = map_to_continent(region)
    return country, region, subregion, continent


def get_default_location() -> UserLocation:
    return UserLocation(
        city="Unknown",
        country="Global",
        country_code="",
        region="Global",
        continent="Global",
    )


def detect_location() -> UserLocation:
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            country = data.get("country_name", "Global")
            country_code = data.get("country_code", "")
            city = data.get("city", "Unknown")
            region = map_to_region(country)
            continent_code = data.get("continent_code", "")
            continent_map = {
                "EU": "Europe",
                "NA": "North America",
                "SA": "South America",
                "AS": "Asia",
                "AF": "Africa",
                "OC": "Oceania",
                "AN": "Antarctica",
            }
            continent = continent_map.get(continent_code, "Global")
            if region == "Global" and continent != "Global":
                region = continent
            lat = data.get("latitude", 0.0)
            lon = data.get("longitude", 0.0)
            return UserLocation(
                city=city,
                country=country,
                country_code=country_code,
                region=region,
                continent=continent,
                latitude=lat,
                longitude=lon,
            )
    except Exception:
        pass

    try:
        resp = requests.get("https://ipinfo.io/json", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            country = data.get("country", "Global")
            country_full = {
                "US": "USA", "GB": "United Kingdom", "DE": "Germany",
                "FR": "France", "IT": "Italy", "ES": "Spain",
                "CA": "Canada", "AU": "Australia", "BR": "Brazil",
                "IN": "India", "CN": "China", "JP": "Japan",
                "RU": "Russia", "ZA": "South Africa", "MX": "Mexico",
                "AR": "Argentina", "NG": "Nigeria", "KE": "Kenya",
                "EG": "Egypt", "TR": "Turkey", "SA": "Saudi Arabia",
                "MK": "North Macedonia", "RS": "Serbia",
            }.get(country, country)
            city = data.get("city", "Unknown")
            region = map_to_region(country_full)
            continent = map_to_continent(region)
            loc = data.get("loc", "0,0").split(",")
            lat = float(loc[0]) if len(loc) == 2 else 0.0
            lon = float(loc[1]) if len(loc) == 2 else 0.0
            return UserLocation(
                city=city,
                country=country_full,
                country_code=country,
                region=region,
                continent=continent,
                latitude=lat,
                longitude=lon,
            )
    except Exception:
        pass

    return get_default_location()


def get_all_regions() -> list[str]:
    regions = sorted(set(REGION_MAP.values()))
    return ["Global"] + regions


def get_countries_for_region(region: str) -> list[str]:
    if region == "Global":
        return ["Global"]
    return [c for c, r in REGION_MAP.items() if r == region]

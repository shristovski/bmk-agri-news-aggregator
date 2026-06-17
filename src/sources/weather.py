from typing import Optional
from src.config import OPENWEATHER_API_KEY

DEMO_WEATHER_RISKS = [
    {
        "location": "Midwest USA",
        "risk_type": "drought risk",
        "severity": "moderate",
        "description": "Below-average precipitation forecast for the next 2 weeks across parts of Iowa and Illinois.",
        "date": "2026-06-17",
    },
    {
        "location": "Southern Europe",
        "risk_type": "heat stress",
        "severity": "high",
        "description": "Temperatures expected to exceed 38°C in Spain and Portugal, threatening olive and grape crops.",
        "date": "2026-06-17",
    },
    {
        "location": "Argentina",
        "risk_type": "frost risk",
        "severity": "moderate",
        "description": "Late-season frost warning for central agricultural regions.",
        "date": "2026-06-17",
    },
    {
        "location": "Southeast Asia",
        "risk_type": "rainfall forecast",
        "severity": "high",
        "description": "Heavy monsoon rains expected in Vietnam and Thailand, potential flooding in rice-growing areas.",
        "date": "2026-06-17",
    },
    {
        "location": "East Africa",
        "risk_type": "drought risk",
        "severity": "severe",
        "description": "Continued below-normal rainfall in the Horn of Africa affecting livestock and staple crops.",
        "date": "2026-06-17",
    },
    {
        "location": "Black Sea Region",
        "risk_type": "storm warnings",
        "severity": "moderate",
        "description": "Severe thunderstorms forecast for Ukraine and southern Russia, risk of crop damage.",
        "date": "2026-06-17",
    },
]


def fetch_weather_risks(lat: float = 0.0, lon: float = 0.0) -> list[dict]:
    if not OPENWEATHER_API_KEY:
        return DEMO_WEATHER_RISKS

    try:
        import requests

        current = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=5,
        )
        forecast = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"},
            timeout=5,
        )

        risks = []

        if current.status_code == 200:
            data = current.json()
            temp = data.get("main", {}).get("temp", 20)
            weather = data.get("weather", [{}])[0].get("main", "")

            if temp > 35:
                risks.append(
                    {
                        "location": "Your Area",
                        "risk_type": "heat stress",
                        "severity": "high",
                        "description": f"Current temperature is {temp}°C. Heat stress risk for crops.",
                        "date": "2026-06-17",
                    }
                )

            if "storm" in weather.lower() or "thunderstorm" in weather.lower():
                risks.append(
                    {
                        "location": "Your Area",
                        "risk_type": "storm warnings",
                        "severity": "high",
                        "description": f"{weather} conditions detected. Potential crop damage risk.",
                        "date": "2026-06-17",
                    }
                )

        if risks:
            return risks

    except Exception:
        pass

    return DEMO_WEATHER_RISKS

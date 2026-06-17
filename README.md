# BMK Global Agri News

A web-based agriculture news aggregator that automatically detects the user's location and surfaces the most relevant agriculture, commodity, weather, and market news from global RSS sources.

Built as a Streamlit MVP with a clean modular architecture designed for future migration to FastAPI + Next.js.

## Features

- **IP-based location detection** — automatically shows relevant news for your country, region, and continent
- **RSS aggregation** — fetches from USDA, FAO, EC Agriculture, World Bank, and top agriculture publications
- **Smart classification** — automatically categorizes articles into Weather Risk, Commodities, Market Prices, Policy & Trade, and more
- **Commodity tagging** — detects mentions of wheat, corn, soybeans, coffee, sugar, and other key commodities
- **Relevance ranking** — scores articles by location relevance, freshness, source reliability, and commodity match
- **Deduplication** — removes duplicate and near-duplicate articles
- **SQLite caching** — stores articles locally to reduce fetch frequency
- **Market prices** — live via Trading Economics API (or demo data)
- **Weather risks** — weather alerts via OpenWeather API (or demo data)
- **Manual filters** — override region, country, and commodity filters manually

## Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone <repository-url>
cd bmk-agri-news-aggregator
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and configure API keys (optional — the app works with demo data):

```bash
cp .env.example .env
```

Edit `.env`:

| Variable | Required | Description |
|---|---|---|
| `FIRECRAWL_API_KEY` | No | For scraping sites without RSS feeds |
| `TRADING_ECONOMICS_API_KEY` | No | Live market prices; shows demo data without this |
| `OPENWEATHER_API_KEY` | No | Live weather data; shows demo data without this |
| `NEWS_REFRESH_INTERVAL_MINUTES` | No | How often to refresh cached articles (default: 60) |

### Run

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Project Structure

```
bmk-agri-news-aggregator/
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── README.md                 # This file
└── src/
    ├── config.py             # Configuration from environment
    ├── geolocation.py        # IP-based location detection + region mapping
    ├── sources/
    │   ├── rss_sources.py    # RSS feed definitions and fetch logic
    │   ├── firecrawl_sources.py  # Firecrawl web extraction (placeholder)
    │   ├── trading_economics.py  # Market prices API + demo data
    │   └── weather.py        # Weather risk data + demo data
    ├── news/
    │   ├── fetcher.py        # Orchestrates fetching from all sources
    │   ├── classifier.py     # Category and commodity keyword classification
    │   ├── ranking.py        # Relevance scoring algorithm
    │   ├── deduplication.py  # Duplicate and near-duplicate detection
    │   └── summarizer.py     # Text summarization helper
    ├── storage/
    │   └── database.py       # SQLite cache layer
    └── ui/
        ├── layout.py         # Header + filter controls
        ├── components.py     # Article cards, market price cards, weather cards
        └── styles.py         # Custom CSS (injected via st.markdown)
```

## How IP-Based Localization Works

1. On first load, the app calls `ipapi.co/json` to detect the user's IP location
2. The country is mapped to a region (e.g., "North Macedonia" → "Balkans")
3. The region is mapped to a continent (e.g., "Balkans" → "Europe")
4. Articles are ranked based on proximity to the user's location hierarchy
5. If IP detection fails, the app defaults to a global view
6. Falls back to `ipinfo.io/json` if the primary service is unavailable

## Adding New RSS Sources

Edit `src/sources/rss_sources.py` and add a new entry to the `RSS_FEEDS` list:

```python
{
    "name": "Source Name",
    "url": "https://example.com/rss",
    "default_category": "General Agriculture",
    "region": "Region Name",
    "country": "Country Name",
    "continent": "Continent Name",
    "reliability": 7,  # 1-10
}
```

## Roadmap

- [ ] Firecrawl integration for non-RSS sources (Reuters, Bloomberg)
- [ ] Live weather risk maps
- [ ] Historical market price charts
- [ ] User accounts and saved preferences
- [ ] Email/notification alerts for commodity price movements
- [ ] FastAPI backend + Next.js frontend migration
- [ ] Multilingual article support
- [ ] Mobile app

## License

Proprietary — BMK Global

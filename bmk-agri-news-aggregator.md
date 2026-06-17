Create a brand new project from scratch called `bmk-agri-news-aggregator`.

The goal is to build a web application similar in concept to time.mk, but focused only on agriculture, commodities, agri-weather, and market news.

Do not reuse the previous report-generator structure. Build a clean new architecture.

Main product idea:
The application should be an agriculture news aggregator. When a user opens the website, the app should automatically detect the user's approximate location from their IP address and show the most relevant agriculture news for their city, country, region, and continent. The user must also be able to manually switch region, country, and commodity filters.

Important:
Do not hardcode North Macedonia or any specific country. The location should be detected dynamically from the user's IP address. If IP detection fails, default to a global agriculture news view.

Technology stack:

* Use Streamlit for the first MVP frontend.
* Use Python.
* Use SQLite for local caching of fetched articles.
* Use RSS feeds where possible.
* Use Firecrawl or simple web extraction only for sources that do not provide RSS.
* Structure the code cleanly so we can later migrate to FastAPI + Next.js if needed.

Homepage layout:
The app should not use a left sidebar as the main navigation. Instead, create a top banner/header similar to a news website.

Header should include:

* BMK Global Agri News
* Detected location text, for example: “Showing agriculture news for: North Macedonia / Balkans / Europe”
* Region selector
* Country selector
* Commodity selector
* Search input
* Refresh news button

Homepage sections:

1. Top Agriculture News
2. Local & Regional Agriculture News
3. Weather Risk for Agriculture
4. Commodity Market News
5. Market Prices / Finance
6. Policy, Trade & Export/Import

Each section should display article cards with:

* title
* source name
* short summary
* published date
* image if available
* category tag
* commodity tags
* region tag
* link to original article

Design:

* Make it look like a modern news aggregator.
* Cards should be clean and visual.
* Use a grid layout.
* Top stories should be larger cards.
* Secondary stories should be smaller cards.
* Use BMK Global branding style.
* Avoid a dashboard-heavy look. It should feel more like a news portal.

News sources to include:

* Barchart commodity news
* Reuters commodities / agriculture pages where available
* Bloomberg commodities page where available
* Trading Economics commodities/news API or pages
* USDA RSS feeds
* European Commission Agriculture newsroom RSS
* FAO agriculture / food security news
* Additional open RSS sources related to agriculture, commodities, crops, weather, fertilizer, trade, and policy

Important note:
Some sources may not provide RSS. For those, create a placeholder connector structure where Firecrawl extraction can be used later. The app should not break if a source is unavailable.

IP/location logic:
Create a module for geolocation:

* Detect approximate country, city, region, and continent from IP.
* Map country to broader region.
  Examples:

  * North Macedonia -> Balkans -> Southeast Europe -> Europe
  * Serbia -> Balkans -> Southeast Europe -> Europe
  * Germany -> Western Europe -> Europe
  * USA -> North America
  * Australia -> Oceania
    If local detection fails, use Global.

News ranking logic:
Each article should receive a relevance score based on:

* location relevance
* commodity relevance
* freshness
* source reliability
* category match
* user-selected filters

Deduplication:
Implement basic duplicate detection:

* Normalize article titles
* Remove exact duplicates
* Group very similar stories under the same topic if possible

Categories:
Automatically classify articles into:

* General Agriculture
* Weather Risk
* Commodities
* Market Prices
* Policy & Trade
* Export/Import
* Fertilizer & Inputs
* Crop Production
* Food Security

Commodities:
Support at least:

* Wheat
* Corn
* Soybeans
* Barley
* Rice
* Sunflower
* Sugar
* Coffee
* Cocoa
* Cotton
* Fertilizer

Weather section:
For the MVP, create a Weather Risk section using an open weather API if possible, or create a placeholder that displays weather-risk related news. Later this should support:

* drought risk
* rainfall forecast
* heat stress
* frost risk
* soil moisture
* storm warnings

Market prices section:
Create a placeholder market prices component for:

* Wheat
* Corn
* Soybeans
* Coffee
* Cocoa
* Sugar
  Use Trading Economics or another available API if configured. If no API key is available, show demo/mock values clearly marked as demo data.

Environment variables:
Create a `.env.example` file with:
FIRECRAWL_API_KEY=
TRADING_ECONOMICS_API_KEY=
OPENWEATHER_API_KEY=
NEWS_REFRESH_INTERVAL_MINUTES=60

Project structure:
Use a clean folder structure:

bmk-agri-news-aggregator/
app.py
requirements.txt
.env.example
README.md
src/
config.py
geolocation.py
sources/
rss_sources.py
firecrawl_sources.py
trading_economics.py
weather.py
news/
fetcher.py
classifier.py
ranking.py
deduplication.py
summarizer.py
storage/
database.py
ui/
layout.py
components.py
styles.py

README:
Create a full README with:

* project description
* setup instructions
* how to run locally
* how to add new RSS sources
* how to configure API keys
* how IP-based localization works
* future roadmap

Commands:
The app should run with:
pip install -r requirements.txt
streamlit run app.py

Deliverables:

* Complete working MVP
* Clean UI
* Local article caching
* RSS fetching
* IP-based location detection
* Manual region/commodity filters
* Placeholder support for Firecrawl, Trading Economics, and weather APIs
* README documentation

Important:
Focus on creating the new product foundation, not on perfect data coverage. The first version should work even with partial sources and should be easy to extend.

import streamlit as st

st.set_page_config(
    page_title="BMK Global Agri News",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.config import CATEGORIES, COMMODITIES
from src.geolocation import detect_location, get_all_regions, get_countries_for_region
from src.storage.database import Database
from src.news.fetcher import get_articles, refresh_articles, fetch_and_store_articles
from src.news.ranking import rank_articles, filter_by_category
from src.sources.trading_economics import fetch_market_prices, is_demo_data
from src.sources.weather import fetch_weather_risks
from src.ui.styles import apply_custom_css
from src.ui.layout import render_header, render_filters
from src.ui.components import (
    render_top_stories,
    render_article_grid,
    render_market_prices,
    render_weather_risks,
    render_section_header,
)


def main():
    apply_custom_css()

    if "user_location" not in st.session_state:
        with st.spinner("Detecting your location..."):
            st.session_state.user_location = detect_location()

    if "db" not in st.session_state:
        st.session_state.db = Database()

    if "articles_fetched" not in st.session_state:
        with st.spinner("Fetching latest agriculture news..."):
            count = fetch_and_store_articles(st.session_state.db)
            st.session_state.articles_fetched = True
            if count > 0:
                st.toast(f"Loaded {count} articles!", icon="🌾")

    user_location = st.session_state.user_location
    db = st.session_state.db

    regions = get_all_regions()
    countries = get_countries_for_region(user_location.region if user_location else "Global")

    render_header(user_location)

    selected_region, selected_country, selected_commodity, search_query, refresh = render_filters(
        regions, countries, COMMODITIES, user_location
    )

    if refresh:
        with st.spinner("Refreshing news..."):
            count = refresh_articles(db)
            if count > 0:
                st.toast(f"Loaded {count} new articles!", icon="🌾")
            st.rerun()

    articles = get_articles(db)

    if search_query:
        articles = [
            a
            for a in articles
            if search_query.lower() in a.get("title", "").lower()
            or search_query.lower() in a.get("summary", "").lower()
        ]

    ranked_articles = rank_articles(
        articles,
        user_location=user_location if selected_region == "Global" and selected_country == "Global" else None,
        selected_region=selected_region,
        selected_country=selected_country,
        selected_commodity=selected_commodity,
    )

    # ====== SECTION 1: Top Agriculture News ======
    render_section_header("Top Agriculture News")
    render_top_stories(ranked_articles, count=4)

    # ====== SECTION 2: Local & Regional Agriculture News ======
    render_section_header("Local & Regional Agriculture News")
    if user_location and user_location.region != "Global":
        local_articles = [
            a
            for a in ranked_articles
            if a.get("region") == user_location.region
            or a.get("continent") == user_location.continent
        ]
        if local_articles:
            render_article_grid(local_articles[:9], cols_count=3)
        else:
            st.info(f"No region-specific articles found for {user_location.region}. Showing top stories instead.")
            render_article_grid(ranked_articles[4:13], cols_count=3)
    else:
        render_article_grid(ranked_articles[4:13], cols_count=3)

    # ====== SECTION 3: Weather Risk for Agriculture ======
    render_section_header("Weather Risk for Agriculture")
    weather_col1, weather_col2 = st.columns([1, 2])
    with weather_col1:
        weather_risks = fetch_weather_risks(
            user_location.latitude if user_location else 0.0,
            user_location.longitude if user_location else 0.0,
        )
        render_weather_risks(weather_risks[:3])
    with weather_col2:
        weather_articles = filter_by_category(ranked_articles, "Weather Risk")
        if weather_articles:
            render_article_grid(weather_articles[:4], cols_count=2)
        else:
            st.info("No weather-related articles available at this time.")

    # ====== SECTION 4: Commodity Market News ======
    render_section_header("Commodity Market News")
    commodity_articles = filter_by_category(ranked_articles, "Commodities")
    if not commodity_articles:
        commodity_articles = filter_by_category(ranked_articles, "Market Prices")
    if commodity_articles:
        render_article_grid(commodity_articles[:9], cols_count=3)
    else:
        # If no commodity-specific articles, show some ranked articles
        render_article_grid(ranked_articles[:9], cols_count=3)

    # ====== SECTION 5: Market Prices / Finance ======
    render_section_header("Market Prices / Finance")
    prices = fetch_market_prices()
    is_demo = is_demo_data()
    render_market_prices(prices, is_demo)

    # ====== SECTION 6: Policy, Trade & Export/Import ======
    render_section_header("Policy, Trade & Export/Import")
    policy_articles = filter_by_category(ranked_articles, "Policy & Trade")
    export_articles = filter_by_category(ranked_articles, "Export/Import")
    policy_articles = policy_articles + export_articles
    if policy_articles:
        render_article_grid(policy_articles[:9], cols_count=3)
    else:
        render_article_grid(ranked_articles[:9], cols_count=3)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center;color:#888;font-size:0.8rem;padding:1rem;">
            <strong>BMK Global Agri News</strong> &middot; Agriculture News Aggregator &middot;
            <a href="https://bmkglobal.com" style="color:#2d6a4f;text-decoration:none;">BMK Global</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

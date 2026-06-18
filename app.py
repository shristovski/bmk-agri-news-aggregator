import os
from typing import Optional
import streamlit as st

st.set_page_config(
    page_title="BMK Global Agri News",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.config import CATEGORIES, COMMODITIES
from src.geolocation import (
    detect_location,
    extract_client_ip,
    get_all_regions,
    get_all_continents,
    get_countries_for_region,
    log_debug,
    DEBUG,
)
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


def get_client_ip_from_streamlit() -> Optional[str]:
    try:
        headers = dict(st.context.headers)
        if DEBUG:
            log_debug(f"Raw headers: {dict(headers)}")
        return extract_client_ip(headers)
    except Exception as e:
        if DEBUG:
            log_debug(f"Header extraction error: {e}")
        return None


def main():
    apply_custom_css()

    # ---- INIT SESSION STATE ----
    if "db" not in st.session_state:
        st.session_state.db = Database()

    if "location_detected" not in st.session_state:
        with st.spinner("Detecting your location..."):
            client_ip = get_client_ip_from_streamlit()
            st.session_state.client_ip = client_ip
            user_location = detect_location(client_ip)
            st.session_state.user_location = user_location
            st.session_state.location_detected = True
            st.session_state.location_warning = user_location.country == "Global"

    if "articles_fetched" not in st.session_state:
        with st.spinner("Fetching latest agriculture news..."):
            count = fetch_and_store_articles(st.session_state.db)
            st.session_state.articles_fetched = True
            if count > 0:
                st.toast(f"Loaded {count} articles!", icon="🌾")

    user_location = st.session_state.user_location
    location_warning = st.session_state.location_warning
    db = st.session_state.db

    regions = get_all_regions()
    continents = get_all_continents()
    countries = get_countries_for_region(user_location.region if user_location else "Global")

    # ---- CHECK MANUAL OVERRIDES ----
    has_manual_override = (
        st.session_state.get("manual_continent", "Global") != "Global"
        or st.session_state.get("manual_region", "Global") != "Global"
        or st.session_state.get("manual_country", "Global") != "Global"
    )

    if has_manual_override:
        manual_continent = st.session_state.get("manual_continent", "Global")
        manual_region = st.session_state.get("manual_region", "Global")
        manual_country = st.session_state.get("manual_country", "Global")
    else:
        manual_continent = ""
        manual_region = ""
        manual_country = ""

    # ---- RENDER HEADER ----
    render_header(
        user_location,
        manual_region=manual_region,
        manual_country=manual_country,
        manual_continent=manual_continent,
        location_warning=location_warning and not has_manual_override,
    )

    # ---- RENDER FILTERS ----
    selected_continent, selected_region, selected_country, selected_commodity, search_query, refresh = render_filters(
        regions, countries, continents, COMMODITIES, user_location,
    )

    # Store manual overrides in session state
    st.session_state.manual_continent = selected_continent if selected_continent != user_location.continent else "Global"
    st.session_state.manual_region = selected_region if selected_region != user_location.region else "Global"
    st.session_state.manual_country = selected_country if selected_country != user_location.country else "Global"

    if refresh:
        with st.spinner("Refreshing news..."):
            count = refresh_articles(db)
            if count > 0:
                st.toast(f"Loaded {count} new articles!", icon="🌾")
            st.rerun()

    # ---- FETCH ARTICLES ----
    articles = get_articles(db)

    if search_query:
        articles = [
            a for a in articles
            if search_query.lower() in a.get("title", "").lower()
            or search_query.lower() in a.get("summary", "").lower()
        ]

    ranked_articles = rank_articles(
        articles,
        user_location=user_location if not has_manual_override else None,
        selected_region=selected_region,
        selected_country=selected_country,
        selected_commodity=selected_commodity,
    )

    # ---- DEBUG OUTPUT ----
    if DEBUG:
        with st.expander("🌐 Geolocation Debug", expanded=True):
            st.code(
                f"Client IP: {st.session_state.get('client_ip', 'N/A')}\n"
                f"Detected: {user_location.country} / {user_location.region} / {user_location.continent}\n"
                f"Auto-detected: {user_location.is_autodetected}\n"
                f"Manual override: {has_manual_override}\n"
                f"Warning: {location_warning}\n"
                f"Headers: {dict(st.context.headers) if hasattr(st, 'context') else 'N/A'}"
            )

    # ---- SECTION 1: Top Agriculture News ----
    render_section_header("Top Agriculture News")
    render_top_stories(ranked_articles, count=4)

    # ---- SECTION 2: Local & Regional Agriculture News ----
    render_section_header("Local & Regional Agriculture News")
    effective_region = manual_region or (user_location.region if user_location else "Global")
    effective_continent = manual_continent or (user_location.continent if user_location else "Global")

    if effective_region != "Global":
        local_articles = [
            a for a in ranked_articles
            if a.get("region") == effective_region or a.get("continent") == effective_continent
        ]
        if local_articles:
            render_article_grid(local_articles[:9], cols_count=3)
        else:
            st.info(f"No region-specific articles found for {effective_region}. Showing top stories instead.")
            render_article_grid(ranked_articles[4:13], cols_count=3)
    else:
        render_article_grid(ranked_articles[4:13], cols_count=3)

    # ---- SECTION 3: Weather Risk for Agriculture ----
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

    # ---- SECTION 4: Commodity Market News ----
    render_section_header("Commodity Market News")
    commodity_articles = filter_by_category(ranked_articles, "Commodities")
    if not commodity_articles:
        commodity_articles = filter_by_category(ranked_articles, "Market Prices")
    if commodity_articles:
        render_article_grid(commodity_articles[:9], cols_count=3)
    else:
        render_article_grid(ranked_articles[:9], cols_count=3)

    # ---- SECTION 5: Market Prices / Finance ----
    render_section_header("Market Prices / Finance")
    prices = fetch_market_prices()
    is_demo = is_demo_data()
    render_market_prices(prices, is_demo)

    # ---- SECTION 6: Policy, Trade & Export/Import ----
    render_section_header("Policy, Trade & Export/Import")
    policy_articles = filter_by_category(ranked_articles, "Policy & Trade")
    export_articles = filter_by_category(ranked_articles, "Export/Import")
    policy_articles = policy_articles + export_articles
    if policy_articles:
        render_article_grid(policy_articles[:9], cols_count=3)
    else:
        render_article_grid(ranked_articles[:9], cols_count=3)

    # ---- FOOTER ----
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

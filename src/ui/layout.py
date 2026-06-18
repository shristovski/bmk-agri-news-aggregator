import streamlit as st
from typing import Optional
from src.geolocation import UserLocation


def render_header(user_location: Optional[UserLocation], manual_region: str = "", manual_country: str = "", manual_continent: str = "", location_warning: bool = False):
    if location_warning:
        st.warning("Automatic location detection is unavailable. Showing global news.")

    is_manual = bool(manual_region or manual_country or manual_continent)

    if is_manual:
        parts = ["Showing manually selected"]
        if manual_continent and manual_continent != "Global":
            parts.append(f"continent: {manual_continent}")
        if manual_region and manual_region != "Global":
            parts.append(f"region: {manual_region}")
        if manual_country and manual_country != "Global":
            parts.append(f"country: {manual_country}")
        location_text = ", ".join(parts)
    elif user_location and user_location.country != "Global" and user_location.is_autodetected:
        parts = []
        if user_location.city:
            parts.append(user_location.city)
        if user_location.country:
            parts.append(user_location.country)
        if user_location.region and user_location.region != "Global":
            parts.append(user_location.region)
        if user_location.continent and user_location.continent != "Global":
            parts.append(user_location.continent)
        location_text = " / ".join(parts)
    else:
        location_text = "Showing global agriculture news"

    st.markdown(
        f"""
        <div class="main-header">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div>
                    <h1>🌾 BMK Global Agri News</h1>
                    <div class="subtitle">{location_text}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_filters(
    regions: list[str],
    countries: list[str],
    continents: list[str],
    commodities: list[str],
    user_location: Optional[UserLocation] = None,
):
    st.markdown('<div class="header-controls">', unsafe_allow_html=True)

    default_region = user_location.region if user_location else "Global"
    if default_region not in regions:
        default_region = "Global"

    default_continent = user_location.continent if user_location else "Global"
    if default_continent not in continents:
        default_continent = "Global"

    filter_cols = st.columns([1, 1, 1, 0.8, 0.7, 0.5])

    with filter_cols[0]:
        selected_continent = st.selectbox(
            "CONTINENT",
            options=continents,
            index=continents.index(default_continent) if default_continent in continents else 0,
            key="continent_filter",
        )

    with filter_cols[1]:
        selected_region = st.selectbox(
            "REGION",
            options=regions,
            index=regions.index(default_region) if default_region in regions else 0,
            key="region_filter",
        )

    if selected_region == "Global":
        country_options = ["Global"]
        default_country = "Global"
    else:
        country_options = countries
        default_country = user_location.country if user_location and user_location.country in countries else "Global"

    with filter_cols[2]:
        selected_country = st.selectbox(
            "COUNTRY",
            options=country_options,
            index=country_options.index(default_country) if default_country in country_options else 0,
            key="country_filter",
        )

    with filter_cols[3]:
        selected_commodity = st.selectbox(
            "COMMODITY",
            options=["All"] + commodities,
            key="commodity_filter",
        )

    with filter_cols[4]:
        search = st.text_input("SEARCH", placeholder="Search articles...", key="search_input")

    with filter_cols[5]:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        refresh = st.button("🔄 Refresh", key="refresh_btn", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    return selected_continent, selected_region, selected_country, selected_commodity, search, refresh




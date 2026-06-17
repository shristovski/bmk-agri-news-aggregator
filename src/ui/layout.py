import streamlit as st
from typing import Optional
from src.geolocation import UserLocation


def render_header(user_location: Optional[UserLocation]):
    location_text = "Global"
    if user_location and user_location.country != "Global":
        parts = []
        if user_location.city and user_location.city != "Unknown":
            parts.append(user_location.city)
        if user_location.country:
            parts.append(user_location.country)
        if user_location.region:
            parts.append(user_location.region)
        if user_location.continent:
            parts.append(user_location.continent)
        location_text = " / ".join(parts)

    st.markdown(
        f"""
        <div class="main-header">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div>
                    <h1>🌾 BMK Global Agri News</h1>
                    <div class="subtitle">Showing agriculture news for: {location_text}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_filters(
    regions: list[str],
    countries: list[str],
    commodities: list[str],
    user_location: Optional[UserLocation] = None,
):
    st.markdown('<div class="header-controls">', unsafe_allow_html=True)

    filter_cols = st.columns([1, 1, 1, 1, 1, 0.5])

    default_region = user_location.region if user_location else "Global"
    if default_region not in regions:
        default_region = "Global"

    with filter_cols[0]:
        region = st.selectbox(
            "REGION",
            options=regions,
            index=regions.index(default_region) if default_region in regions else 0,
            key="region_filter",
        )

    if region == "Global":
        country_options = ["Global"]
        default_country = "Global"
    else:
        country_options = countries
        default_country = user_location.country if user_location and user_location.country in countries else "Global"

    with filter_cols[1]:
        country = st.selectbox(
            "COUNTRY",
            options=country_options,
            index=country_options.index(default_country) if default_country in country_options else 0,
            key="country_filter",
        )

    with filter_cols[2]:
        commodity = st.selectbox(
            "COMMODITY",
            options=["All"] + commodities,
            key="commodity_filter",
        )

    with filter_cols[3]:
        search = st.text_input("SEARCH", placeholder="Search articles...", key="search_input")

    with filter_cols[4]:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        refresh = st.button("🔄 Refresh News", key="refresh_btn", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    return region, country, commodity, search, refresh

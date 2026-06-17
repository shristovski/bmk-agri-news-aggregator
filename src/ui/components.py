import streamlit as st
from datetime import datetime


def render_article_card(article: dict, large: bool = False):
    card_class = "article-card large" if large else "article-card"

    html = f'<div class="{card_class}">'

    image_url = article.get("image_url")
    if image_url:
        html += f'<img class="article-image" src="{image_url}" alt="" onerror="this.style.display=\'none\'">'

    html += f'<div class="card-title">{article.get("title", "")}</div>'

    pub_date = article.get("published_date", "")
    formatted_date = ""
    if pub_date:
        try:
            dt = datetime.fromisoformat(pub_date)
            formatted_date = dt.strftime("%b %d, %Y")
        except Exception:
            formatted_date = pub_date[:10]

    source = article.get("source", "Unknown")
    html += f'<div class="card-meta">{source} &middot; {formatted_date}</div>'

    summary = article.get("summary", "")
    if summary:
        html += f'<div class="card-summary">{summary[:200]}{"..." if len(summary) > 200 else ""}</div>'

    html += '<div class="card-tags">'

    category = article.get("category", "")
    if category:
        html += f'<span class="tag tag-category">{category}</span>'

    commodities = article.get("commodities", [])
    for commodity in commodities[:3]:
        html += f'<span class="tag tag-commodity">{commodity}</span>'

    region = article.get("region", "")
    if region:
        html += f'<span class="tag tag-region">{region}</span>'

    html += "</div>"

    link = article.get("url", "")
    if link:
        html += f'<div style="margin-top:0.7rem"><a href="{link}" target="_blank" style="color:#2d6a4f;font-size:0.8rem;font-weight:600;text-decoration:none;">Read full article &rarr;</a></div>'

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


def render_top_stories(articles: list[dict], count: int = 4):
    if not articles:
        st.info("No top stories available.")
        return

    top = articles[:count]
    cols = st.columns(2)

    for i, article in enumerate(top):
        with cols[i % 2]:
            render_article_card(article, large=True)


def render_article_grid(articles: list[dict], cols_count: int = 3):
    if not articles:
        st.info("No articles to display.")
        return

    cols = st.columns(cols_count)
    for i, article in enumerate(articles):
        with cols[i % cols_count]:
            render_article_card(article, large=False)


def render_market_prices(prices: list[dict], is_demo: bool = False):
    if not prices:
        st.info("No market price data available.")
        return

    if is_demo:
        st.markdown(
            '<span class="demo-badge">DEMO DATA</span> &nbsp; Configure TRADING_ECONOMICS_API_KEY for live data.',
            unsafe_allow_html=True,
        )

    cols = st.columns(3)
    for i, price in enumerate(prices):
        with cols[i % 3]:
            change = price.get("change", "0")
            change_str = str(change)
            is_positive = change_str.startswith("+")

            change_class = "positive" if is_positive else "negative"

            st.markdown(
                f"""
                <div class="market-price-card">
                    <div class="commodity-name">{price.get("commodity", "")}</div>
                    <div class="price">${price.get("price", 0):.2f}</div>
                    <div class="change {change_class}">{change_str}</div>
                    <div style="font-size:0.7rem;color:#999;">{price.get("unit", "")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_weather_risks(risks: list[dict]):
    if not risks:
        st.info("No weather risk data available.")
        return

    st.markdown(
        '<span class="demo-badge">DEMO DATA</span> &nbsp; Configure OPENWEATHER_API_KEY for live data.',
        unsafe_allow_html=True,
    )

    for risk in risks:
        severity = risk.get("severity", "moderate")
        st.markdown(
            f"""
            <div class="weather-risk-card {severity}">
                <div style="font-weight:600;font-size:0.95rem;">{risk.get("location", "")}</div>
                <div style="font-size:0.8rem;color:#666;margin:0.2rem 0;">
                    <strong>{risk.get("risk_type", "").title()}</strong> &middot; Severity: {severity.title()}
                </div>
                <div style="font-size:0.85rem;color:#555;">{risk.get("description", "")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_section_header(title: str):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

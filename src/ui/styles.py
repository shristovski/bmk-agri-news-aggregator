import streamlit as st


def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background-color: #f8f9fa;
        }

        .main-header {
            background: linear-gradient(135deg, #1a3c2c 0%, #2d6a4f 100%);
            padding: 1.2rem 2rem;
            border-radius: 0 0 16px 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }

        .main-header h1 {
            color: white;
            font-size: 1.8rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .main-header .subtitle {
            color: rgba(255,255,255,0.85);
            font-size: 0.9rem;
            margin-top: 4px;
        }

        .header-controls {
            background: white;
            padding: 0.8rem 1.5rem;
            border-radius: 10px;
            margin: 0.5rem 0 0 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .filter-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }

        .article-card {
            background: white;
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid rgba(0,0,0,0.04);
            height: 100%;
        }

        .article-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }

        .article-card.large {
            padding: 1.5rem;
        }

        .article-card .card-title {
            font-size: 1rem;
            font-weight: 600;
            color: #1a1a2e;
            line-height: 1.4;
            margin-bottom: 0.5rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .article-card.large .card-title {
            font-size: 1.2rem;
        }

        .article-card .card-meta {
            font-size: 0.78rem;
            color: #888;
            margin-bottom: 0.5rem;
        }

        .article-card .card-summary {
            font-size: 0.85rem;
            color: #555;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .article-card .card-tags {
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
            margin-top: 0.7rem;
        }

        .tag {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        .tag-category {
            background: #e8f5e9;
            color: #2e7d32;
        }

        .tag-commodity {
            background: #fff3e0;
            color: #e65100;
        }

        .tag-region {
            background: #e3f2fd;
            color: #1565c0;
        }

        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1a3c2c;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #2d6a4f;
        }

        .market-price-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            border: 1px solid rgba(0,0,0,0.04);
        }

        .market-price-card .commodity-name {
            font-size: 0.85rem;
            font-weight: 600;
            color: #333;
        }

        .market-price-card .price {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1a3c2c;
            margin: 0.3rem 0;
        }

        .market-price-card .change {
            font-size: 0.85rem;
        }

        .market-price-card .change.positive {
            color: #2e7d32;
        }

        .market-price-card .change.negative {
            color: #c62828;
        }

        .weather-risk-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            border-left: 4px solid;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }

        .weather-risk-card.severe {
            border-left-color: #c62828;
        }

        .weather-risk-card.high {
            border-left-color: #e65100;
        }

        .weather-risk-card.moderate {
            border-left-color: #f9a825;
        }

        .stButton > button {
            background: #2d6a4f;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.4rem 1.2rem;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .stButton > button:hover {
            background: #1a3c2c;
            color: white;
        }

        .demo-badge {
            display: inline-block;
            background: #fff3e0;
            color: #e65100;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
        }

        .stSelectbox label, .stTextInput label {
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            color: #666 !important;
        }

        div[data-testid="stSelectbox"] > div > div {
            border-radius: 8px;
            font-size: 0.85rem;
        }

        .search-container {
            position: relative;
        }

        .article-image {
            width: 100%;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 0.7rem;
        }

        .article-card.large .article-image {
            height: 180px;
        }

        @media (max-width: 768px) {
            .main-header {
                padding: 1rem;
            }
            .main-header h1 {
                font-size: 1.3rem;
            }
            .header-controls {
                flex-direction: column;
                align-items: stretch;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

import re

CATEGORY_KEYWORDS = {
    "Weather Risk": [
        "drought", "rainfall", "flood", "storm", "frost", "heat wave",
        "heatwave", "temperature", "weather", "precipitation", "climate",
        "el niño", "la niña", "humidity", "hail", "tornado", "hurricane",
        "soil moisture", "frost risk", "heat stress",
    ],
    "Commodities": [
        "commodity", "futures", "wheat", "corn", "soybean", "barley",
        "rice", "sunflower", "sugar", "coffee", "cocoa", "cotton",
        "livestock", "pork", "beef", "poultry", "dairy",
    ],
    "Market Prices": [
        "price", "market price", "cash price", "futures price",
        "trading", "settlement", "bid", "offer", "quote",
        "price forecast", "price outlook", "price rally",
    ],
    "Policy & Trade": [
        "policy", "regulation", "subsidy", "tariff", "trade deal",
        "trade agreement", "WTO", "EU policy", "farm bill",
        "agricultural policy", "government", "legislation",
    ],
    "Export/Import": [
        "export", "import", "shipment", "cargo", "trade balance",
        "customs", "tariff", "sanction", "trade war",
        "trade flow", "export ban", "import duty",
    ],
    "Fertilizer & Inputs": [
        "fertilizer", "fertiliser", "nitrogen", "phosphorus",
        "potash", "urea", "ammonia", "DAP", "MAP", "NPK",
        "input cost", "seed", "pesticide", "herbicide",
    ],
    "Crop Production": [
        "crop", "harvest", "planting", "yield", "production",
        "cultivation", "sowing", "grain", "crop condition",
        "crop progress", "biotech", "GMO", "irrigation",
    ],
    "Food Security": [
        "food security", "hunger", "famine", "malnutrition",
        "food supply", "food crisis", "food price", "staple",
        "food aid", "humanitarian", "food inflation",
    ],
}

COMMODITY_KEYWORDS = {
    "Wheat": ["wheat", "winter wheat", "spring wheat", "durum"],
    "Corn": ["corn", "maize"],
    "Soybeans": ["soybean", "soya", "soy", "soyabean"],
    "Barley": ["barley", "malting barley"],
    "Rice": ["rice", "paddy", "jasmine rice", "basmati"],
    "Sunflower": ["sunflower", "sunflower seed", "sunflower oil"],
    "Sugar": ["sugar", "sugarcane", "sugar beet"],
    "Coffee": ["coffee", "arabica", "robusta"],
    "Cocoa": ["cocoa", "cacao"],
    "Cotton": ["cotton"],
    "Fertilizer": ["fertilizer", "fertiliser", "urea", "nitrogen", "potash", "ammonia"],
}


def classify_article(article: dict) -> str:
    title_summary = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            matches = len(re.findall(rf"\b{re.escape(keyword)}\b", title_summary))
            score += matches
        if score > 0:
            category_scores[category] = score

    if category_scores:
        return max(category_scores, key=category_scores.get)

    return article.get("category", "General Agriculture")


def extract_commodities(article: dict) -> list[str]:
    title_summary = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    detected = []

    for commodity, keywords in COMMODITY_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", title_summary):
                detected.append(commodity)
                break

    return detected


def classify_articles(articles: list[dict]) -> list[dict]:
    for article in articles:
        article["category"] = classify_article(article)
        article["commodities"] = extract_commodities(article)
    return articles

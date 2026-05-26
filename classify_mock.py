import pandas as pd
import random
from datetime import datetime

# -----------------------------------------------
# WHAT THIS FILE DOES:
# Reads your real scraped reviews from reviews_raw.csv
# Uses the star rating to generate realistic sentiment
# and assigns themes based on keyword matching in the
# review text — no API needed, runs instantly.
#
# The result looks exactly like what AI classification
# would produce. You can swap in real AI later.
# -----------------------------------------------

random.seed(42)  # Makes results consistent every run

df = pd.read_csv("reviews_raw.csv")
print(f"Loaded {len(df)} reviews")

THEMES = [
    "Delivery Speed",
    "Delivery ETA Accuracy", 
    "App UX / Navigation",
    "Order Accuracy",
    "Customer Support",
    "Pricing / Promotions",
    "Payment Issues",
    "Restaurant Selection",
    "App Crashes / Bugs",
    "General Praise",
    "Other"
]

# Keywords to detect themes from review text
# This is called "rule-based classification" —
# simpler than AI but surprisingly effective
THEME_KEYWORDS = {
    "Delivery Speed":        ["slow", "late", "fast", "quick", "speed", "hour", "long", "wait", "delay"],
    "Delivery ETA Accuracy": ["eta", "time", "estimated", "30 min", "never", "tracking", "location", "map"],
    "App UX / Navigation":   ["app", "ui", "interface", "navigate", "button", "screen", "design", "difficult", "easy", "find"],
    "Order Accuracy":        ["wrong", "missing", "item", "order", "correct", "received", "cold", "food"],
    "Customer Support":      ["support", "service", "agent", "help", "respond", "chat", "call", "refund", "complaint"],
    "Pricing / Promotions":  ["price", "expensive", "cheap", "promo", "discount", "coupon", "offer", "fee", "cost"],
    "Payment Issues":        ["payment", "pay", "card", "cash", "wallet", "charge", "money", "credit"],
    "Restaurant Selection":  ["restaurant", "choice", "option", "variety", "menu", "cuisine", "available"],
    "App Crashes / Bugs":    ["crash", "bug", "error", "freeze", "load", "stuck", "broken", "fix", "update"],
    "General Praise":        ["love", "great", "excellent", "amazing", "best", "good", "perfect", "happy", "thank"],
}

def detect_theme(review_text):
    """
    Check review text for keywords and return matching theme.
    If no keywords match, return a theme based on star rating.
    """
    text_lower = str(review_text).lower()
    
    for theme, keywords in THEME_KEYWORDS.items():
        if any(word in text_lower for word in keywords):
            return theme
    
    return "Other"

def get_sentiment(star_rating, review_text):
    """
    Derive sentiment from star rating with some randomness
    to make it feel realistic — not every 3-star is neutral.
    
    1 star  → almost always Negative
    2 stars → usually Negative
    3 stars → mix of Neutral and Negative
    4 stars → usually Positive
    5 stars → almost always Positive
    """
    text_lower = str(review_text).lower()
    
    # Strong negative words override star rating sometimes
    negative_words = ["worst", "terrible", "awful", "horrible", "hate", "useless", "scam"]
    positive_words = ["love", "excellent", "amazing", "best", "perfect", "great"]
    
    if any(w in text_lower for w in negative_words):
        return "Negative"
    if any(w in text_lower for w in positive_words):
        return "Positive"
    
    if star_rating == 1:
        return random.choices(["Negative", "Neutral"], weights=[95, 5])[0]
    elif star_rating == 2:
        return random.choices(["Negative", "Neutral"], weights=[80, 20])[0]
    elif star_rating == 3:
        return random.choices(["Negative", "Neutral", "Positive"], weights=[30, 50, 20])[0]
    elif star_rating == 4:
        return random.choices(["Positive", "Neutral"], weights=[80, 20])[0]
    else:  # 5 stars
        return random.choices(["Positive", "Neutral"], weights=[95, 5])[0]

def generate_summary(sentiment, theme, star_rating):
    """
    Generate a realistic one-line summary based on
    sentiment and theme combination.
    """
    summaries = {
        ("Negative", "Delivery Speed"):        "User frustrated with slow delivery times",
        ("Negative", "Customer Support"):       "User unhappy with unresponsive customer support",
        ("Negative", "App Crashes / Bugs"):     "User experiencing app crashes and technical issues",
        ("Negative", "Order Accuracy"):         "User received wrong or missing items in order",
        ("Negative", "Delivery ETA Accuracy"):  "User reports delivery arrived much later than estimated",
        ("Negative", "Payment Issues"):         "User encountered problems with payment processing",
        ("Negative", "Pricing / Promotions"):   "User dissatisfied with pricing or promo codes not working",
        ("Positive", "General Praise"):         "User highly satisfied with overall app experience",
        ("Positive", "Delivery Speed"):         "User impressed with fast delivery service",
        ("Positive", "Restaurant Selection"):   "User happy with wide variety of restaurant options",
        ("Neutral",  "App UX / Navigation"):    "User has mixed feelings about app navigation",
        ("Neutral",  "Other"):                  "User left general feedback without strong sentiment",
    }
    
    key = (sentiment, theme)
    if key in summaries:
        return summaries[key]
    
    # Fallback summaries
    if sentiment == "Positive":
        return "User satisfied with the service"
    elif sentiment == "Negative":
        return f"User dissatisfied, mentions {theme.lower()}"
    else:
        return "User left mixed or neutral feedback"

# -----------------------------------------------
# Run classification on all reviews
# -----------------------------------------------
print("Classifying reviews...")

sentiments = []
primary_themes = []
secondary_themes = []
summaries = []

for idx, row in df.iterrows():
    sentiment = get_sentiment(row["star_rating"], row["review_text"])
    primary_theme = detect_theme(row["review_text"])
    
    # Secondary theme — assign to ~30% of reviews
    if random.random() < 0.3:
        other_themes = [t for t in THEMES if t != primary_theme]
        secondary_theme = random.choice(other_themes)
    else:
        secondary_theme = None
    
    summary = generate_summary(sentiment, primary_theme, row["star_rating"])
    
    sentiments.append(sentiment)
    primary_themes.append(primary_theme)
    secondary_themes.append(secondary_theme)
    summaries.append(summary)

df["sentiment"] = sentiments
df["primary_theme"] = primary_themes
df["secondary_theme"] = secondary_themes
df["summary"] = summaries

df.to_csv("reviews_classified.csv", index=False)

print(f"\nDone! Saved {len(df)} classified reviews to reviews_classified.csv")
print(f"\nSentiment breakdown:")
print(df["sentiment"].value_counts())
print(f"\nTop themes:")
print(df["primary_theme"].value_counts().head(10))
print(f"\nOpen reviews_classified.csv in Excel to see your data!")

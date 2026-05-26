from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime

# -----------------------------------------------
# WHAT THIS FILE DOES:
# Connects to Google Play Store and downloads
# real user reviews for Talabat's app.
# Saves them to a CSV file you can open in Excel.
# -----------------------------------------------

# Talabat's app ID on Google Play Store
# (you can find this in any Play Store URL: ?id=XXXX)
APP_ID = "com.talabat"

print("Scraping Talabat reviews from Play Store...")
print("This will take about 1-2 minutes...")

# Download reviews — we ask for 2000, may get slightly less
result, _ = reviews(
    APP_ID,
    lang="en",           # English reviews only
    country="ae",        # UAE store
    sort=Sort.NEWEST,    # Most recent first
    count=2000,
)

# Convert to a pandas DataFrame (think: a table in Python)
df = pd.DataFrame(result)

# Keep only the columns we care about
df = df[["content", "score", "at", "appVersion"]]

# Rename columns to be more readable
df.columns = ["review_text", "star_rating", "date", "app_version"]

# Remove any rows where the review text is empty
df = df.dropna(subset=["review_text"])

# Remove reviews that are just 1-2 words (not useful)
df = df[df["review_text"].str.split().str.len() >= 3]

# Convert date to a clean format (YYYY-MM-DD)
df["date"] = pd.to_datetime(df["date"]).dt.date

# Save to CSV
df.to_csv("reviews_raw.csv", index=False)

print(f"\nDone! Saved {len(df)} reviews to reviews_raw.csv")
print(f"\nFirst 5 reviews:")
print(df.head())
print(f"\nStar rating breakdown:")
print(df["star_rating"].value_counts().sort_index())

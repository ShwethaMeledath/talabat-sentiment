import anthropic
import pandas as pd
import json
import time
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv()

# -----------------------------------------------
# WHAT THIS FILE DOES:
# Reads every review from reviews_raw.csv,
# sends each one to Claude, and asks it to return:
#   - Sentiment (Positive / Negative / Neutral)
#   - Primary theme (what is the review about?)
#   - Secondary theme (optional second topic)
#   - A one-line summary
# Saves enriched data to reviews_classified.csv
# -----------------------------------------------

# Connect to Anthropic API
client = anthropic.Anthropic()

# Load our scraped reviews
df = pd.read_csv("reviews_raw.csv")
print(f"Loaded {len(df)} reviews to classify")

# -----------------------------------------------
# THEME TAXONOMY — you designed this as a PM
# These are the categories that matter for a
# food delivery app. Change these for other apps.
# -----------------------------------------------
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

def classify_review(review_text, star_rating):
    """
    Send one review to Claude and get back structured JSON.
    
    'Structured JSON' means we tell Claude exactly what format
    to respond in, so our code can reliably read the answer.
    """
    
    prompt = f"""You are a product analyst for a food delivery app.

Analyze this user review and return ONLY a JSON object with no other text.

Review: "{review_text}"
Star Rating: {star_rating}/5

Return this exact JSON structure:
{{
  "sentiment": "Positive" | "Negative" | "Neutral",
  "primary_theme": one of {THEMES},
  "secondary_theme": one of {THEMES} or null if only one theme,
  "summary": "one sentence max summarizing the core feedback"
}}

Rules:
- sentiment must be exactly "Positive", "Negative", or "Neutral"
- primary_theme must be exactly one value from the list provided
- Do not add any explanation, only return the JSON object"""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Haiku = fast + cheap, perfect for bulk classification
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the JSON response
        response_text = message.content[0].text.strip()
        result = json.loads(response_text)
        return result
        
    except json.JSONDecodeError:
        # If Claude didn't return valid JSON, return a fallback
        print(f"  Warning: Could not parse JSON for review: {review_text[:50]}...")
        return {
            "sentiment": "Neutral",
            "primary_theme": "Other",
            "secondary_theme": None,
            "summary": "Could not classify"
        }
    except Exception as e:
        print(f"  API Error: {e}")
        # Wait a moment and return fallback (handles rate limiting)
        time.sleep(5)
        return {
            "sentiment": "Neutral",
            "primary_theme": "Other",
            "secondary_theme": None,
            "summary": "Error during classification"
        }

# -----------------------------------------------
# Run classification on all reviews
# We process in batches and save progress every 100
# so if it crashes partway, you don't lose work
# -----------------------------------------------

# Add new columns to our dataframe
df["sentiment"] = None
df["primary_theme"] = None
df["secondary_theme"] = None
df["summary"] = None

# Check if we already have partial results (resume from where we left off)
try:
    existing = pd.read_csv("reviews_classified.csv")
    classified_count = existing["sentiment"].notna().sum()
    df.update(existing)
    print(f"Resuming from {classified_count} already classified reviews")
except FileNotFoundError:
    print("Starting fresh classification...")

total = len(df)
for i, (idx, row) in enumerate(df.iterrows()):
    
    # Skip if already classified
    if pd.notna(row["sentiment"]):
        continue
    
    # Show progress
    if i % 10 == 0:
        print(f"Progress: {i}/{total} reviews ({round(i/total*100)}%)")
    
    # Classify this review
    result = classify_review(row["review_text"], row["star_rating"])
    
    # Store results
    df.at[idx, "sentiment"] = result.get("sentiment", "Neutral")
    df.at[idx, "primary_theme"] = result.get("primary_theme", "Other")
    df.at[idx, "secondary_theme"] = result.get("secondary_theme")
    df.at[idx, "summary"] = result.get("summary", "")
    
    # Save progress every 100 reviews
    if i % 100 == 0:
        df.to_csv("reviews_classified.csv", index=False)
    
    # Small delay to avoid hitting API rate limits
    # Rate limit = how many requests per minute the API allows
    time.sleep(0.3)

# Final save
df.to_csv("reviews_classified.csv", index=False)

print(f"\n✓ Done! Saved to reviews_classified.csv")
print(f"\nSentiment breakdown:")
print(df["sentiment"].value_counts())
print(f"\nTop themes:")
print(df["primary_theme"].value_counts().head(10))

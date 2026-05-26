# Talabat Sentiment Analysis Dashboard

An interactive sentiment analysis dashboard built using Python and Streamlit to analyze Talabat app reviews from the Google Play Store.

The project was designed to support AI-powered review classification using the Anthropic Claude API. However, due to billing/payment limitations during development, the current implementation uses pre-classified mock sentiment data to simulate the production workflow.

This allows the dashboard to run fully without requiring paid API access while still demonstrating the analytics and visualization pipeline.

---

# Features

- Google Play Store review scraping
- Sentiment analysis dashboard
- Interactive visualizations using Plotly
- Streamlit-based UI
- Mock AI-classified dataset support
- Optional Anthropic Claude API integration

---

# Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Google Play Scraper
- Anthropic Claude API (optional)
- dotenv

---

# Installation

## Clone Repository

```bash
git clone https://github.com/ShwethaMeledath/talabat-sentiment.git
cd talabat-sentiment
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Mock Mode (Recommended)

Runs using pre-classified sentiment data.

```bash
streamlit run app.py
```

No API key required.

---

## Real AI Mode (Optional)

### Create `.env`

```env
ANTHROPIC_API_KEY=your_api_key_here
```

### Run AI Classification

```bash
python services/classify_reviews.py
```

### Launch Dashboard

```bash
streamlit run app.py
```

---

# Environment Variables

Create a `.env` file locally:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

The `.env` file is ignored using `.gitignore` for security.

---

# Screenshots

Add dashboard screenshots inside the `screenshots/` folder.

Example:

```md
![Dashboard](screenshots/dashboard.png)
```

---

# Future Improvements

- Real-time AI classification
- Multi-language review analysis
- Trend forecasting
- Cloud deployment
- Exportable reports

---

# Author

Shwetha AM

GitHub:
https://github.com/ShwethaMeledath
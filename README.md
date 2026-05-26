# AI-Powered Talabat Sentiment Analysis Dashboard

An interactive sentiment analysis dashboard built using Python and Streamlit to analyze Talabat app reviews from the Google Play Store.

The project was designed to support AI-powered review classification using the Anthropic Claude API. However, due to billing/payment limitations during development, the current implementation uses pre-classified mock sentiment data to simulate the production workflow.

This allows the dashboard to run fully without requiring paid API access while still demonstrating the analytics and visualization pipeline.

---

# Dashboard Preview

## Main Dashboard

![Dashboard Preview](screenshots/dashboard.png)

## Sentiment Analytics

![Analytics](screenshots/charts.png)

---

# Features

- Automated Google Play Store review scraping
- AI-ready sentiment analysis pipeline
- Interactive Streamlit dashboard
- Sentiment distribution visualizations
- Review trend analytics
- Mock-data fallback architecture
- Secure environment-variable configuration
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

# Workflow

1. Scrape Talabat reviews from Google Play Store
2. Process and clean review data
3. Classify sentiment using:
   - Mock classified dataset (default)
   - OR Anthropic Claude API (optional)
4. Visualize insights in Streamlit dashboard
5. Analyze sentiment trends and distributions

---

# Installation

## Clone Repository

```bash
git clone https://github.com/ShwethaMeledath/talabat-sentiment.git
cd talabat-sentiment
```

---

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

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Mock Mode (Recommended)

Runs using pre-classified sentiment data.

```bash
python -m streamlit run app.py
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
python -m streamlit run app.py
```

---

# Environment Variables

Create a `.env` file locally:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

The `.env` file is ignored using `.gitignore` for security.

---

# .env.example

Create a `.env.example` file containing:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

---

# Project Structure

talabat-sentiment/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
├── services/
├── screenshots/

---

# Key Learnings

Through this project, I explored:
- AI workflow integration
- Streamlit dashboard development
- Data visualization using Plotly
- Secure API key management
- Mock-driven development approaches
- Structuring reproducible analytics pipelines

---

# Resume Highlights

- Built a Python-based sentiment analytics dashboard using Streamlit and Plotly
- Designed a sentiment-classification workflow with optional Anthropic Claude API integration
- Implemented mock-data fallback architecture to enable reproducible local execution without external API dependency
- Applied secure `.env`-based configuration management and GitHub secret-safe workflows

---

# Future Improvements

- Real-time AI classification
- Multi-language review analysis
- Trend forecasting
- Cloud deployment
- Exportable reports

---

Note:
Ensure sufficient disk space is available before installing dependencies and creating the virtual environment.

# Author

Shwetha AM

GitHub:
https://github.com/ShwethaMeledath
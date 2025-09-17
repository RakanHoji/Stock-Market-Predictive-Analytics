## Code by @RakanHoji - find me on LinkedIn: https://www.linkedin.com/in/rakan-hoji/
# Stock-Market-Predictive-Analytics
An end-to-end data engineering and data science project that ingests stock market data and financial news, processes it into a structured PostgreSQL database, runs sentiment analysis + forecasting models, and serves interactive insights through a Streamlit dashboard.

This project demonstrates skills across ETL pipelines, SQL, ML modeling, and MLOps — built entirely with free/open-source tools.

Tools & Tech Stack

Orchestration: Apache Airflow

Database: PostgreSQL

Ingestion: yFinance API, BeautifulSoup (web scraping)

ETL/ELT: SQLAlchemy, Pandas

Machine Learning: Prophet (forecasting), VADER Sentiment (NLP)

Visualization: Streamlit, Plotly

Deployment: Docker (optional)

            ┌────────────────┐
            │  APIs / Scrape │
            │ (yfinance/news)│
            └───────┬────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   Airflow Scheduler   │
        │   (Daily DAG Runs)    │
        └─────────┬─────────────┘
                  │
        ┌─────────▼───────────┐
        │   PostgreSQL DB     │
        │ Raw + Clean Schemas │
        └─────────┬───────────┘
                  │
      ┌───────────▼───────────┐
      │  Processing & ML      │
      │ (Sentiment + Prophet) │
      └───────────┬───────────┘
                  │
        ┌─────────▼────────────┐
        │   Streamlit App      │
        │   (Dashboard UI)     │
        └──────────────────────┘

stock-pipeline-project/
├── airflow/              # DAGs & Airflow configs
├── db/                   # Database schema & SQL transformations
├── ingestion/            # Data ingestion scripts
├── processing/           # Data cleaning & ML (forecasting, NLP)
├── dashboard/            # Streamlit dashboard
├── docker/               # Docker configs
├── tests/                # Unit tests
├── requirements.txt      # Dependencies
└── README.md             # Project docs



## Workflow

Ingestion:

Stock price data pulled from Yahoo Finance (yfinance)
Financial headlines scraped from Yahoo Finance News

Storage:

Data saved into PostgreSQL
Raw schema → Clean schema → Enriched tables

Processing:

Clean and join stock + sentiment data
Run VADER sentiment analysis on headlines
Forecast stock price using Prophet

Visualization:

Interactive Streamlit dashboard
Forecast charts + sentiment trends

**Scan for Bugs:**
Use **SonarQube** to scan bugs and any security risks
Use **HashiCorp** for securing API keys and passwords



#### Extensions (For Future Work)

Add real-time ingestion with Kafka + Spark Streaming.

Deploy on GCP using Terraform.

Implement CI/CD retraining pipeline with GitHub Actions.

Build Buy/Sell signal recommender.



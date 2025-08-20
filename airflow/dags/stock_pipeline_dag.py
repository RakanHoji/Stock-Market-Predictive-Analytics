from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from ingestion.fetch_stocks import fetch_stock_data
from ingestion.fetch_news import fetch_news
from processing.sentiment_analysis import analyze_sentiment

default_args = {"owner": "airflow", "start_date": datetime(2024, 1, 1)}

with DAG("stock_pipeline",
         default_args=default_args,
         schedule_interval="@daily",
         catchup=False) as dag:

    task_fetch_stocks = PythonOperator(
        task_id="fetch_stocks",
        python_callable=fetch_stock_data,
        op_args=["AAPL"]
    )

    task_fetch_news = PythonOperator(
        task_id="fetch_news",
        python_callable=fetch_news,
        op_args=["AAPL"]
    )

    task_sentiment = PythonOperator(
        task_id="sentiment_analysis",
        python_callable=analyze_sentiment
    )

    task_fetch_stocks >> task_fetch_news >> task_sentiment


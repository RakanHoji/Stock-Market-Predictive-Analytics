from __future__ import annotations

from datetime import timedelta

import pendulum

# Airflow 3.x import paths: DAG authoring lives in the Task SDK; core operators
# moved to the `apache-airflow-providers-standard` package. (If your 3.x minor
# predates the SDK split, `from airflow import DAG` still works as a fallback.)
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator

# Shared DB layer — sits next to this file in airflow/dags/.
import dag_db

# Project modules — entrypoints assumed (see module-interface note above).
from ingestion import fetch_stocks, fetch_news
from processing import clean_data, sentiment_analysis, forecasting

# Hardcoded for clarity. For anything dynamic, promote to an Airflow Variable:
# TICKERS = Variable.get("tickers", deserialize_json=True).
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]

default_args = {
    "owner": "rakan",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
}


# --- Thin task wrappers ----------------------------------------------------
# Each wrapper pulls the logical run date (`ds`, YYYY-MM-DD) from the task
# context and forwards it to the module entrypoint. Context is auto-injected
# into PythonOperator callables in Airflow 2.0+, so no `provide_context` flag.

def _check_db(**_context) -> None:
    dag_db.test_connection()


def _fetch_stocks(**context) -> None:
    fetch_stocks.run(run_date=context["ds"], tickers=TICKERS)


def _fetch_news(**context) -> None:
    fetch_news.run(run_date=context["ds"], tickers=TICKERS)


def _clean_data(**context) -> None:
    clean_data.run(run_date=context["ds"])


def _run_sentiment(**context) -> None:
    sentiment_analysis.run(run_date=context["ds"])


def _run_forecast(**context) -> None:
    forecasting.run(run_date=context["ds"])


with DAG(
    dag_id="stock_pipeline",
    description="Daily check -> ingest -> clean -> sentiment + forecast pipeline.",
    default_args=default_args,
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    # Weekdays at 23:00 UTC — after the US market close (16:00 ET), skipping
    # weekends. Note: cron does NOT skip market holidays; gate ingestion behind
    # a short-circuit task (e.g. pandas_market_calendars) if that matters.
    schedule="0 23 * * 1-5",
    catchup=False,
    max_active_runs=1,  # runs share DB tables; serialize them.
    tags=["stocks", "etl", "ml", "prophet", "vader"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    check_db = PythonOperator(
        task_id="check_db",
        python_callable=_check_db,
        retries=3,                          # DB may still be coming up
        retry_delay=timedelta(seconds=20),
    )

    fetch_stocks_task = PythonOperator(
        task_id="fetch_stocks",
        python_callable=_fetch_stocks,
    )

    fetch_news_task = PythonOperator(
        task_id="fetch_news",
        python_callable=_fetch_news,
    )

    clean_data_task = PythonOperator(
        task_id="clean_data",
        python_callable=_clean_data,
    )

    run_sentiment_task = PythonOperator(
        task_id="run_sentiment",
        python_callable=_run_sentiment,
    )

    run_forecast_task = PythonOperator(
        task_id="run_forecast",
        python_callable=_run_forecast,
    )

    # check DB first, ingest in parallel, clean, then fan out the two ML tasks.
    start >> check_db >> [fetch_stocks_task, fetch_news_task] >> clean_data_task
    clean_data_task >> [run_sentiment_task, run_forecast_task] >> end

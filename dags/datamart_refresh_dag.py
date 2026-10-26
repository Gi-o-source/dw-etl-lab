from datetime import datetime, timedelta
from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    "owner": "data_engineers",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

@dag(
    dag_id="datamart_refresh_dag",
    default_args=default_args,
    schedule="@hourly",
    start_date=datetime(2026, 10, 1),
    catchup=False,
    tags=["datamart", "reporting"],
)
def datamart_refresh():

    @task
    def refresh_daily_category_sales():
        hook = PostgresHook(postgres_conn_id="dwh_postgres")
        hook.run("REFRESH MATERIALIZED VIEW dw.v_daily_category_sales;")

    refresh_daily_category_sales()

datamart_refresh()

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
import os

# ==============================
# Config
# ==============================
DATA_DIR = "/opt/airflow/data"
DBT_PROJECT_DIR = "/opt/airflow/dbt"
ALERTS_OUTPUT = "/opt/airflow/data/fraud_alerts.csv"

default_args = {
    'owner': 'Adebimpe',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ==============================
# DAG Definition
# ==============================
with DAG(
    'fraud_transactions_pipeline',
    default_args=default_args,
    description='ETL and alert pipeline for financial fraud detection',
    schedule_interval='@daily',
    start_date=datetime(2026, 3, 13),
    catchup=False,
) as dag:

    # ------------------------------
    # 1. Load CSV -> staging (simulated)
    # ------------------------------
    def load_transactions():
        # For demo, we just read CSV
        file_path = os.path.join(DATA_DIR, "sample_data.csv")
        df = pd.read_csv(file_path)
        # Optional: Save to staging CSV or database
        staging_path = os.path.join(DATA_DIR, "stg_transactions.csv")
        df.to_csv(staging_path, index=False)
        print(f"Loaded {len(df)} transactions to staging.")

    load_staging = PythonOperator(
        task_id='load_transactions_to_staging',
        python_callable=load_transactions
    )

    # ------------------------------
    # 2. Run dbt models
    # ------------------------------
    dbt_run = BashOperator(
        task_id='run_dbt_models',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt deps && dbt run'
    )

    # ------------------------------
    # 3. Generate fraud alerts
    # ------------------------------
    def generate_alerts():
        fct_path = os.path.join(DATA_DIR, "fct_fraud_summary.csv")
        if not os.path.exists(fct_path):
            print("Fact summary not found, skipping alerts.")
            return
        df = pd.read_csv(fct_path)

        # Example alert: CASH_OUT > 200k or high fraud count
        alerts = df[(df['total_amount'] > 200000) | (df['fraud_count'] > 0)]
        alerts.to_csv(ALERTS_OUTPUT, index=False)
        print(f"{len(alerts)} alerts generated and saved to {ALERTS_OUTPUT}")

    alert_task = PythonOperator(
        task_id='generate_fraud_alerts',
        python_callable=generate_alerts
    )

    # ------------------------------
    # DAG dependencies
    # ------------------------------
    load_staging >> dbt_run >> alert_task

"""
DAG do Apache Airflow para Orquestração do Pipeline Olist E-Commerce.
Fluxo: Checagem de Arquivos -> Ingestão Híbrida (PostgreSQL + GCP BigQuery Sandbox) -> dbt Run -> dbt Test.
"""

import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "engenharia_dados",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def checar_arquivos_raw():
    """
    Verifica se a pasta data/raw existe e se há arquivos CSV brutos para ingestão.
    """
    raw_path = os.path.join(os.getcwd(), "data", "raw")
    if not os.path.exists(raw_path):
        os.makedirs(raw_path, exist_ok=True)
        print(f"Diretório {raw_path} criado.")

    files = [f for f in os.listdir(raw_path) if f.endswith(".csv")]
    print(f"Arquivos CSV encontrados em {raw_path}: {len(files)} arquivos.")
    return True


with DAG(
    "pipeline_olist_ecommerce",
    default_args=default_args,
    description="Pipeline Completo ELT: Carga Raw + GCP BigQuery Sandbox + dbt Transform + dbt Test",
    schedule_interval="@daily",
    catchup=False,
    tags=["olist", "elt", "dbt", "postgres", "bigquery", "gcp"],
) as dag:

    # 1. Checagem dos arquivos de entrada
    task_checar_arquivos = PythonOperator(
        task_id="task_checar_arquivos",
        python_callable=checar_arquivos_raw,
    )

    # 2a. Ingestão dos dados brutos no PostgreSQL (Camada Bronze / Raw Local)
    task_ingestao_postgres = BashOperator(
        task_id="task_ingestao_postgres",
        bash_command="python /app/scripts/carregar_rapido.py || python scripts/carregar_rapido.py",
    )

    # 2b. Ingestão e sincronização para o Cloud Data Warehouse (Google BigQuery Sandbox)
    task_ingestao_bigquery = BashOperator(
        task_id="task_ingestao_bigquery",
        bash_command="python /app/scripts/carregar_bigquery.py || python scripts/carregar_bigquery.py",
    )

    # 3. Execução das transformações dbt (Camada Prata e Ouro)
    task_dbt_run = BashOperator(
        task_id="task_dbt_run",
        bash_command="cd /app/dbt_olist && dbt run --profiles-dir . || cd dbt_olist && dbt run --profiles-dir .",
    )

    # 4. Execução dos testes de qualidade de dados dbt
    task_dbt_test = BashOperator(
        task_id="task_dbt_test",
        bash_command="cd /app/dbt_olist && dbt test --profiles-dir . || cd dbt_olist && dbt test --profiles-dir .",
    )

    # Ordem de execução do pipeline (Cargas para Postgres e BigQuery rodam em paralelo)
    task_checar_arquivos >> [task_ingestao_postgres, task_ingestao_bigquery] >> task_dbt_run >> task_dbt_test

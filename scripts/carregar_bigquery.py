"""
Script para carga dos dados do Olist no Google BigQuery Sandbox.
Lê os arquivos CSV da pasta data/raw e realiza a carga em lote (batch) 
para o dataset 'olist_raw' no BigQuery.
"""

import os
import sys
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Fix para encoding em consoles Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract_olist import extract_olist_csvs


def get_bigquery_client():
    """Inicializa e retorna o cliente do BigQuery utilizando as credenciais salvas."""
    project_id = os.getenv("GCP_PROJECT_ID", "bidataanalytics-505811")
    key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "secrets/gcp-key.json")

    # Caso o caminho seja relativo à raiz
    if not os.path.isabs(key_path):
        key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), key_path)

    if not os.path.exists(key_path):
        raise FileNotFoundError(
            f"[ERRO] Arquivo de credenciais nao encontrado em: {key_path}\n"
            "Certifique-se de salvar a chave JSON em secrets/gcp-key.json"
        )

    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=project_id)
    print(f"[OK] Autenticado no BigQuery GCP (Projeto: {project_id})")
    return client, project_id


def carregar_para_bigquery():
    """Carrega os dataframes brutos da Olist para o BigQuery Sandbox."""
    client, project_id = get_bigquery_client()
    dataset_id = f"{project_id}.olist_raw"

    # 1. Criar o Dataset se não existir (Localização US para a cota gratuita do Sandbox)
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset.description = "Dataset contendo os dados brutos da Olist para E-commerce Analytics"
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f"[DATASET] Dataset 'olist_raw' garantido em: {dataset_id}")

    # 2. Extrair dados brutos da pasta data/raw
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
    print(f"[READ] Lendo CSVs da pasta: {data_dir}")
    raw_dfs = extract_olist_csvs(data_dir)

    if not raw_dfs:
        print("[AVISO] Nenhum arquivo CSV encontrado para carregar.")
        return

    # 3. Mapeamento de tabelas
    table_configs = {
        "customers": {"df_key": "customers", "table_name": "raw_customers"},
        "products": {"df_key": "products", "table_name": "raw_products"},
        "orders": {"df_key": "orders", "table_name": "raw_orders"},
        "order_items": {"df_key": "order_items", "table_name": "raw_order_items"},
        "order_payments": {"df_key": "order_payments", "table_name": "raw_order_payments"},
    }

    print("\n[START] Iniciando carga em lote para o BigQuery Sandbox...")

    for key, config in table_configs.items():
        if key not in raw_dfs or raw_dfs[key] is None or raw_dfs[key].empty:
            print(f"[SKIP] Ignorando tabela {key}: Dados nao encontrados.")
            continue

        df = raw_dfs[key].copy()
        table_name = config["table_name"]
        table_ref = f"{dataset_id}.{table_name}"

        # Deletar tabela anterior para recriar com autodetect limpo
        client.delete_table(table_ref, not_found_ok=True)

        # Configurar job de carga do BigQuery
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            autodetect=True
        )

        print(f"[LOAD] Carregando {len(df):,} linhas na tabela BigQuery '{table_ref}'...")
        
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Aguarda a conclusão do job de carga

        table = client.get_table(table_ref)
        print(f"[SUCCESS] Tabela '{table_name}' criada com sucesso! Total no BigQuery: {table.num_rows:,} linhas ({table.num_bytes / (1024*1024):.2f} MB)")

    print("\n[FINISH] Todas as tabelas foram carregadas com sucesso no BigQuery Sandbox!")


if __name__ == "__main__":
    carregar_para_bigquery()

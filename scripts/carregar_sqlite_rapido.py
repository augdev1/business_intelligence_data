"""
Script de carga ultra rápida para SQLite usando pandas to_sql.
"""

import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "olist.db")
if os.path.exists(db_file):
    try:
        os.remove(db_file)
        print(f"  {db_file} antigo removido com sucesso.")
    except Exception as e:
        print(f"Erro ao remover {db_file}: {e}")

from database.connection import engine, init_db
from etl.extract_olist import extract_olist_csvs
from etl.transform_olist import transform_all


def main():
    print("Inicializando banco de dados...")
    init_db()

    print("Extraindo CSVs do Olist...")
    dfs = extract_olist_csvs("data/raw")

    print("Transformando dados...")
    transformed = transform_all(dfs)

    tables = ["customers", "products", "orders", "order_items", "order_payments"]

    total = 0
    with engine.begin() as conn:
        for name in tables:
            if name not in transformed:
                print(f"  {name}: não encontrado, pulando")
                continue
            df, _errs, _warns = transformed[name]

            df.to_sql(name, con=conn, if_exists="append", index=False)
            n = len(df)
            total += n
            print(f"  {name}: {n} inseridos")

    print(f"\nCarga ultra rápida concluída: {total} registros totais inseridos.")


if __name__ == "__main__":
    main()

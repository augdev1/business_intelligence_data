"""
Script de carga rápida do dataset Olist usando bulk inserts com ON CONFLICT DO NOTHING.
Muito mais rápido que carregar_olist.py (sem queries individuais de deduplicação).
"""
import sys
import os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.dialects.postgresql import insert
from database.connection import engine, init_db
from etl.extract_olist import extract_olist_csvs
from etl.transform_olist import transform_all

from backend.models.customer import Customer
from backend.models.product import Product
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.order_payment import OrderPayment


def nat_to_none(df: pd.DataFrame) -> list[dict]:
    """Convert DataFrame to list of dicts replacing NaT/NaN with None."""
    records = df.to_dict("records")
    for row in records:
        for k, v in row.items():
            if isinstance(v, float) and np.isnan(v):
                row[k] = None
            elif pd.isnull(v) if not isinstance(v, (list, dict)) else False:
                row[k] = None
    return records


def bulk_upsert(model, records: list[dict], chunk: int = 5000) -> int:
    """Insert records in chunks using ON CONFLICT DO NOTHING. Returns count inserted."""
    if not records:
        return 0
    inserted = 0
    with engine.begin() as conn:
        for i in range(0, len(records), chunk):
            batch = records[i : i + chunk]
            stmt = insert(model).values(batch).on_conflict_do_nothing()
            result = conn.execute(stmt)
            inserted += result.rowcount
    return inserted


def main():
    print("Inicializando banco de dados...")
    init_db()

    print("Extraindo CSVs do Olist...")
    dfs = extract_olist_csvs("data/raw")

    print("Transformando dados...")
    transformed = transform_all(dfs)

    tables = [
        ("customers",     Customer,     "customer_id"),
        ("products",      Product,      "product_id"),
        ("orders",        Order,        "order_id"),
        ("order_items",   OrderItem,    None),
        ("order_payments",OrderPayment, None),
    ]

    total = 0
    for name, model, _ in tables:
        if name not in transformed:
            print(f"  {name}: não encontrado, pulando")
            continue
        df, _errs, _warns = transformed[name]
        records = nat_to_none(df)
        n = bulk_upsert(model, records)
        total += n
        print(f"  {name}: {n} inseridos de {len(records)} registros")

    print(f"\nCarga concluída: {total} registros totais inseridos.")


if __name__ == "__main__":
    main()

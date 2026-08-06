"""
Script de geração e persistência de embeddings de produtos usando pgvector no PostgreSQL.
"""

import os
import logging
from typing import List
from sqlalchemy.orm import Session
from database.connection import engine, SessionLocal, init_db
from backend.models.product import Product
from backend.models.product_embedding import ProductEmbedding
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_embedding(text_str: str) -> List[float]:
    """
    Gera embedding de 1536 dimensões usando OpenAIEmbeddings se disponível,
    ou fallback determinístico base de teste caso não haja API key.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from langchain_openai import OpenAIEmbeddings

            embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
            return embeddings.embed_query(text_str)
        except Exception as e:
            logger.warning(f"Erro ao usar OpenAIEmbeddings: {e}. Usando fallback.")

    # Fallback vetorial determinístico para ambientes sem API key (1536 dimensões)
    import hashlib

    hash_object = hashlib.sha256(text_str.encode("utf-8"))
    seed = int(hash_object.hexdigest(), 16) % (2**32)
    import numpy as np

    np.random.seed(seed)
    vector = np.random.normal(0, 1, 1536)
    norm = np.linalg.norm(vector)
    return (vector / norm).tolist()


def init_pgvector_extension():
    """Garante que a extensão vector esteja criada no banco PostgreSQL."""
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        logger.info("Extensão pgvector verificada/habilitada no banco de dados.")
    except Exception as e:
        logger.warning(f"Não foi possível habilitar a extensão pgvector automaticamente: {e}")


def run_embedding_pipeline(batch_size: int = 500):
    """
    Carrega os produtos cadastrados na tabela `products`, constrói a representação textual
    e salva na tabela `product_embeddings`.
    """
    init_db()
    init_pgvector_extension()

    db: Session = SessionLocal()
    try:
        products = db.query(Product).all()
        logger.info(f"Processando embeddings para {len(products)} produtos...")

        count = 0
        for i in range(0, len(products), batch_size):
            batch = products[i : i + batch_size]
            for p in batch:
                cat = p.product_category_name or "geral"
                text_repr = f"Produto ID: {p.product_id}. Categoria: {cat}. Peso: {p.product_weight_g or 0}g."

                vector_data = generate_embedding(text_repr)

                # Upsert / Merge do embedding
                existing = db.query(ProductEmbedding).filter_by(product_id=p.product_id).first()
                if existing:
                    existing.category_name = cat
                    existing.text_content = text_repr
                    existing.embedding = vector_data
                else:
                    emb_obj = ProductEmbedding(
                        product_id=p.product_id,
                        category_name=cat,
                        text_content=text_repr,
                        embedding=vector_data,
                    )
                    db.add(emb_obj)
                count += 1

            db.commit()
            logger.info(f"Progresso de embeddings: {count}/{len(products)} concluídos.")

        logger.info(
            f"Pipeline de embeddings concluído com sucesso. {count} registros inseridos/atualizados."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Erro no pipeline de embeddings: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_embedding_pipeline()

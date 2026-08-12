"""
Script de geração e persistência de embeddings de avaliações de clientes (reviews) usando pgvector / JSON no PostgreSQL.
"""

import os
import logging
import pandas as pd
from typing import List
from sqlalchemy.orm import Session
from database.connection import engine, SessionLocal, init_db
from backend.models.review_embedding import ReviewEmbedding
from ai.embed_products import generate_embedding, init_pgvector_extension

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_review_embedding_pipeline(
    csv_path: str = "data/raw/olist_order_reviews_dataset.csv",
    batch_size: int = 200,
    max_reviews: int = 5000,
):
    """
    Carrega o dataset de avaliações do Olist, filtra avaliações com comentários significativos,
    gera embeddings de 1536 dimensões e salva na tabela `review_embeddings`.

    Args:
        csv_path: Caminho para o CSV de reviews
        batch_size: Tamanho do lote para commit no banco
        max_reviews: Limite máximo de avaliações para processar (para otimização de tempo/API)
    """
    init_db()
    init_pgvector_extension()

    if not os.path.exists(csv_path):
        logger.error(f"Arquivo CSV não encontrado em: {csv_path}")
        return

    logger.info(f"Carregando dataset de reviews de {csv_path}...")
    df = pd.read_csv(csv_path)

    # Filtrar apenas avaliações que contêm comentário em texto
    df_with_comments = df[df["review_comment_message"].notna() & (df["review_comment_message"].str.strip() != "")].copy()
    
    total_found = len(df_with_comments)
    logger.info(f"Total de reviews com comentário em texto: {total_found}")

    if total_found == 0:
        logger.warning("Nenhum comentário de texto encontrado para gerar embeddings.")
        return

    # Limitar aos primeiros max_reviews para balancear riqueza de dados e tempo de execução
    if max_reviews and max_reviews < total_found:
        df_with_comments = df_with_comments.head(max_reviews)

    logger.info(f"Processando embeddings para {len(df_with_comments)} avaliações...")

    db: Session = SessionLocal()
    try:
        count = 0
        records = df_with_comments.to_dict(orient="records")

        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            for row in batch:
                review_id = str(row.get("review_id", ""))
                order_id = str(row.get("order_id", ""))
                score = int(row.get("review_score", 0)) if pd.notna(row.get("review_score")) else 0
                title = str(row.get("review_comment_title", "")) if pd.notna(row.get("review_comment_title")) else ""
                comment = str(row.get("review_comment_message", "")).strip()

                if not review_id or not comment:
                    continue

                text_repr = f"Nota: {score}/5. Título: {title}. Comentário: {comment}"
                vector_data = generate_embedding(text_repr)

                # Upsert / Merge do embedding de review
                existing = db.query(ReviewEmbedding).filter_by(review_id=review_id).first()
                if existing:
                    existing.order_id = order_id
                    existing.score = score
                    existing.comment_text = comment
                    existing.text_content = text_repr
                    existing.embedding = vector_data
                else:
                    emb_obj = ReviewEmbedding(
                        review_id=review_id,
                        order_id=order_id,
                        score=score,
                        comment_text=comment,
                        text_content=text_repr,
                        embedding=vector_data,
                    )
                    db.add(emb_obj)
                count += 1

            db.commit()
            logger.info(f"Progresso de embeddings de reviews: {count}/{len(records)} concluídos.")

        logger.info(f"Pipeline de embeddings de reviews concluído com sucesso! Total: {count} processados.")
    except Exception as e:
        db.rollback()
        logger.error(f"Erro no pipeline de embeddings de reviews: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_review_embedding_pipeline()

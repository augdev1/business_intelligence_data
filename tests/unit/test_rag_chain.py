"""
Testes unitários para os componentes e pipelines do RAG.
"""

import pytest
from backend.models.review_embedding import ReviewEmbedding
from ai.sql_chain import SQLChain


def test_review_embedding_model_instantiation():
    """Testa a instanciação do modelo ReviewEmbedding."""
    review_emb = ReviewEmbedding(
        review_id="rev_123",
        order_id="ord_456",
        score=5,
        category_name="beleza_saude",
        comment_text="Excelente produto!",
        text_content="Nota: 5/5. Comentário: Excelente produto!",
    )

    assert review_emb.review_id == "rev_123"
    assert review_emb.order_id == "ord_456"
    assert review_emb.score == 5
    assert review_emb.comment_text == "Excelente produto!"
    assert "ReviewEmbedding" in repr(review_emb)


def test_sql_chain_initialization():
    """Testa se o SQLChain lida adequadamente com o provider de IA ou exceção de chave."""
    try:
        chain = SQLChain(ai_provider="groq")
        assert chain.ai_provider == "groq"
    except ValueError as e:
        assert "GROQ_API_KEY" in str(e)

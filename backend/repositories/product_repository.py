"""
Repository para operações com products.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.product import Product
from backend.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository para operações específicas de products.
    """
    
    def __init__(self, db: Session):
        super().__init__(Product, db)
    
    def get_by_category(self, category: str) -> List[Product]:
        """
        Busca produtos por categoria.
        
        Args:
            category: Nome da categoria
            
        Returns:
            Lista de produtos da categoria
        """
        return self.db.query(Product).filter(Product.product_category_name == category).all()
    
    def get_categories(self) -> List[str]:
        """
        Retorna todas as categorias únicas.
        
        Returns:
            Lista de nomes de categorias
        """
        result = self.db.query(Product.product_category_name).distinct().all()
        return [r[0] for r in result if r[0]]

"""
Repository para operações com customers.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.customer import Customer
from backend.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """
    Repository para operações específicas de customers.
    """
    
    def __init__(self, db: Session):
        super().__init__(Customer, db)
    
    def get_by_unique_id(self, customer_unique_id: str) -> Optional[Customer]:
        """
        Busca um cliente pelo customer_unique_id.
        
        Args:
            customer_unique_id: Identificador único agregado
            
        Returns:
            Instância de Customer ou None
        """
        return self.db.query(Customer).filter(Customer.customer_unique_id == customer_unique_id).first()
    
    def get_by_state(self, state: str) -> List[Customer]:
        """
        Busca clientes por estado.
        
        Args:
            state: Sigla do estado (UF)
            
        Returns:
            Lista de clientes do estado
        """
        return self.db.query(Customer).filter(Customer.customer_state == state).all()
    
    def get_by_city(self, city: str) -> List[Customer]:
        """
        Busca clientes por cidade.
        
        Args:
            city: Nome da cidade
            
        Returns:
            Lista de clientes da cidade
        """
        return self.db.query(Customer).filter(Customer.customer_city == city).all()

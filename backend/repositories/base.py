"""
Repository base com operações CRUD genéricas.
"""
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Repository base com operações CRUD genéricas.
    
    Implementa o padrão Repository para abstrair o acesso ao banco de dados.
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Inicializa o repository.
        
        Args:
            model: Classe do modelo SQLAlchemy
            db: Sessão do banco de dados
        """
        self.model = model
        self.db = db
    
    def create(self, obj_in: dict) -> ModelType:
        """
        Cria um novo registro.
        
        Args:
            obj_in: Dicionário com os dados do objeto
            
        Returns:
            Instância do modelo criado
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def get(self, id: int) -> Optional[ModelType]:
        """
        Busca um registro por ID.
        
        Args:
            id: ID do registro
            
        Returns:
            Instância do modelo ou None
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Busca todos os registros com paginação.
        
        Args:
            skip: Quantidade de registros para pular
            limit: Quantidade máxima de registros
            
        Returns:
            Lista de instâncias do modelo
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        """
        Atualiza um registro.
        
        Args:
            id: ID do registro
            obj_in: Dicionário com os dados para atualizar
            
        Returns:
            Instância do modelo atualizada ou None
        """
        db_obj = self.get(id)
        if db_obj:
            for field, value in obj_in.items():
                setattr(db_obj, field, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """
        Deleta um registro.
        
        Args:
            id: ID do registro
            
        Returns:
            True se deletado, False se não encontrado
        """
        db_obj = self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        """
        Conta o total de registros.
        
        Returns:
            Número total de registros
        """
        return self.db.query(self.model).count()

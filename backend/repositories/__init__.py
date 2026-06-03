"""
Repositories do projeto - Dataset Olist.
"""
from backend.repositories.base import BaseRepository
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.product_repository import ProductRepository
from backend.repositories.order_repository import OrderRepository
from backend.repositories.order_item_repository import OrderItemRepository
from backend.repositories.order_payment_repository import OrderPaymentRepository
from backend.repositories.kpi_repository import KPIRepository

__all__ = [
    "BaseRepository",
    "CustomerRepository",
    "ProductRepository",
    "OrderRepository",
    "OrderItemRepository",
    "OrderPaymentRepository",
    "KPIRepository"
]

"""
Modelos SQLAlchemy do projeto - Dataset Olist.
"""
from backend.models.customer import Customer
from backend.models.product import Product
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.order_payment import OrderPayment

__all__ = ["Customer", "Product", "Order", "OrderItem", "OrderPayment"]

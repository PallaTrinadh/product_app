from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum,uuid
from product_app.database import Base


class OrderStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)



class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, index=True)
    status = Column(Enum(OrderStatus), nullable=False)
    total = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(String(36), ForeignKey("orders.id"))
    product_id = Column(String(250), ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship("Order", back_populates="items")

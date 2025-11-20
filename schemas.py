from pydantic import BaseModel
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# --------------------------
# PRODUCT SCHEMAS
# --------------------------

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    stock: int

    model_config = {
        "from_attributes": True
    }


# --------------------------
# ORDER ITEM SCHEMAS
# --------------------------

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int


class OrderItemResponse(BaseModel):
    product_id:str
    quantity: int
    unit_price: float

    model_config = {
        "from_attributes": True
    }


# --------------------------
# ORDER SCHEMAS
# --------------------------

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: str
    status: OrderStatus
    total: float
    items: List[OrderItemResponse]

    model_config = {
        "from_attributes": True
    }


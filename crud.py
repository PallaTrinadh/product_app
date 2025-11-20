from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import uuid


def create_order(db: Session, order_data: schemas.OrderCreate):

    order_id = str(uuid.uuid4())

    # 1) CHECK STOCK
    products = {
        p.id: p for p in db.query(models.Product)
        .filter(models.Product.id.in_([i.product_id for i in order_data.items]))
        .with_for_update()
    }

    total = 0

    # Check each product stock
    for item in order_data.items:
        if item.product_id not in products:
            raise HTTPException(404, f"Product {item.product_id} not found")

        product = products[item.product_id]
        if product.stock < item.quantity:
            # FAIL ORDER
            order = models.Order(id=order_id, status=models.OrderStatus.FAILED, total=0)
            db.add(order)
            db.commit()
            db.refresh(order)
            return order

        total += product.price * item.quantity

    # 2) ORDER SUCCESS → create order row
    order = models.Order(id=order_id, status=models.OrderStatus.SUCCESS, total=total)
    db.add(order)
    db.flush()

    # 3) DEDUCT STOCK
    for item in order_data.items:
        product = products[item.product_id]
        product.stock -= item.quantity

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order


def cancel_order(db: Session, order_id: str):

    order = db.query(models.Order).filter(models.Order.id == order_id).with_for_update().first()
    if not order:
        raise HTTPException(404, "Order not found")

    # Restore stock if SUCCESS
    if order.status == models.OrderStatus.SUCCESS:
        for item in order.items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
            product.stock += item.quantity

    order.status = models.OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    return order


def list_orders(db: Session, status=None):
    q = db.query(models.Order)
    if status:
        q = q.filter(models.Order.status == status)
    return q.all()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from product_app.database import get_db
from product_app import schemas, crud

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@router.post("/{order_id}/cancel", response_model=schemas.OrderResponse)
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    return crud.cancel_order(db, order_id)


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    return crud.get_order(db, order_id)


@router.get("/", response_model=list[schemas.OrderResponse])
def list_orders(status: schemas.OrderStatus | None = None, db: Session = Depends(get_db)):
    return crud.list_orders(db, status)

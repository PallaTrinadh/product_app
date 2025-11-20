from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from product_app.database import get_db
from product_app import models, schemas

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    p = models.Product(**product.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("/", response_model=list[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

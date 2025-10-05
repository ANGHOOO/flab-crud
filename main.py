from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from app.crud import product as crud_product
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

app = FastAPI()


@app.get("/")
def root():
    return {"message": "CRUD with SQLAlchemy & Alembic"}


@app.get("/products")
def get_all_count_products(db: Session = Depends(get_db)):
    result = crud_product.get_all_product_count(db)
    return {"product count": result}


@app.get(
    "/product/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return crud_product.get_product_by_id(db, id)


@app.post(
    "/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product_data)


@app.patch("/products/", status_code=status.HTTP_200_OK)
def update_product(update: ProductUpdate, id: int, db: Session = Depends(get_db)):
    result = crud_product.update_product_by_id(db, id, update)
    return {"Update": result}


@app.delete("/product/{id}", status_code=status.HTTP_200_OK)
def delete_product_by_id(id: int, db: Session = Depends(get_db)):
    result = crud_product.delete_product_by_id(db, id)
    return {"Delete": result}

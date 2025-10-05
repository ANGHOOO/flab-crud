from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: int
    quantity: int
    description: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    quantity: int | None = None
    description: str | None = None


class ProductResponse(BaseModel):
    product_id: int
    name: str
    price: int
    quantity: int
    description: str | None = None

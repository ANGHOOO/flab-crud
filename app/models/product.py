from sqlalchemy import Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(
        Identity(always=True, start=1, cycle=False),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Product(id={self.product_id}, name='{self.name}', price={self.price})>"
        )

import logging

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


def create_product(db: Session, product_data: ProductCreate):
    db_product = Product(
        name=product_data.name,
        price=product_data.price,
        quantity=product_data.quantity,
        description=product_data.description,
    )

    try:
        db.add(db_product)
        db.commit()
        logger.info(f"상품 {db_product.name} 등록 완료")
        return db_product

    except Exception as e:
        db.rollback()
        logger.error(f"상품 {db_product.name} 등록 실패: {str(e)}")
        raise


def get_product_by_id(db: Session, id: int) -> Product | None:
    try:
        found_product = db.get(Product, id)
        if found_product:
            logger.info(f"상품 {id}번 조회 완료")
        else:
            logger.warning(f"상품 {id} 조회 실패")
        return found_product

    except Exception as e:
        logger.error(f"상품 {id}번 조회 중 에러 발생: {str(e)}")
        raise


def update_product_by_id(db: Session, id: int, product_data: ProductUpdate) -> bool:
    try:
        update_data = product_data.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning("업데이트 할 데이터가 없습니다.")
            return False

        stmt = update(Product).where(Product.product_id == id).values(**update_data)
        result = db.execute(stmt)
        db.commit()

        if result.rowcount:
            logger.info(f"상품 {id}번 업데이트 완료")
            return True
        else:
            logger.warning(f"상품{id} 조회 실패")
            return False

    except Exception as e:
        db.rollback()
        logger.error(f"상품 {id}번 업데이트 실패")
        raise


def delete_product_by_id(db: Session, id: int) -> bool:
    try:
        stmt = delete(Product).where(Product.product_id == id)
        result = db.execute(stmt)
        db.commit()

        if result.rowcount:
            logger.info(f"상품{id}번 삭제 완료")
            return True
        else:
            logger.warning(f"상품{id}번 조회 실패")
            return False

    except Exception as e:
        db.rollback()
        logger.error(f"상품{id}번 삭제에 실패하였습니다.: {str(e)}")
        raise


def get_all_product_count(db: Session):
    try:
        stmt = select(func.count(Product.product_id))
        result = db.execute(stmt).scalar()
        logger.info(f"전체 상품 개수: {result}개")
        return result

    except Exception as e:
        logger.error(f"상품 개수 조회 실패: {str(e)}")
        raise

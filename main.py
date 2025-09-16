from fastapi import FastAPI, status 
from pydantic import BaseModel

import psycopg
import dotenv
import logging
import os 

logger = logging.getLogger(__name__)

app = FastAPI()


dotenv.load_dotenv()
DB_URL = os.environ["DATABASE_URL"]
    
class Product(BaseModel):
    name: str 
    price: int 
    quantity: int 
    description: str | None = None 

# CRUD
# 1. Create -> table 구조에 맞게 name, price, quantity, description 전송하면 데이터 저장
@app.post("/products/")
def create_product(product: Product):
    product_name = product.name
    product_price = product.price
    product_quantity = product.quantity
    product_description = None 
    if product.description is not None:
        product_description = product.description

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                            INSERT INTO products (name, price, quantity, description)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (product_name, product_price, product_quantity, product_description)
                            )
        logger.info(f"{product_name} 제품 등록에 성공하였습니다.")
        return {"product": product}
    
    except Exception as e:
        logger.error(f"제품 등록에 실패하였습니다. {str(e)}")            

# 2. Read -> product_id를 기준으로 제품 정보 조회
@app.get("/products/{product_id}")
def get_product(product_id: int):
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(""" 
                            SELECT
                                * 
                            FROM 
                                products
                            WHERE
                                product_id = (%s)
                            """,
                            (product_id, ))
        
                result = cur.fetchone()

        logger.info(f"result: {result}")
        logger.info(f"{product_id} 아이템 조회 성공")
        return {"product": result}
    
    except Exception as e:
        logger.error(f"{product_id} 제품 조회에 실패하였습니다.: {str(e)}")

# 3. Update -> 제품 가격이 바뀌는 경우 제품 정보 업데이트
@app.post("/products/{product_id}")
def update_product_price(product_id:int, price: int):
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE
                                products
                            SET
                                price = %s
                            WHERE
                                product_id = %s
                            """,
                            (price, product_id)
                )

        logger.info(f"{product_id} 제품 가격 변경 완료")
        return "ok"
    
    except Exception as e:
        logger.error(f"제품 가격 업데이트에 실패하였습니다. {str(e)}")

# 4. Delete -> 제품이 단종되었다고 가정하고 제품 삭제
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            DELETE FROM products
                            WHERE product_id = %s
                            """,
                            (product_id,))
    
        logger.info(f"{product_id} 제품 삭제 완료")
        return "삭제완료"    
    
    except Exception as e:
        logger.error(f"{product_id} 제품 삭제에 실패하였습니다. {str(e)}")

    


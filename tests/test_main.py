from fastapi.testclient import TestClient

from app.schemas.product import ProductCreate


def test_get_all_count_products(db_client: TestClient):
    product1 = ProductCreate(
        name="test1",
        price=100,
        quantity=10,
        description="test1",
    )
    product2 = ProductCreate(
        name="test2",
        price=100,
        quantity=10,
        description="test2",
    )

    db_client.post(
        "/products",
        json=product1.model_dump(),
    )
    db_client.post(
        "/products",
        json=product2.model_dump(),
    )

    response = db_client.get("/products")
    assert response.status_code == 200
    assert response.json()["product count"] == 2


def test_create_product(db_client: TestClient):
    test_product = ProductCreate(
        name="Test Product",
        price=100,
        quantity=10,
        description="Test Product Description",
    )

    response = db_client.post("/products", json=test_product.model_dump())
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["name"] == test_product.name
    assert response_data["price"] == test_product.price
    assert response_data["quantity"] == test_product.quantity
    assert response_data["description"] == test_product.description
    assert "product_id" in response_data


def test_get_product_by_id(db_client: TestClient):
    test_product = ProductCreate(
        name="Test Product",
        price=100,
        quantity=10,
    )
    db_client.post(
        "/products",
            json=test_product.model_dump(),
    )
    response = db_client.get("/products/1")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["product_id"] == 1


def test_update_product():
    assert False


def test_delete_product_by_id():
    assert False

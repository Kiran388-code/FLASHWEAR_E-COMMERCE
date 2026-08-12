import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_products():
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_orders_flow():
    # 1. Create order
    payload = {
        "delivery_address": "Koramangala, Bangalore",
        "payment_method": "UPI"
    }
    response = client.post("/api/orders/", json=payload)
    assert response.status_code == 201
    order = response.json()
    assert "order_number" in order

    # 2. Get order details
    order_num = order["order_number"]
    response = client.get(f"/api/orders/{order_num}")
    assert response.status_code == 200

    # 3. Step progression
    step_resp = client.patch(f"/api/orders/{order_num}/step", json={"step_number": 4, "status": "WAREHOUSE_RECEIVED"})
    assert step_resp.status_code == 200
    assert step_resp.json()["step_number"] == 4

def test_rider_flow():
    profile = client.get("/api/rider/profile")
    assert profile.status_code == 200
    assert profile.json()["name"] == "Rahul Kumar"

    otp_resp = client.post("/api/rider/verify-otp", json={"order_id": 123, "otp": "2587"})
    assert otp_resp.status_code == 200
    assert otp_resp.json()["verified"] is True

def test_ai_features():
    try_on = client.post("/api/ai/virtual-try-on", json={"product_id": 1})
    assert try_on.status_code == 200
    assert try_on.json()["status"] == "success"

    size_rec = client.post("/api/ai/size-recommendation", json={"height_cm": 175.0, "weight_kg": 72.0})
    assert size_rec.status_code == 200
    assert "recommended_size" in size_rec.json()

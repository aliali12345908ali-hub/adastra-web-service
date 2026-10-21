from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "Adastra CaaS Ecosystem"
    assert data["status"] == "Operational"

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests_handled" in data
    assert data["status"] == "Healthy"

def test_caas_scan_endpoint():
    response = client.post("/caas/scan?target=example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["target"] == "example.com"
    assert "task_id" in data

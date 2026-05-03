"""
Basic tests for the API gateway
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Vois Capture API Gateway" in data["message"]
    assert "version" in data
    assert "docs" in data
    assert "health" in data


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_create_capture(client):
    """Test capture creation"""
    response = client.post(
        "/api/v1/captures/",
        json={"title": "Test Capture", "description": "A test capture"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "capture_id" in data
    assert data["title"] == "Test Capture"
    assert data["status"] == "created"
    assert "created_at" in data

    capture_id = data["capture_id"]

    # Test getting capture status
    response = client.get(f"/api/v1/captures/{capture_id}/status")
    assert response.status_code == 200
    status_data = response.json()
    assert status_data["capture_id"] == capture_id
    assert status_data["status"] == "created"


def test_capture_not_found(client):
    """Test 404 for non-existent capture"""
    response = client.get("/api/v1/captures/non-existent-id/status")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_invalid_file_type(client):
    """Test invalid file type rejection"""
    # Create a capture first
    response = client.post(
        "/api/v1/captures/",
        json={"title": "Test Capture"}
    )
    capture_id = response.json()["capture_id"]

    # Try to upload invalid file type
    response = client.post(
        f"/api/v1/captures/{capture_id}/images",
        files={"file": ("test.txt", b"invalid content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__])
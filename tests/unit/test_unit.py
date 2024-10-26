import pytest
from fastapi.testclient import TestClient
from app.main import app  # Assuming `app` is your FastAPI instance

client = TestClient(app)

@pytest.fixture
def mock_image_buffer():
    return b"fake_image_data"

def test_health_check():
    """Test the health check endpoint of the service."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_upload_image(mock_image_buffer):
    """Test uploading an image via the file service."""
    files = {"file": ("test_image.png", mock_image_buffer, "image/png")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert "file_name" in response.json()

def test_predict(mock_image_buffer):
    """Test predicting an image classification."""
    response = client.post(
        "/predict/",
        json={
            "file_name": "test_image.png",
            "image_buffer": mock_image_buffer
        }
    )
    assert response.status_code == 200
    assert "classification" in response.json()
    assert "probabilities" in response.json()

import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import Session
from app.db import get_db, Base
from app.db import engine  # Assuming SQLAlchemy engine is configured here
from app.models import prediction_result  # Import model for tests

client = TestClient(app)

@pytest.fixture
def db_session():
    """Creates a new database session for a test."""
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_end_to_end_image_prediction(mock_image_buffer, db_session):
    """Test the complete workflow: upload image -> predict -> save to DB."""
    
    # 1. Upload an image
    files = {"file": ("test_image.png", mock_image_buffer, "image/png")}
    upload_response = client.post("/upload", files=files)
    assert upload_response.status_code == 200
    file_name = upload_response.json()["file_name"]

    # 2. Perform a prediction on the uploaded image
    predict_response = client.post(
        "/predict/",
        json={
            "file_name": file_name,
            "image_buffer": mock_image_buffer
        }
    )
    assert predict_response.status_code == 200
    classification = predict_response.json()["classification"]

    # 3. Check if the result is saved in the DB
    result = db_session.query(prediction_result).filter_by(file_name=file_name).first()
    assert result is not None
    assert result.classification == classification

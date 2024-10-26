from fastapi import APIRouter, BackgroundTasks, Depends
from app.rabbitmq import consume_image_buffer
from src.models.classifier import Classifier
from sqlalchemy.orm import Session
from app.db import get_db, insert_prediction_result

router = APIRouter()

@router.post("/predict/")
async def predict(file_name: str, image_buffer: bytes, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Initialize the classifier with the model path
    classifier = Classifier(model_path='path/to/your/model.pth', db_session=db)

    # Get predictions from the classifier
    classification, probabilities = classifier.predict(image_buffer, file_name)

    # Log or handle predictions as needed (e.g., save to DB)
      # Save the prediction result to the database
    await insert_prediction_result(file_name, classification, probabilities)
    
    return {
        "file_name": file_name,
        "classification": classification,
        "probabilities": probabilities
    }



import torch
from torchvision import transforms
from PIL import Image
from sqlalchemy.orm import Session
from .prediction_result import PredictionResult

class Classifier:
    def __init__(self, model_path: str, db_session: Session):
        self.model = torch.load(model_path)
        self.model.eval()  # Set the model to evaluation mode
        self.db_session = db_session
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def predict(self, image_buffer: bytes, file_name: str):
        image = Image.open(io.BytesIO(image_buffer)).convert("RGB")
        image = self.transform(image).unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            output = self.model(image)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)

        # Get the predicted class index and probabilities
        _, predicted_class_index = torch.max(probabilities, dim=0)
        predicted_class = str(predicted_class_index.item())
        probabilities_dict = probabilities.tolist()  # Convert to a list for JSON storage

        # Save prediction result to the database
        self.save_prediction(file_name, predicted_class, probabilities_dict)

        return predicted_class, probabilities_dict

    def save_prediction(self, file_name: str, classification: str, probabilities: list):
        prediction_result = PredictionResult(
            file_name=file_name,
            classification=classification,
            probabilities=probabilities
        )
        self.db_session.add(prediction_result)
        self.db_session.commit()

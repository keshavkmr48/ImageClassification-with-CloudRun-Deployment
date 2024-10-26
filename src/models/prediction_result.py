from sqlalchemy import Column, Integer, String, JSON
from app.db import Base

class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    classification = Column(String)
    probabilities = Column(JSON)

    def __repr__(self):
        return f"<PredictionResult(file_name={self.file_name}, classification={self.classification}, probabilities={self.probabilities})>"

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database.models import Base

class Prediction(Base):
    __tablename__ = 'Predictions'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Results
    actual_class = Column(String, nullable=True)
    predicted_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    source = Column(String, nullable=False)

    # Foreign Keys
    inference_input_id = Column(Integer, ForeignKey('Inference-Inputs.id'), nullable=True)
    processed_features_id = Column(Integer, ForeignKey('Processed-Features.id'), nullable=True)
from pydantic import BaseModel
from typing import Optional

class Prediction(BaseModel):
    id: Optional[int] = None

    # Results
    actual_class: Optional[str] = None
    predicted_class: str
    confidence: float
    source: str


    # Foreign Keys
    inference_input_id: Optional[int] = None
    processed_features_id: Optional[int] = None

from typing import List
from app.database.database import database
from app.schemas.prediction import Prediction
from app.database.models.prediction import Prediction as PredictionModel

class PredictionCRUD:
    def __init__(self):
        if database:
            self.db = database
        else:
            print("Database does not connected!")

    def create(self, prediction: Prediction) -> Prediction:
        try:
            prediction_model = PredictionModel(
                predicted_class=prediction.predicted_class,
                confidence=prediction.confidence,
                source=prediction.source,
                actual_class=prediction.actual_class,
                inference_input_id=prediction.inference_input_id,
                processed_features_id=prediction.processed_features_id
            )

            self.db.session.add(prediction_model)
            self.db.session.commit()
            self.db.session.refresh(prediction_model)
            
            return self._sqlalchemy_to_pydantic(prediction_model)

        except Exception as e:
            self.db.session.rollback()
            print(f"Error creating prediction: {e}")
            return None
    
    def get_by_id(self, prediction_id: int) -> Prediction:
        try:
            prediction_model = self.db.session.query(PredictionModel).filter(
                PredictionModel.id == prediction_id
            ).first()
            
            if prediction_model:
                return self._sqlalchemy_to_pydantic(prediction_model)
            return None
            
        except Exception as e:
            print(f"Error getting prediction by id: {e}")
            return None
    
    def get_all(self, limit: int = None, source: str = None) -> List[Prediction]:
        try:
            query = self.db.session.query(PredictionModel)
            if source:
                query = query.filter(PredictionModel.source == source)
            
            if limit:
                query = query.limit(limit)
            
            prediction_models = query.all()
            
            return [self._sqlalchemy_to_pydantic(model) for model in prediction_models]
            
        except Exception as e:
            print(f"Error getting all predictions: {e}")
            return []

    def _sqlalchemy_to_pydantic(self, prediction_model: PredictionModel) -> Prediction:
        return Prediction(
            id=prediction_model.id,
            predicted_class=prediction_model.predicted_class,
            confidence=prediction_model.confidence,
            source=prediction_model.source,
            actual_class=prediction_model.actual_class
        )

prediction_crud = PredictionCRUD()
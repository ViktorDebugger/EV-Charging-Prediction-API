from app.services.utils.processed_feature import sqlalchemy_to_pydantic
from app.database.database import database
from typing import List
from app.schemas.processed_feature import ProcessedFeature
from app.database.models.processed_feature import ProcessedFeature as ProcessedFeatureModel

class ProcessedFeaturesCRUD:
    def __init__(self):
        if database:
            self.db = database
        else:
            print("Database does not connected!")

    def get_by_id(self, feature_id: int) -> ProcessedFeature:
        try:
            feature_model = self.db.session.query(ProcessedFeatureModel).filter(
                ProcessedFeatureModel.id == feature_id
            ).first()
            
            if feature_model:
                return sqlalchemy_to_pydantic(feature_model)
            return None
            
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_all(self, limit: int = None) -> List[ProcessedFeature]:
        try:
            if limit:
                feature_models = self.db.session.query(ProcessedFeatureModel).limit(limit).all()
            else:
                feature_models = self.db.session.query(ProcessedFeatureModel).all()
            
            return [sqlalchemy_to_pydantic(model) for model in feature_models]
            
        except Exception as e:
            print(f"Error: {e}")
            return []

processed_crud = ProcessedFeaturesCRUD()
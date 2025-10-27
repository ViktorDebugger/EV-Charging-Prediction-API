from typing import List
from app.database.database import database
from app.schemas.inference_input import InferenceInput
from app.services.utils.inference_input import InferenceInputModel, generate_random_datetime, pydantic_to_sqlalchemy, sqlalchemy_to_pydantic

class InferenceInputCRUD:
    def __init__(self):
        if database:
            self.db = database
        else:
            print("Database does not connected!")
    
    def create(self, inference_input: InferenceInput) -> InferenceInput:
        try:

            inference_input.timestamp = generate_random_datetime()

            inference_model = pydantic_to_sqlalchemy(inference_input)
            
            self.db.session.add(inference_model)
            self.db.session.commit()
            self.db.session.refresh(inference_model)
            
            return sqlalchemy_to_pydantic(inference_model)
            
        except Exception as e:
            self.db.session.rollback()
            print(f"Error: {e}")
            return None
    
    def get_by_id(self, inference_id: int) -> InferenceInput:
        try:
            inference_model = self.db.session.query(InferenceInputModel).filter(
                InferenceInputModel.id == inference_id
            ).first()
            
            if inference_model:
                return sqlalchemy_to_pydantic(inference_model)
            return None
            
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_all(self, limit: int = None) -> List[InferenceInput]:
        try:
            if limit:
                inference_models = self.db.session.query(InferenceInputModel).limit(limit).all()
            else:
                inference_models = self.db.session.query(InferenceInputModel).all()
            
            return [sqlalchemy_to_pydantic(model) for model in inference_models]
            
        except Exception as e:
            print(f"Error: {e}")
            return []

inference_crud = InferenceInputCRUD()
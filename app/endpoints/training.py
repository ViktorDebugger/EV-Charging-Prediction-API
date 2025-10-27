from fastapi import APIRouter, HTTPException
from app.database.crud.processed_feature import processed_crud
from app.database.crud.prediction import prediction_crud
from app.schemas.prediction import Prediction
from app.services.utils.processed_feature import prepare_dataframe, prepare_data, split_data
from app.services.model import svc_model
import numpy as np
from app.services.utils.logger import model_logger

router = APIRouter()

@router.post("/train_model")
async def train_model():
    try:
        all_features = processed_crud.get_all()

        if not all_features:
            raise HTTPException(status_code=404, detail="No data found")
        
        features_df = prepare_dataframe(all_features)

        prepared_X, prepared_y = prepare_data(features_df)

        X_train, y_train, X_test, y_test = split_data(prepared_X, prepared_y)

        training_result = svc_model.train(X_train, y_train, X_test, y_test)

        if training_result["status"] == "error":
            raise HTTPException(status_code=500, detail=training_result["message"])

        svc_model.save_model()

        classification_rep = training_result["classification_report"]
        
        weighted_avg = classification_rep.get("weighted avg", {})
        precision = weighted_avg.get("precision", 0.0)
        recall = weighted_avg.get("recall", 0.0)
        f1_score = weighted_avg.get("f1-score", 0.0)

        model_logger.log_training(
            status="success",
            accuracy=training_result["accuracy"],
            train_size=training_result["train_size"],
            test_size=training_result["test_size"],
            classes=training_result["classes"],
            additional_info={
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "confusion_matrix": training_result["confusion_matrix"],
                "classification_report": classification_rep
            }
        )

        predictions_saved = 0
        try:
            train_indices = X_train.index

            y_train_pred = svc_model.model.predict(X_train)
            y_train_proba = svc_model.model.predict_proba(X_train)
            y_train_confidence = np.max(y_train_proba, axis=1)
            
            for idx, (pred_class, confidence, actual_class) in enumerate(zip(
                y_train_pred, 
                y_train_confidence, 
                y_train.values
            )):

                original_idx = train_indices[idx]
                processed_feature_id = all_features[original_idx].id

                prediction = Prediction(
                    predicted_class=str(pred_class),
                    confidence=float(confidence),
                    actual_class=str(actual_class),
                    source="train",
                    processed_features_id=processed_feature_id
                )
                
                saved = prediction_crud.create(prediction)
                if saved:
                    predictions_saved += 1
                    
        except Exception as e:
            print(f"Warning: Could not save train predictions: {e}")

        return {
            "message": "Model trained successfully",
            "accuracy": training_result["accuracy"],
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "train_size": training_result["train_size"],
            "test_size": training_result["test_size"],
            "classes": training_result["classes"],
            "confusion_matrix": training_result["confusion_matrix"],
            "classification_report": classification_rep
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
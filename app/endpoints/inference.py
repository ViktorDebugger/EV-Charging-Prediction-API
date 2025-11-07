from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.inference_input import InferenceInput
from app.database.crud.inference_input import inference_crud
from app.database.crud.prediction import prediction_crud
from app.database.crud.processed_feature import processed_crud
from app.services.model import svc_model
from app.schemas.prediction import Prediction
from app.services.utils.logger import model_logger
import os
import time

from app.services.utils.inference_input import prepare_input_for_prediction, validate_categorical_fields, validate_input_data
from app.services.utils.processed_feature import prepare_dataframe

router = APIRouter()

@router.post("/predict")
async def predict(input_data: InferenceInput):
    missing_fields = validate_input_data(input_data)

    if len(missing_fields):
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": "Not all required fields are filled in",
                "missing_fields": missing_fields,
            }
        )
    
    validation_result = validate_categorical_fields(input_data)
    
    if validation_result['invalid_fields']:
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": "Invalid categorical values",
                "invalid_fields": validation_result['invalid_fields'],
                "errors": validation_result['errors']
            }
        )

    start_time = time.time()

    try:
        saved_data = inference_crud.create(input_data)

        if not saved_data:
            raise HTTPException(status_code=500, detail="Failed to save data")

        model_path = "models/svc_model.pkl"
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model not found. Please train the model first.")
        
        svc_model.load_model(model_path)

        trained_data = processed_crud.get_all()

        trained_df = prepare_dataframe(trained_data)

        df = prepare_input_for_prediction(saved_data, trained_df)

        result = svc_model.predict(df)

        if result["status"] == "success":
            prediction_result = result["predictions"][0]
            processing_time = time.time() - start_time


            prediction = Prediction(
                predicted_class=str(prediction_result["predicted_class"]),
                confidence=float(prediction_result["confidence"]),
                source="inference",
                inference_input_id=saved_data.id
            )

            saved_prediction = prediction_crud.create(prediction)

            model_logger.log_inference(
                input_data=input_data.dict(),
                predicted_class=prediction_result["predicted_class"],
                confidence=prediction_result["confidence"],
                status="success",
                processing_time=processing_time,
                inference_input_id=saved_data.id
            )

            return {
                "status": "success",
                "predicted_class": prediction_result["predicted_class"],
                "confidence": prediction_result["confidence"],
                "processing_time": round(processing_time, 4),
                "input_summary": {
                    "user_id": input_data.user_id,
                    "vehicle_model": input_data.vehicle_model,
                    "charging_station_location": input_data.charging_station_location,
                    "user_type": input_data.user_type
                },
                "saved_prediction_id": saved_prediction.id if saved_prediction else None
            }
        else:
            processing_time = time.time() - start_time
            error_msg = result.get("message", "Prediction failed")
            
            model_logger.log_inference(
                input_data=input_data.dict(),
                status="error",
                error_message=error_msg,
                processing_time=processing_time
            )
            
            raise HTTPException(status_code=500, detail=error_msg)

    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        
        model_logger.log_inference(
            input_data=input_data.dict() if input_data else {},
            status="error",
            error_message=str(e),
            processing_time=processing_time
        )
        
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
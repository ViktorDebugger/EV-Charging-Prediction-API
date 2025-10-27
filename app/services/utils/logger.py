import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class ModelLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.training_log_file = self.log_dir / "training.log"
        self.inference_log_file = self.log_dir / "inference.log"
    
    def log_training(
        self, 
        status: str,
        accuracy: Optional[float] = None,
        train_size: Optional[int] = None,
        test_size: Optional[int] = None,
        classes: Optional[list] = None,
        error_message: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> None:

        timestamp = datetime.now().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "type": "training",
            "status": status,
            "accuracy": accuracy,
            "train_size": train_size,
            "test_size": test_size,
            "classes": classes,
            "error_message": error_message
        }

        if additional_info:
            log_entry.update(additional_info)
        
        self._write_log(self.training_log_file, log_entry)
    

    def log_inference(self,
        input_data: Dict[str, Any],
        predicted_class: Optional[str] = None,
        confidence: Optional[float] = None,
        probabilities: Optional[Dict[str, float]] = None,
        status: str = "success", 
        error_message: Optional[str] = None,
        processing_time: Optional[float] = None,
        inference_input_id: Optional[int] = None
    ) -> None:

        timestamp = datetime.now().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "type": "inference",
            "status": status,
            "inference_input_id": inference_input_id,
            "input_data": {
                "user_id": input_data.get("user_id"),
                "vehicle_model": input_data.get("vehicle_model"),
                "charging_station_location": input_data.get("charging_station_location"),
                "user_type": input_data.get("user_type")
            },
            "prediction": {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "probabilities": probabilities
            },
            "processing_time": processing_time,
            "error_message": error_message
        }
        
        # Записуємо у файл
        self._write_log(self.inference_log_file, log_entry)

        
    def _write_log(self, log_file: Path, log_entry: Dict[str, Any]) -> None:
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error writing log: {e}")

model_logger = ModelLogger()
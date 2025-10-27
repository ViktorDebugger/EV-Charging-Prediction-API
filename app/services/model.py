import pickle
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Dict, Any
import os

class SVCModel:
    def __init__(self):
        self.model = SVC(kernel='linear', random_state=42, probability=True)
        self.is_trained = False
        self.feature_names = []
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
        try:
            self.feature_names = X_train.columns.tolist()

            self.model.fit(X_train, y_train)
            self.is_trained = True

            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)

            classification_rep = classification_report(
                y_test, y_pred, 
                output_dict=True,
                zero_division=0
            )
            
            confusion_mat = confusion_matrix(y_test, y_pred)

            unique_classes = sorted(y_train.unique().tolist())
            
            return {
                "status": "success",
                "accuracy": float(accuracy),
                "classification_report": classification_rep,
                "confusion_matrix": confusion_mat.tolist(),
                "classes": unique_classes,
                "n_features": len(self.feature_names),
                "train_size": len(X_train),
                "test_size": len(X_test)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def predict(self, X: pd.DataFrame) -> Dict[str, Any]:

        try:
            if not self.is_trained:
                raise ValueError("Model is not trained yet! Please load or train the model first.")

            missing_features = set(self.feature_names) - set(X.columns)
            if missing_features:
                raise ValueError(f"Missing features: {missing_features}")

            X_ordered = X[self.feature_names]

            prediction = self.model.predict(X_ordered)

            probabilities = self.model.predict_proba(X_ordered)

            confidence = probabilities.max(axis=1)

            class_names = self.model.classes_

            results = []

            for i in range(len(prediction)):
                class_probabilities = {
                    str(class_name): float(prob) 
                    for class_name, prob in zip(class_names, probabilities[i])
                }
                
                results.append({
                    'predicted_class': str(prediction[i]),
                    'confidence': float(confidence[i]),
                })
            
            return {
                "status": "success",
                "predictions": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def save_model(self, filepath: str = "models/svc_model.pkl"):
        if not self.is_trained:
            raise ValueError("Model is not trained yet!")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        model_data = {
            'model': self.model,
            'is_trained': self.is_trained,
            'feature_names': self.feature_names
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath: str = "models/svc_model.pkl"):
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
            
        self.model = model_data['model']
        self.is_trained = model_data['is_trained']
        self.feature_names = model_data['feature_names']

svc_model = SVCModel()
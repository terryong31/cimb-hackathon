import json
import pandas as pd
import mlflow
import os
import logging

def init():
    global model
    # Setup logging to see errors in Azure Logs
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 1. Find the base path where Azure mounted the model
    base_path = os.getenv("AZUREML_MODEL_DIR")
    logger.info(f"AZUREML_MODEL_DIR is: {base_path}")

    # 2. Walk through directories to find the 'MLmodel' file or the folder
    model_path = None
    
    # Debug: Print all files in the directory to help troubleshooting
    for root, dirs, files in os.walk(base_path):
        logger.info(f"Searching: {root} | Files: {files}")
        if "MLmodel" in files or "model.pkl" in files:
            model_path = root
            break
            
    if model_path is None:
        # Fallback: try the hardcoded path if search fails
        model_path = os.path.join(base_path, "anomaly_model_dir")
    
    logger.info(f"Attempting to load model from: {model_path}")

    try:
        model = mlflow.sklearn.load_model(model_path)
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model. Error: {e}")
        raise e

def run(raw_data):
    try:
        data = json.loads(raw_data)
        input_df = pd.DataFrame(data['data'])
        
        # Predict and Score
        raw_prediction = model.predict(input_df)
        raw_scores = model.decision_function(input_df)
        
        result_list = []
        for pred, score in zip(raw_prediction, raw_scores):
            is_fraud = 1 if pred == -1 else 0
            # Normalize score (approximate)
            normalized_score = 0.5 - (score * 2.5)
            confidence = max(0.0, min(1.0, normalized_score))
            
            result_list.append({
                "fraud": is_fraud,
                "confidence_score": round(confidence, 4)
            })

        return result_list
    except Exception as e:
        return {"error": str(e)}
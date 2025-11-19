import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import IsolationForest
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

# 1. Load Data
df = pd.read_csv("bank_transactions_data_2.csv")

# 2. Select the specific features you requested
features = ['TransactionAmount', 'TransactionDuration', 'LoginAttempts', 'AccountBalance', 'CustomerAge']
X = df[features]

# 3. Train Isolation Forest (Unsupervised)
# contamination: Estimate of how much fraud is in your dataset (e.g., 0.05 = 5%)
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X)

# 4. Save Model Locally
model_path = "anomaly_model_dir"
mlflow.sklearn.save_model(model, model_path)

# 6. Register Model to Azure ML
# Connect to Azure (Replace with your details)
ml_client = MLClient(
    DefaultAzureCredential(), 
    subscription_id="<YOUR_SUBSCRIPTION_ID>", 
    resource_group_name="<YOUR_RESOURCE_GROUP>", 
    workspace_name="<YOUR_WORKSPACE_NAME>"
)

# Register the model
cloud_model = Model(
    path=model_path,
    name="bank-fraud-detection-model",
    type=AssetTypes.MLFLOW_MODEL,
    description="Model to predict fraud from transaction details"
)
ml_client.models.create_or_update(cloud_model)

print("Model registered successfully!")
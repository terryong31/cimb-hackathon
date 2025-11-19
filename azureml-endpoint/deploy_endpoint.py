from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, CodeConfiguration, Environment, OnlineRequestSettings

# Connect to Azure
ml_client = MLClient(
    DefaultAzureCredential(), 
    subscription_id="<YOUR_SUBSCRIPTION_ID>", 
    resource_group_name="<YOUR_RESOURCE_GROUP>", 
    workspace_name="<YOUR_WORKSPACE_NAME>"
)

# 1. Define the Endpoint
endpoint_name = "<YOUR_ENDPOINT_NAME>" # Name must be unique in Azure region
endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    description="Online endpoint for bank fraud detection",
    auth_mode="key"
)
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# 2. Define the Deployment
deployment = ManagedOnlineDeployment(
    name="<YOUR-DEPLOYMENT-NAME>",
    endpoint_name=endpoint_name,
    model="bank-fraud-detection-model@latest",
    instance_type="Standard_D2a_v4",
    instance_count=1,   
    
    # FIX 2: Use our custom environment instead of the curated one
    environment=Environment(
        conda_file="anomaly_model_dir/conda.yaml",
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04" # Base image
    ),
    
    code_configuration=CodeConfiguration(
        code="./", 
        scoring_script="score.py"
    ),
    
    request_settings=OnlineRequestSettings(
        max_concurrent_requests_per_instance=3000,  # Allow 3000 requests at once
        request_timeout_ms=60000,                 # Wait up to 60 seconds
        max_queue_wait_ms=60000                   # Queue wait time
    )
)

print("Deploying model... this may take a few minutes.")
ml_client.online_deployments.begin_create_or_update(deployment).result()

# 3. Route traffic to the deployment
endpoint.traffic = {"blue-deployment": 100}
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

print(f"Deployment complete. Endpoint URL: {endpoint.scoring_uri}") # Usually blank, check Azure ML website
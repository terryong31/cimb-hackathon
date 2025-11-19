# Anti-Scam Fraud Detection Dashboard

A minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning and AI-powered explanations.

---

## ✨ Highlights

- Excel/CSV upload for batch transaction analysis
- ML-based fraud scoring with optional external ML API
- AI-generated human-friendly explanations via Azure OpenAI (gpt-5-mini)
- Async processing for better throughput
- Mock-data fallback for easy local testing

## 🚀 Quick demo

Live (deployed): https://cimbxmicrosoft.azurewebsites.net
\nGive it some time to run, its Azure web app free tier, don't be shocked if it takes 5 mins to launch the site.

---

## 📋 Required Transaction Fields

The uploaded CSV/XLSX must include at least the following columns (case-sensitive):

- `TransactionAmount` — transaction amount (currency)
- `TransactionDuration` — time taken in seconds
- `LoginAttempts` — number of login attempts
- `AccountBalance` — account balance
- `CustomerAge` — customer age

If your file has extra columns, the app will ignore them.

---

## 🛠 Technology stack

- Backend: Flask (Python 3.11)
- Frontend: React 18
- Optional ML: external REST ML API
- AI: Azure OpenAI (gpt-5-mini)
- Deployment: Azure Web App (Linux) + GitHub Actions

---

## 💻 Local development (fast)

Prerequisites

- Python 3.11+
- Node.js 18+

Backend (Windows example)

```powershell
git clone https://github.com/terryong31/cimb-hackathon.git
cd cimb-hackathon
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
# create a .env file (see example below)
python app.py
```

Backend (Linux/macOS)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Frontend

```bash
cd frontend
npm install
npm start
```

The backend runs on http://localhost:5000 and the frontend on http://localhost:3000 by default.

---

## ⚙️ Environment variables

Create a `.env` file for local runs (or set these as Azure App Settings in production). Minimal example:

```
AZURE_OPENAI_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
AZURE_ML_ENDPOINT=https://<your-endpoint>.inference.ml.azure.com/score
AZURE_ML_API_KEY=your_azure_ml_api_key
PORT=8000
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

Notes:
- If `AZURE_OPENAI_*` are missing, the app will run in mock mode for explanations.
- If `AZURE_ML_ENDPOINT` and `AZURE_ML_API_KEY` are missing, the app will use mock fraud predictions.
- ML and OpenAI work independently—you can use one or both.

---

## ☁️ Azure deployment (high level)

1. Create an Azure Web App (Linux) and set runtime to **Python 3.11**.
2. In Azure Portal → Deployment Center, connect your GitHub repo (or use publish profile).
3. Add the following App Settings (Configuration → Application settings):

```
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_KEY
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
AZURE_ML_ENDPOINT
AZURE_ML_API_KEY
PORT=8000
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

4. Ensure startup command in General settings uses gunicorn:

```
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
```

5. Push to `main` and watch the GitHub Actions workflow (set `AZUREAPPSERVICE_PUBLISHPROFILE` secret if using publish-profile auth).

---

## 🤖 Azure ML Integration

Your app is now integrated with Azure ML for real-time fraud detection! The endpoint uses an XGBoost model trained on transaction patterns.

### Current Configuration

The app is configured to use:
- **Endpoint**: `https://cimbxms-hackathon-endpoint.southeastasia.inference.ml.azure.com/score`
- **Environment Variables**: `AZURE_ML_ENDPOINT` and `AZURE_ML_API_KEY`

### API Request/Response Format

**Request format:**
```json
{
  "data": [
    {
      "TransactionAmount": 157.47,
      "TransactionDuration": 169,
      "LoginAttempts": 1,
      "AccountBalance": 4120.75,
      "CustomerAge": 53
    }
  ]
}
```

**Response format:**
```json
[
  {
    "fraud": 0,              // 0 = legitimate, 1 = fraudulent
    "confidence_score": 0.0884  // fraud probability (0.0 to 1.0)
  }
]
```

### Testing the Integration

You can test the ML API integration with the provided test scripts:

```powershell
# Test ML API directly
python test_ml_integration.py

# Test full Flask app (requires app to be running)
# Terminal 1:
python app.py

# Terminal 2:
python test_app_integration.py
```

### Example Predictions

✅ **Low-risk transaction** (Normal):
- Amount: $157.47, Duration: 169s, Login Attempts: 1
- Result: `fraud=0`, confidence: 8.84%

🚨 **High-risk transaction** (Fraudulent):
- Amount: $8500, Duration: 5s, Login Attempts: 5
- Result: `fraud=1`, confidence: 89.65%

### Performance Features

- ⚡ **Async batch processing** - Processes up to 50 transactions concurrently
- 🔄 **Automatic fallback** - Uses mock predictions if ML API is unavailable
- 📊 **Real-time scoring** - ~100-200ms response time per transaction
- �️ **Error handling** - Graceful degradation with detailed logging

### Deploying Your Own Model

If you want to deploy your own fraud detection model, see the `azureml-endpoint/` directory for:
- `train-and-deploy.py` - Complete training and deployment script
- `score.py` - Scoring script for the endpoint
- `test_request.py` - Test your deployed endpoint

Configuration for your Flask app:
```powershell
# For local development (.env file)
AZURE_ML_ENDPOINT=https://your-endpoint.inference.ml.azure.com/score
AZURE_ML_API_KEY=your-api-key

# For Azure Web App
az webapp config appsettings set --name cimbxmicrosoft --resource-group cimbhackathon --settings `
  AZURE_ML_ENDPOINT="https://your-endpoint.inference.ml.azure.com/score" `
  AZURE_ML_API_KEY="your-api-key"
```

---

## 📁 Project layout

```
cimb-hackathon/
├── .github/workflows/      # CI/CD pipeline
├── azureml-endpoint/       # ML model deployment & testing
│   ├── train-and-deploy.py   # Complete training & deployment
│   ├── score.py              # Scoring script for endpoint
│   └── bank_transactions_data_2.csv  # Training data
├── frontend/               # React app
│   ├── src/
│   ├── public/
│   └── build/             # Production build
├── uploads/                # Uploaded CSV/Excel files
├── app.py                  # Flask backend
├── test_ml_integration.py  # Test ML API directly
├── test_app_integration.py # Test full app integration
├── requirements.txt
├── runtime.txt            # Python 3.11
└── README.md
```

---

## 🔌 API (backend)

- `GET /api/status` — returns service & config status
- `POST /api/upload` — upload a CSV/XLSX and get analysis
- `POST /api/explain` — request AI explanation for a flagged transaction

---

## ✅ Tips & troubleshooting

- If the frontend fails to build in GitHub Actions, make sure `frontend` build step uses `npm install` (not `npm ci`) unless package-lock.json matches exactly.
- If pandas fails to build on Azure, ensure Python runtime is 3.11 and `requirements.txt` pins a compatible pandas version (the repo already targets pandas 2.2.x).
- For Azure OpenAI: the `gpt-5-mini` deployment does not accept a custom `temperature` parameter — use the default behavior.

---

## Contributing

1. Fork the repo
2. Create a branch `git checkout -b feature/name`
3. Make changes, run tests locally
4. Push and open a Pull Request

---

If you want, I can also add a `.env.example` file and a short commit for this README change — tell me whether you want me to commit it for you or just leave the file for you to review and commit.

**Built with ❤️ for CIMB x Microsoft Hackathon**




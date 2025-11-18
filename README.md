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
Give it some time to run, its Azure web app free tier, don't be shocked if it takes 5 mins to launch the site.

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
ML_API_ENDPOINT=            # optional: https://your-ml-api.example.com/predict
PORT=8000
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

Notes:
- If `AZURE_OPENAI_*` are missing the app will run in mock mode for explanations.
- `ML_API_ENDPOINT` is optional—ML and OpenAI work independently.

---

## ☁️ Azure deployment (high level)

1. Create an Azure Web App (Linux) and set runtime to **Python 3.11**.
2. In Azure Portal → Deployment Center, connect your GitHub repo (or use publish profile).
3. Add the following App Settings (Configuration → Application settings):

```
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_KEY
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
PORT=8000
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

4. Ensure startup command in General settings uses gunicorn:

```
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
```

5. Push to `main` and watch the GitHub Actions workflow (set `AZUREAPPSERVICE_PUBLISHPROFILE` secret if using publish-profile auth).

---

## 📁 Project layout

```
cimb-hackathon/
├── .github/workflows/   # CI/CD pipeline
├── frontend/            # React app
├── uploads/             # uploaded files
├── app.py               # Flask app
├── requirements.txt
├── runtime.txt          # python runtime pinned to 3.11
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


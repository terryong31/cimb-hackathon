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
# Anti-Scam Fraud Detection Dashboard# Anti-Scam Fraud Detection Dashboard# Anti-Scam Fraud Detection Dashboard



A minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning and AI-powered explanations.



## ✨ FeaturesA minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning and AI-powered explanations.



- 📊 Excel/CSV file upload for transaction analysis

- 🤖 ML-based fraud detection  

- 🔍 AI-powered fraud explanations via Azure OpenAI## ✨ FeaturesA minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning and AI-powered explanations.A minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning.

- 🎨 CIMB brand theme (minimalistic red & white)

- 🔄 Mock data fallback when API keys are not configured

- ⚡ Async batch processing for high-volume transactions

- 📊 Excel/CSV file upload for transaction analysis

## 📋 Required Transaction Fields

- 🤖 ML-based fraud detection  

Your Excel or CSV file must contain these columns:

- `TransactionAmount` - Transaction amount- 🔍 AI-powered fraud explanations via Azure OpenAI## Features

- `TransactionDuration` - Time taken (seconds)

- `LoginAttempts` - Number of login attempts- 🎨 CIMB brand theme (minimalistic red & white)

- `AccountBalance` - Account balance

- `CustomerAge` - Customer age- 🔄 Mock data fallback when API keys are not configured



## 🛠️ Technology Stack- ⚡ Async batch processing for high-volume transactions



- **Backend**: Flask (Python 3.11)- 📊 Excel/CSV file upload for transaction analysis- 📊 Excel/CSV file upload for transaction analysis

- **Frontend**: React 18

- **ML**: REST API (optional)## 📋 Required Transaction Fields

- **AI**: Azure OpenAI gpt-5-mini

- **Deployment**: Azure Web App + GitHub Actions- 🤖 ML-based fraud detection- 🤖 ML-based fraud detection



## 🚀 Live DemoYour Excel or CSV file must contain these columns:



**https://cimbxmicrosoft.azurewebsites.net**- `TransactionAmount` - Transaction amount- 🔍 AI-powered fraud explanations via Azure OpenAI- 🔍 AI-powered fraud explanations via Azure OpenAI



## 💻 Local Development- `TransactionDuration` - Time taken (seconds)



### Prerequisites- `LoginAttempts` - Number of login attempts- 🎨 CIMB brand theme (minimalistic red & white)- 🎨 CIMB brand theme (minimalistic red & white)

- Python 3.11+

- Node.js 18+- `AccountBalance` - Account balance



### Backend Setup- `CustomerAge` - Customer age- 🔄 Mock data fallback when API keys are not configured- 🔄 Mock data fallback when API keys are not configured



```bash

# Clone and navigate

git clone https://github.com/terryong31/cimb-hackathon.git## 🛠️ Technology Stack- ⚡ Async batch processing for high-volume transactions

cd cimb-hackathon



# Create virtual environment

python -m venv venv- **Backend**: Flask (Python 3.11)## Required Transaction Fields

venv\Scripts\activate  # Windows

# source venv/bin/activate  # Linux/Mac- **Frontend**: React 18



# Install dependencies- **ML**: REST API (optional)The Excel or CSV file must contain these columns:

pip install -r requirements.txt

- **AI**: Azure OpenAI gpt-5-mini

# Create .env file with your keys

# AZURE_OPENAI_ENDPOINT=your_endpoint- **Deployment**: Azure Web App + GitHub Actions- `TransactionAmount` - Transaction amount in currency

# AZURE_OPENAI_KEY=your_key

# AZURE_OPENAI_DEPLOYMENT=gpt-5-mini



# Run backend## 🚀 Live Demo- `TransactionDuration` - Time taken for transaction (seconds)

python app.py

```



Backend: `http://localhost:5000`**https://cimbxmicrosoft.azurewebsites.net**- `LoginAttempts` - Number of login attempts



### Frontend Setup



```bash## 💻 Local Development- `AccountBalance` - Account balance

cd frontend

npm install

npm start

```### Prerequisites- `CustomerAge` - Customer age



Frontend: `http://localhost:3000`- Python 3.11+



## ☁️ Azure Deployment- Node.js 18+## Setup



### Quick Setup



1. **Create Azure Web App**### Backend Setup## Technology Stack

   - Runtime: Python 3.11 (Linux)

   - Region: Southeast Asia (Singapore)



2. **Enable Basic Auth**```bash### Backend (Flask)

   - Configuration → General settings

   - Turn ON both basic auth options# Clone and navigate



3. **Download Publish Profile**git clone https://github.com/terryong31/cimb-hackathon.git- **Backend**: Flask (Python 3.11)

   - Overview → Get publish profile

cd cimb-hackathon

4. **Add GitHub Secret**

   - Repo → Settings → Secrets → Actions- **Frontend**: React 181. Install Python dependencies:

   - Name: `AZUREAPPSERVICE_PUBLISHPROFILE`

   - Value: Paste entire `.PublishSettings` XML# Create virtual environment



5. **Add Environment Variables in Azure**python -m venv venv- **ML Integration**: REST API (optional)```bash

   - Configuration → Application settings:

   ```venv\Scripts\activate  # Windows

   AZURE_OPENAI_ENDPOINT=your_endpoint

   AZURE_OPENAI_KEY=your_key  # source venv/bin/activate  # Linux/Mac- **AI**: Azure OpenAI (optional)pip install -r requirements.txt

   AZURE_OPENAI_DEPLOYMENT=gpt-5-mini

   PORT=8000

   SCM_DO_BUILD_DURING_DEPLOYMENT=true

   ```# Install dependencies- **Deployment**: Azure Web App with GitHub Actions CI/CD```



6. **Push to Deploy**pip install -r requirements.txt

   ```bash

   git push origin main

   ```

# Create .env file with your keys

Monitor deployment: [GitHub Actions](https://github.com/terryong31/cimb-hackathon/actions)

# AZURE_OPENAI_ENDPOINT=your_endpoint## Local Development Setup2. Configure environment variables in `.env`:

## 📁 Project Structure

# AZURE_OPENAI_KEY=your_key

```

cimb-hackathon/# AZURE_OPENAI_DEPLOYMENT=gpt-5-mini```

├── .github/workflows/          # CI/CD pipeline

├── frontend/                   # React app

│   ├── src/

│   ├── build/                 # Production build# Run backend### PrerequisitesML_API_ENDPOINT=your_ml_api_endpoint

│   └── package.json

├── uploads/                    # File uploadspython app.py

├── app.py                      # Flask backend

├── requirements.txt            # Python deps```- Python 3.11+AZURE_OPENAI_ENDPOINT=your_azure_endpoint

├── runtime.txt                 # Python 3.11

└── README.md

```

Backend: `http://localhost:5000`- Node.js 18+AZURE_OPENAI_KEY=your_azure_key

## 🎯 Usage



1. Visit https://cimbxmicrosoft.azurewebsites.net

2. Upload Excel/CSV file### Frontend Setup- GitAZURE_OPENAI_DEPLOYMENT=your_deployment_name

3. View fraudulent transactions  

4. Click "Explain" for AI analysis

5. Hover over scores for risk levels

```bash```

## 🔌 API Endpoints

cd frontend

- `GET /api/status` - Check configuration

- `POST /api/upload` - Analyze transactionsnpm install### Backend Setup

- `POST /api/explain` - Get AI explanation

npm start

## ⚡ Performance

```3. Run the Flask server:

- Processes 50 transactions concurrently

- Async non-blocking operations

- 10s timeout with fallback

- Mock mode for testingFrontend: `http://localhost:3000`1. Clone the repository:```bash



## 🤝 Contributing



1. Fork the repo## ☁️ Azure Deployment```bashpython app.py

2. Create feature branch

3. Commit changes

4. Push and create PR

### Quick Setupgit clone https://github.com/yourusername/cimb-hackathon.git```

---



**Built with ❤️ for CIMB x Microsoft Hackathon**

1. **Create Azure Web App**cd cimb-hackathon

   - Runtime: Python 3.11 (Linux)

   - Region: Southeast Asia (Singapore)```Server runs on `http://localhost:5000`



2. **Enable Basic Auth**

   - Configuration → General settings

   - Turn ON both basic auth options2. Create and activate a virtual environment:### Frontend (React)



3. **Download Publish Profile**```bash

   - Overview → Get publish profile

python -m venv venv1. Install dependencies:

4. **Add GitHub Secret**

   - Repo → Settings → Secrets → Actions# Windows```bash

   - Name: `AZUREAPPSERVICE_PUBLISHPROFILE`

   - Value: Paste entire `.PublishSettings` XMLvenv\Scripts\activatecd frontend



5. **Add Environment Variables in Azure**# Linux/Macnpm install

   - Configuration → Application settings:

   ```source venv/bin/activate```

   AZURE_OPENAI_ENDPOINT=your_endpoint

   AZURE_OPENAI_KEY=your_key  ```

   AZURE_OPENAI_DEPLOYMENT=gpt-5-mini

   PORT=80002. Start the development server:

   SCM_DO_BUILD_DURING_DEPLOYMENT=true

   ```3. Install Python dependencies:```bash



6. **Push to Deploy**```bashnpm start

   ```bash

   git push origin mainpip install -r requirements.txt```

   ```

```

Monitor deployment: [GitHub Actions](https://github.com/terryong31/cimb-hackathon/actions)

Frontend runs on `http://localhost:3000`

## 📁 Project Structure

4. Create a `.env` file with your configuration:

```

cimb-hackathon/```env## Usage

├── .github/workflows/          # CI/CD pipeline

├── frontend/                   # React appML_API_ENDPOINT=your_ml_api_endpoint  # Optional

│   ├── src/

│   ├── build/                 # Production buildAZURE_OPENAI_ENDPOINT=your_azure_endpoint  # Optional1. Open the dashboard in your browser

│   └── package.json

├── uploads/                    # File uploadsAZURE_OPENAI_KEY=your_azure_key  # Optional2. Upload an Excel (.xlsx, .xls) or CSV (.csv) file with transaction data

├── app.py                      # Flask backend

├── requirements.txt            # Python depsAZURE_OPENAI_DEPLOYMENT=your_deployment_name  # Optional (default: gpt-4)3. View flagged fraudulent transactions

├── runtime.txt                 # Python 3.11

└── README.md```4. Click on any transaction to see AI-generated explanation

```

5. Hover over fraud scores to see risk levels

## 🎯 Usage

5. Run the Flask backend:

1. Visit https://cimbxmicrosoft.azurewebsites.net

2. Upload Excel/CSV file```bash## Mock Data Mode

3. View fraudulent transactions  

4. Click "Explain" for AI analysispython app.py

5. Hover over scores for risk levels

```If API credentials are not configured, the application automatically uses mock data for demonstration purposes.

## 🔌 API Endpoints



- `GET /api/status` - Check configuration

- `POST /api/upload` - Analyze transactionsBackend runs on `http://localhost:5000`## Tech Stack

- `POST /api/explain` - Get AI explanation



## ⚡ Performance

### Frontend Setup- **Backend**: Flask, Python, pandas, openpyxl

- Processes 50 transactions concurrently

- Async non-blocking operations- **Frontend**: React, Axios, CIMB theme

- 10s timeout with fallback

- Mock mode for testing1. Navigate to the frontend directory:- **ML Integration**: REST API



## 🤝 Contributing```bash- **AI**: Azure OpenAI



1. Fork the repocd frontend

2. Create feature branch

3. Commit changes```---

4. Push and create PR

Built for CIMB x Microsoft Hackathon

---

2. Install dependencies:

**Built with ❤️ for CIMB x Microsoft Hackathon**```bash

npm install
```

3. Start the React development server:
```bash
npm start
```

Frontend runs on `http://localhost:3000`

## Azure Web App Deployment

This project is configured for automated deployment to Azure Web App using GitHub Actions.

### Prerequisites
- Azure account with an active subscription
- Azure Web App created (Python 3.11, Linux)
- GitHub repository

### Deployment Steps

1. **Create Azure Web App**:
   - Go to Azure Portal
   - Create a new Web App
   - Runtime: Python 3.11 (Linux)
   - Operating System: Linux

2. **Configure GitHub Actions**:
   - In Azure Portal, go to your Web App
   - Navigate to "Deployment Center"
   - Select "GitHub" as the source
   - Authorize GitHub and select your repository
   - Azure will automatically create a publish profile

3. **Add GitHub Secrets**:
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add the following secret:
     - `AZURE_WEBAPP_PUBLISH_PROFILE`: Download from Azure Portal (Deployment Center → Manage publish profile)

4. **Update Workflow Configuration**:
   - Edit `.github/workflows/azure-webapp.yml`
   - Update `AZURE_WEBAPP_NAME` with your Azure Web App name

5. **Configure Environment Variables in Azure**:
   - In Azure Portal, go to your Web App → Configuration → Application settings
   - Add the following settings:
     ```
     ML_API_ENDPOINT=your_ml_api_endpoint
     AZURE_OPENAI_ENDPOINT=your_azure_endpoint
     AZURE_OPENAI_KEY=your_azure_key
     AZURE_OPENAI_DEPLOYMENT=your_deployment_name
     PORT=8000
     ```

6. **Deploy**:
   - Push to the `main` branch
   - GitHub Actions will automatically:
     - Build the React frontend
     - Install Python dependencies
     - Deploy to Azure Web App
   - Monitor the deployment in the "Actions" tab on GitHub

### Startup Command (Azure Configuration)

In Azure Portal → Configuration → General settings, set:
```bash
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
```

## Project Structure

```
cimb-hackathon/
├── .github/
│   └── workflows/
│       └── azure-webapp.yml    # CI/CD pipeline
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # CIMB styling
│   │   └── index.js            # React entry point
│   ├── package.json
│   └── build/                  # Production build (generated)
├── uploads/                    # File uploads directory
├── app.py                      # Flask backend
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version
├── sample_transactions.csv     # Sample data
├── .env                        # Environment variables (local)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Usage

1. Open the dashboard in your browser
2. Upload an Excel (.xlsx, .xls) or CSV (.csv) file with transaction data
3. View flagged fraudulent transactions
4. Click on any transaction to see AI-generated explanation
5. Hover over fraud scores to see risk levels

## Mock Data Mode

If API credentials are not configured, the application automatically uses mock data for demonstration purposes. This allows you to test the application without external dependencies.

## API Endpoints

- `GET /` - Serve React frontend
- `GET /api/status` - Check API status and configuration
- `POST /api/upload` - Upload and analyze transaction file
- `POST /api/explain` - Get AI explanation for flagged transaction

## Performance

- **Batch Processing**: Processes up to 50 transactions concurrently
- **Async Operations**: Non-blocking API calls for better performance
- **Timeout Handling**: 10-second timeout for ML API calls
- **Fallback Mode**: Automatic fallback to mock data on errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project was built for the CIMB x Microsoft Hackathon.

## Support

For issues or questions, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for CIMB x Microsoft Hackathon**

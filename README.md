# Anti-Scam Fraud Detection Dashboard

A minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning.

## Features

- 📊 Excel/CSV file upload for transaction analysis
- 🤖 ML-based fraud detection
- 🔍 AI-powered fraud explanations via Azure OpenAI
- 🎨 CIMB brand theme (minimalistic red & white)
- 🔄 Mock data fallback when API keys are not configured

## Required Transaction Fields

The Excel or CSV file must contain these columns:
- `TransactionAmount`
- `TransactionDuration`
- `LoginAttempts`
- `AccountBalance`
- `CustomerAge`

## Setup

### Backend (Flask)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```
ML_API_ENDPOINT=your_ml_api_endpoint
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_KEY=your_azure_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
```

3. Run the Flask server:
```bash
python app.py
```

Server runs on `http://localhost:5000`

### Frontend (React)

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

Frontend runs on `http://localhost:3000`

## Usage

1. Open the dashboard in your browser
2. Upload an Excel (.xlsx, .xls) or CSV (.csv) file with transaction data
3. View flagged fraudulent transactions
4. Click on any transaction to see AI-generated explanation
5. Hover over fraud scores to see risk levels

## Mock Data Mode

If API credentials are not configured, the application automatically uses mock data for demonstration purposes.

## Tech Stack

- **Backend**: Flask, Python, pandas, openpyxl
- **Frontend**: React, Axios, CIMB theme
- **ML Integration**: REST API
- **AI**: Azure OpenAI

---
Built for CIMB x Microsoft Hackathon

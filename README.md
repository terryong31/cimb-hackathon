# Anti-Scam Fraud Detection Dashboard# Anti-Scam Fraud Detection Dashboard



A minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning and AI-powered explanations.A minimalistic CIMB-themed web application for detecting fraudulent transactions using machine learning.



## Features## Features



- 📊 Excel/CSV file upload for transaction analysis- 📊 Excel/CSV file upload for transaction analysis

- 🤖 ML-based fraud detection- 🤖 ML-based fraud detection

- 🔍 AI-powered fraud explanations via Azure OpenAI- 🔍 AI-powered fraud explanations via Azure OpenAI

- 🎨 CIMB brand theme (minimalistic red & white)- 🎨 CIMB brand theme (minimalistic red & white)

- 🔄 Mock data fallback when API keys are not configured- 🔄 Mock data fallback when API keys are not configured

- ⚡ Async batch processing for high-volume transactions

## Required Transaction Fields

## Required Transaction Fields

The Excel or CSV file must contain these columns:

The Excel or CSV file must contain these columns:- `TransactionAmount`

- `TransactionAmount` - Transaction amount in currency- `TransactionDuration`

- `TransactionDuration` - Time taken for transaction (seconds)- `LoginAttempts`

- `LoginAttempts` - Number of login attempts- `AccountBalance`

- `AccountBalance` - Account balance- `CustomerAge`

- `CustomerAge` - Customer age

## Setup

## Technology Stack

### Backend (Flask)

- **Backend**: Flask (Python 3.11)

- **Frontend**: React 181. Install Python dependencies:

- **ML Integration**: REST API (optional)```bash

- **AI**: Azure OpenAI (optional)pip install -r requirements.txt

- **Deployment**: Azure Web App with GitHub Actions CI/CD```



## Local Development Setup2. Configure environment variables in `.env`:

```

### PrerequisitesML_API_ENDPOINT=your_ml_api_endpoint

- Python 3.11+AZURE_OPENAI_ENDPOINT=your_azure_endpoint

- Node.js 18+AZURE_OPENAI_KEY=your_azure_key

- GitAZURE_OPENAI_DEPLOYMENT=your_deployment_name

```

### Backend Setup

3. Run the Flask server:

1. Clone the repository:```bash

```bashpython app.py

git clone https://github.com/yourusername/cimb-hackathon.git```

cd cimb-hackathon

```Server runs on `http://localhost:5000`



2. Create and activate a virtual environment:### Frontend (React)

```bash

python -m venv venv1. Install dependencies:

# Windows```bash

venv\Scripts\activatecd frontend

# Linux/Macnpm install

source venv/bin/activate```

```

2. Start the development server:

3. Install Python dependencies:```bash

```bashnpm start

pip install -r requirements.txt```

```

Frontend runs on `http://localhost:3000`

4. Create a `.env` file with your configuration:

```env## Usage

ML_API_ENDPOINT=your_ml_api_endpoint  # Optional

AZURE_OPENAI_ENDPOINT=your_azure_endpoint  # Optional1. Open the dashboard in your browser

AZURE_OPENAI_KEY=your_azure_key  # Optional2. Upload an Excel (.xlsx, .xls) or CSV (.csv) file with transaction data

AZURE_OPENAI_DEPLOYMENT=your_deployment_name  # Optional (default: gpt-4)3. View flagged fraudulent transactions

```4. Click on any transaction to see AI-generated explanation

5. Hover over fraud scores to see risk levels

5. Run the Flask backend:

```bash## Mock Data Mode

python app.py

```If API credentials are not configured, the application automatically uses mock data for demonstration purposes.



Backend runs on `http://localhost:5000`## Tech Stack



### Frontend Setup- **Backend**: Flask, Python, pandas, openpyxl

- **Frontend**: React, Axios, CIMB theme

1. Navigate to the frontend directory:- **ML Integration**: REST API

```bash- **AI**: Azure OpenAI

cd frontend

```---

Built for CIMB x Microsoft Hackathon

2. Install dependencies:
```bash
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

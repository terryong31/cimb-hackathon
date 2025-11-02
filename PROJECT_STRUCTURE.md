# Project Structure

```
anti-scam/
│
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── .gitignore                 # Git ignore rules
│
├── uploads/                    # Directory for uploaded files
│   └── .gitkeep
│
├── generate_sample_data.py    # Script to create test data
├── sample_transactions.xlsx   # Generated test data file
│
├── setup.ps1                  # Automated setup script
├── start-backend.ps1          # Backend start script
├── start-frontend.ps1         # Frontend start script
│
├── README.md                  # Main documentation
├── QUICKSTART.md              # Quick setup guide
├── DESIGN.md                  # Design specifications
│
└── frontend/                  # React application
    ├── package.json           # Node.js dependencies
    ├── public/
    │   └── index.html         # HTML template
    └── src/
        ├── index.js           # React entry point
        ├── index.css          # Global styles
        ├── App.js             # Main application component
        └── App.css            # Application styles (CIMB theme)
```

## File Descriptions

### Backend Files

**app.py**
- Flask server with CORS enabled
- Three main endpoints: `/api/status`, `/api/upload`, `/api/explain`
- Mock data fallback when API keys not configured
- Excel file processing with pandas
- ML API and Azure OpenAI integration

**requirements.txt**
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin requests
- pandas 2.1.4 - Data processing
- openpyxl 3.1.2 - Excel file handling
- requests 2.31.0 - HTTP requests to ML API
- python-dotenv 1.0.0 - Environment variables
- openai 1.3.0 - Azure OpenAI client

**.env**
- ML_API_ENDPOINT - Your ML model API URL
- AZURE_OPENAI_ENDPOINT - Azure OpenAI endpoint
- AZURE_OPENAI_KEY - Azure OpenAI API key
- AZURE_OPENAI_DEPLOYMENT - Model deployment name

### Frontend Files

**frontend/src/App.js**
- Main React component
- File upload functionality
- Results display with summary cards
- Transaction table with click handlers
- Modal for detailed fraud analysis
- API integration using axios

**frontend/src/App.css**
- CIMB brand theme colors
- Responsive grid layouts
- Card components styling
- Table and modal styles
- Animations and transitions
- Mobile-responsive breakpoints

### Utility Files

**generate_sample_data.py**
- Creates sample Excel and CSV files with 20 transactions
- Includes all required fields
- Some transactions trigger fraud detection
- Additional columns to test parsing

**setup.ps1**
- Automated setup for Windows PowerShell
- Checks Python and Node.js installation
- Installs all dependencies
- Generates sample data
- Provides next steps

## API Endpoints

### GET /api/status
Returns system status and configuration mode.

**Response:**
```json
{
  "status": "online",
  "mock_mode": true,
  "ml_api_configured": false,
  "openai_configured": false
}
```

### POST /api/upload
Processes uploaded Excel or CSV file and returns fraud analysis.

**Request:** Multipart form data with file (accepts .xlsx, .xls, .csv)
**Response:**
```json
{
  "total_transactions": 20,
  "fraudulent_count": 8,
  "fraudulent_transactions": [...],
  "mock_mode": true
}
```

### POST /api/explain
Generates AI explanation for a fraudulent transaction.

**Request:**
```json
{
  "id": 0,
  "TransactionAmount": 7500,
  "TransactionDuration": 5,
  "LoginAttempts": 5,
  "AccountBalance": 8000,
  "CustomerAge": 22,
  "fraud_score": 0.85
}
```

**Response:**
```json
{
  "explanation": "Fraud analysis text...",
  "mock_mode": true
}
```

## Environment Variables

All API credentials are optional. If not provided, the system uses mock data.

```env
# ML Model API
ML_API_ENDPOINT=https://your-ml-api.com/predict

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

## Excel/CSV File Format

The uploaded Excel or CSV file must contain these columns:
- **TransactionAmount** (numeric) - Transaction amount in RM
- **TransactionDuration** (numeric) - Duration in seconds
- **LoginAttempts** (integer) - Number of login attempts
- **AccountBalance** (numeric) - Account balance in RM
- **CustomerAge** (integer) - Customer age in years

Additional columns are allowed and will be ignored.

**Supported formats:** .xlsx, .xls, .csv

## Technologies Used

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Lightweight web framework
- **pandas** - Data manipulation
- **openpyxl** - Excel file reading
- **Azure OpenAI** - AI explanations

### Frontend
- **React 18** - UI framework
- **JavaScript ES6+** - Programming language
- **CSS3** - Styling with custom properties
- **Axios** - HTTP client

## Development vs Production

### Development Mode (Current)
- Flask debug mode enabled
- React development server with hot reload
- Detailed error messages
- Mock data fallback

### Production Deployment
- Set Flask debug=False
- Build React app: `npm run build`
- Serve static files through Flask or nginx
- Configure proper API keys
- Use production WSGI server (gunicorn)
- Enable HTTPS
- Add rate limiting
- Implement authentication

## Mock Data Logic

When API keys are not configured, the system uses intelligent mock data:

**Fraud Detection:**
- Flags transactions with amount > RM 5,000
- Flags transactions with login attempts > 3
- Generates realistic fraud scores (0.65-0.95 for fraud, 0.05-0.45 for legitimate)

**Fraud Explanations:**
- Analyzes transaction fields
- Generates bullet-point risk factors
- Provides risk score interpretation
- Suggests next steps

This allows full demonstration without real API access!

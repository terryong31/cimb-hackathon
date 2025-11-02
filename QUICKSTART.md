# Quick Start Guide

## 🚀 Setup Instructions

### Step 1: Backend Setup

1. Open a terminal in the project root directory
2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. (Optional) Configure your API keys in `.env`:
   ```
   ML_API_ENDPOINT=your_ml_api_endpoint
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_KEY=your_azure_key
   AZURE_OPENAI_DEPLOYMENT=your_deployment_name
   ```
   
   **Note:** If you skip this step, the app will use mock data automatically!

4. Start the Flask server:
   ```powershell
   python app.py
   ```
   
   ✓ Backend running at http://localhost:5000

### Step 2: Frontend Setup

1. Open a new terminal and navigate to the frontend folder:
   ```powershell
   cd frontend
   ```

2. Install Node.js dependencies:
   ```powershell
   npm install
   ```

3. Start the React development server:
   ```powershell
   npm start
   ```
   
   ✓ Frontend running at http://localhost:3000
   ✓ Browser should open automatically

### Step 3: Generate Sample Data

1. In the project root, run:
   ```powershell
   python generate_sample_data.py
   ```
   
   This creates both `sample_transactions.xlsx` and `sample_transactions.csv` with 20 test transactions.

## 📊 Using the Dashboard

1. **Upload File**: Click "Choose Excel or CSV File" and select either:
   - `sample_transactions.xlsx` (Excel format)
   - `sample_transactions.csv` (CSV format)
2. **Analyze**: Click "Analyze Transactions" button
3. **View Results**: See summary cards and fraudulent transactions table
4. **Get Details**: Click any transaction row to see AI-powered fraud explanation

## 🎨 Features

- **CIMB Theme**: Minimalistic red & white design
- **Mock Mode**: Works without API keys using intelligent mock data
- **Risk Levels**: Color-coded fraud scores (Low/Medium/High/Critical)
- **AI Explanations**: Detailed analysis of each fraudulent transaction
- **Responsive**: Works on desktop and mobile devices

## 🔧 Troubleshooting

**Backend won't start?**
- Make sure Python 3.8+ is installed
- Check that all dependencies installed successfully
- Verify port 5000 is not in use

**Frontend won't start?**
- Ensure Node.js 14+ is installed
- Delete `node_modules` and run `npm install` again
- Check that port 3000 is not in use

**Can't upload Excel?**
- File must be .xlsx, .xls, or .csv format
- Required columns: TransactionAmount, TransactionDuration, LoginAttempts, AccountBalance, CustomerAge
- Use the sample files to test

## 📝 API Endpoints

- `GET /api/status` - Check system status and mode
- `POST /api/upload` - Upload and analyze Excel file
- `POST /api/explain` - Get fraud explanation for a transaction

---
Need help? Check README.md for more details!

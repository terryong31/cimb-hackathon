# Anti-Scam Dashboard Setup Script
$separator = "=" * 60
Write-Host $separator -ForegroundColor Cyan
Write-Host "  CIMB Anti-Scam Fraud Detection Dashboard Setup" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan
Write-Host ""

# Step 1: Backend Setup
Write-Host "[1/4] Setting up Python backend..." -ForegroundColor Yellow
Write-Host ""

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

Write-Host "Installing Python dependencies..." -ForegroundColor White
pip install -r requirements.txt
Write-Host ""

# Step 2: Frontend Setup
Write-Host "[2/4] Setting up React frontend..." -ForegroundColor Yellow
Write-Host ""

try {
    $nodeVersion = node --version 2>&1
    $npmVersion = npm --version 2>&1
    Write-Host "✓ Found Node: $nodeVersion" -ForegroundColor Green
    Write-Host "✓ Found npm: v$npmVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

Write-Host "Installing Node.js dependencies..." -ForegroundColor White
Push-Location frontend
npm install
Pop-Location
Write-Host ""

# Step 3: Generate Sample Data
Write-Host "[3/4] Generating sample transaction data..." -ForegroundColor Yellow
Write-Host ""

python generate_sample_data.py
Write-Host ""

# Step 4: Summary
Write-Host "[4/4] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host $separator -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure API keys in .env (optional - uses mock data by default)" -ForegroundColor White
Write-Host ""
Write-Host "2. Start the backend server:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. In a new terminal, start the frontend:" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Yellow
Write-Host "   npm start" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "5. Upload sample_transactions.xlsx to test the dashboard" -ForegroundColor White
Write-Host ""
Write-Host $separator -ForegroundColor Cyan
Write-Host "For Azure deployment, see AZURE_DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan
Write-Host ""

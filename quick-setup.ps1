# Quick Setup and Test Script
Write-Host "CIMB Anti-Scam Dashboard - Quick Setup" -ForegroundColor Cyan
Write-Host ""

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install Flask Flask-CORS pandas openpyxl requests python-dotenv openai

# Generate sample data
Write-Host ""
Write-Host "Generating sample data..." -ForegroundColor Yellow
python generate_sample_data.py

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run locally:" -ForegroundColor White
Write-Host "  Backend:  python app.py" -ForegroundColor Yellow
Write-Host "  Frontend: cd frontend && npm install && npm start" -ForegroundColor Yellow
Write-Host ""
Write-Host "To deploy to Azure:" -ForegroundColor White
Write-Host "  1. Run: .\build-for-azure.ps1" -ForegroundColor Yellow
Write-Host "  2. Follow AZURE_DEPLOYMENT.md" -ForegroundColor Yellow
Write-Host ""

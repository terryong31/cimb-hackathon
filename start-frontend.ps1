# Start Frontend Server
Write-Host "Starting CIMB Anti-Scam Frontend..." -ForegroundColor Cyan
Write-Host "Frontend will run at http://localhost:3000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location frontend
npm start

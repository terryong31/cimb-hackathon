# Build script for Azure deployment
$separator = "=" * 60
Write-Host $separator -ForegroundColor Cyan
Write-Host "  Building for Azure App Service" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan
Write-Host ""

# Step 1: Build React frontend
Write-Host "[1/2] Building React frontend for production..." -ForegroundColor Yellow
Write-Host ""

Push-Location frontend
Write-Host "Installing dependencies..." -ForegroundColor White
npm install

Write-Host "Creating production build..." -ForegroundColor White
npm run build

if (Test-Path "build") {
    Write-Host "✓ Frontend built successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Frontend build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host ""

# Step 2: Verify files
Write-Host "[2/2] Verifying deployment files..." -ForegroundColor Yellow
Write-Host ""

$requiredFiles = @(
    "app.py",
    "requirements-azure.txt",
    "startup.sh",
    "runtime.txt",
    ".deployment",
    "frontend/build/index.html"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ $file (missing)" -ForegroundColor Red
        $allFilesExist = $false
    }
}
Write-Host ""

if ($allFilesExist) {
    Write-Host $separator -ForegroundColor Cyan
    Write-Host "  Build Complete!" -ForegroundColor Green
    Write-Host $separator -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ready for Azure deployment. See AZURE_DEPLOYMENT.md for instructions." -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "ERROR: Some required files are missing" -ForegroundColor Red
    exit 1
}

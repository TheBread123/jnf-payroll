# Development setup script for JNF Payroll System (PowerShell)

Write-Host "Setting up JNF Payroll System for local development..." -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Activating..." -ForegroundColor Yellow
} else {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install

# Build React app for production
Write-Host "Building React app..." -ForegroundColor Yellow
npm run build
Set-Location ..

# Copy React build files to Flask static and templates folders
Write-Host "Setting up build files for Flask..." -ForegroundColor Yellow
if (Test-Path "static") {
    Remove-Item -Recurse -Force "static"
}
if (Test-Path "templates") {
    Remove-Item -Recurse -Force "templates"
}

# Create directories
New-Item -ItemType Directory -Force -Path "static" | Out-Null
New-Item -ItemType Directory -Force -Path "templates" | Out-Null

# Copy build files with proper structure for Flask
# Copy all files from build root (excluding the nested static folder)
Get-ChildItem "frontend\build" -Exclude "static" | Copy-Item -Destination "static" -Recurse -Force

# Copy the contents of the nested static folder to Flask's static root
if (Test-Path "frontend\build\static") {
    Get-ChildItem "frontend\build\static" | Copy-Item -Destination "static" -Recurse -Force
}

# Copy index.html to templates
Copy-Item "frontend\build\index.html" "templates\"

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Development options:" -ForegroundColor Cyan
Write-Host "1. Development mode (recommended):" -ForegroundColor Yellow
Write-Host "   - Activate virtual environment: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   - Start Flask backend: python app.py" -ForegroundColor White
Write-Host "   - Start React frontend: cd frontend && npm start" -ForegroundColor White
Write-Host "   - Frontend: http://localhost:3000 (hot reload)" -ForegroundColor White
Write-Host "   - Backend API: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "2. Production mode (using build files):" -ForegroundColor Yellow
Write-Host "   - Activate virtual environment: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   - Start Flask only: python app.py" -ForegroundColor White
Write-Host "   - Full app: http://localhost:5000 (production build)" -ForegroundColor White
Write-Host ""
Write-Host "Demo accounts:" -ForegroundColor Magenta
Write-Host "- Username: admin, Password: password123" -ForegroundColor White
Write-Host "- Username: demo, Password: demo123" -ForegroundColor White
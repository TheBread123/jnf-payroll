#!/bin/bash

# Development setup script for JNF Payroll System

echo "Setting up JNF Payroll System for local development..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Activating..."
else
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd frontend
npm install

# Build React app for production
echo "Building React app..."
npm run build
cd ..

# Copy React build files to Flask static and templates folders
echo "Setting up build files for Flask..."
rm -rf static templates 2>/dev/null || true

# Create directories
mkdir -p static templates

# Copy build files with proper structure for Flask
# Copy all files from build root (excluding the nested static folder)
find frontend/build -maxdepth 1 -not -name "static" -not -name "build" -exec cp -r {} static/ \; 2>/dev/null || true

# Copy the contents of the nested static folder to Flask's static root
if [ -d "frontend/build/static" ]; then
    cp -r frontend/build/static/* static/ 2>/dev/null || true
fi

# Copy index.html to templates
cp frontend/build/index.html templates/

echo "Setup complete!"
echo ""
echo "Development options:"
echo "1. Development mode (recommended):"
echo "   - Activate virtual environment: source venv/bin/activate"
echo "   - Start Flask backend: python app.py"
echo "   - Start React frontend: cd frontend && npm start"
echo "   - Frontend: http://localhost:3000 (hot reload)"
echo "   - Backend API: http://localhost:5000"
echo ""
echo "2. Production mode (using build files):"
echo "   - Activate virtual environment: source venv/bin/activate"
echo "   - Start Flask only: python app.py"
echo "   - Full app: http://localhost:5000 (production build)"
echo ""
echo "Demo accounts:"
echo "- Username: admin, Password: password123"
echo "- Username: demo, Password: demo123"

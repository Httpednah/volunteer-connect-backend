#!/bin/bash
# Build script for Render deployment
# This ensures gunicorn is properly installed and available

echo "========================================="
echo "Starting Render Build Process"
echo "========================================="

# Upgrade pip to latest version
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies without cache
echo "Installing dependencies from requirements.txt..."
pip install --no-cache-dir -r requirements.txt

# Verify gunicorn is installed
echo "Verifying gunicorn installation..."
python -c "import gunicorn; print(f'Gunicorn version: {gunicorn.__version__}')"

# Check that gunicorn can be found
echo "Checking gunicorn availability..."
which gunicorn || python -c "import gunicorn.app.wsgiapp; print('Gunicorn available via Python module')"

echo "========================================="
echo "Build completed successfully!"
echo "========================================="


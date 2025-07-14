#!/bin/bash

echo "Setting up NER Project environment..."

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment (for Unix/Mac)
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
  echo "Activating virtual environment (Unix/Mac)..."
  source venv/bin/activate
# Activate virtual environment (for Windows)
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  echo "Activating virtual environment (Windows)..."
  source venv/Scripts/activate
fi

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Run the application
echo "Starting Streamlit application..."
streamlit run app.py

# Note: To deactivate the virtual environment when done
# Just run: deactivate

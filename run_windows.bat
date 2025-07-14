@echo off
echo Setting up NER Project environment...

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages...
pip install -r requirements.txt

echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo Starting Streamlit application...
streamlit run app.py

echo.
echo When finished, type 'deactivate' to exit the virtual environment

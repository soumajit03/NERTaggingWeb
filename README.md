# NER Project - Sentence-wise Dataset Tagging Tool

This is a Named Entity Recognition (NER) project that provides a user interface for tagging sentences.

## Setup and Run Instructions

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Option 1: Running on Windows
1. Open Command Prompt
2. Navigate to the project directory:
   ```
   cd c:\Users\souma\Downloads\NERproject
   ```
3. Run the batch file:
   ```
   run_windows.bat
   ```

### Option 2: Running on Unix/Mac/Linux
1. Open Terminal
2. Navigate to the project directory:
   ```
   cd path/to/NERproject
   ```
3. Make the script executable:
   ```
   chmod +x setup_and_run.sh
   ```
4. Run the script:
   ```
   ./setup_and_run.sh
   ```

### Option 3: Manual Setup
1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Mac: `source venv/bin/activate`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Download spaCy model:
   ```
   python -m spacy download en_core_web_sm
   ```
5. Start the application:
   ```
   streamlit run app.py
   ```

## Usage
1. Upload a text file in the web interface
2. Tag entities in each sentence
3. Save tags for each sentence
4. Export all annotations to JSON when finished

## Deactivating the Environment
When you're done, type `deactivate` in your terminal to exit the virtual environment.

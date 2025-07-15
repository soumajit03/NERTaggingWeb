
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python -m spacy download en_core_web_sm

streamlit run app.py

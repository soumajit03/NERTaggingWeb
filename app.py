import json
import streamlit as st
import re
import os

# Configure Streamlit for deployment
st.set_page_config(
    layout="wide",
    page_title="NER Tagging Tool",
    page_icon="📘"
)

# Add deployment-specific configurations
if 'RENDER' in os.environ:
    st.markdown("""
    <style>
    .stApp > header {
        background-color: transparent;
    }
    .stApp {
        margin-top: -80px;
    }
    </style>
    """, unsafe_allow_html=True)

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    st.error("📚 spaCy is required but not installed. Please run: pip install spacy")
    st.stop()

from spacy import displacy

st.set_page_config(layout="wide")
st.title("📘 Sentence-wise Dataset Tagging Tool (Persistent + Final Export)")

TAGS = ["O", "B-MYTH", "I-MYTH", "B-LOC", "I-LOC", "B-GEO", "I-GEO", "B-ORG", "I-ORG"]

# Load spaCy model with error handling
@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error("🚨 **spaCy model 'en_core_web_sm' not found!**")
        st.error("Please install it by running:")
        st.code("python -m spacy download en_core_web_sm")
        if 'RENDER' in os.environ:
            st.error("If you're seeing this on Render, the build command may have failed.")
        st.stop()
        return None

nlp = load_nlp()

def annotate_text(text):
    if nlp:
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents]
    else:
        # Fallback: simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

def tokenize_sentence(sentence):
    if nlp:
        return [token for token in nlp(sentence)]
    else:
        # Fallback: simple word tokenization
        words = re.findall(r'\b\w+\b', sentence)
        # Create token-like objects
        class SimpleToken:
            def __init__(self, text, idx):
                self.text = text
                self.idx = idx
        
        tokens = []
        idx = 0
        for word in words:
            start_idx = sentence.find(word, idx)
            tokens.append(SimpleToken(word, start_idx))
            idx = start_idx + len(word)
        return tokens

# Session-wide store for all sentence annotations
if "annotations" not in st.session_state:
    st.session_state.annotations = {}

if "sentences" not in st.session_state:
    st.session_state.sentences = []

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    sentences = annotate_text(text)
    
    # Extract base filename without extension
    base_filename = os.path.splitext(uploaded_file.name)[0]
    
    # Clear previous annotations when new file is uploaded
    if "current_file_name" not in st.session_state or st.session_state.current_file_name != uploaded_file.name:
        st.session_state.annotations = {}
        st.session_state.current_file_name = uploaded_file.name
        st.session_state.base_filename = base_filename
    
    st.session_state.sentences = sentences  # Store sentences in session state
    total_sentences = len(sentences)

    # Navigation controls
    sentence_index = st.number_input("Sentence #", min_value=0, max_value=total_sentences-1, value=0, step=1)
    # Add sentence progress display
    st.text(f"{sentence_index}/{total_sentences-1}")
    current_sentence = sentences[sentence_index]
    tokens = tokenize_sentence(current_sentence)

    # Prepare previously selected tags or default "O"
    prev_annotations = st.session_state.annotations.get(sentence_index, [])
    default_tags = [ann[4] for ann in prev_annotations] if prev_annotations else ["O"] * len(tokens)
    
    # Ensure default_tags matches the number of tokens
    if len(default_tags) != len(tokens):
        default_tags = ["O"] * len(tokens)

    st.markdown("---")
    st.markdown(f"### Sentence: {current_sentence}")

    tagged = []
    st.markdown("### Tagging")
    for i, token in enumerate(tokens):
        cols = st.columns([2, 3])
        with cols[0]:
            st.markdown(f"<div style='padding: 8px 0;'>{token.text}</div>", unsafe_allow_html=True)
        with cols[1]:
            # Safe access to default_tags with bounds checking
            default_tag = default_tags[i] if i < len(default_tags) else "O"
            tag = st.selectbox(
                "", TAGS, key=f"{sentence_index}-{i}", index=TAGS.index(default_tag), label_visibility="collapsed"
            )
            tagged.append([
                token.idx,
                token.idx + len(token.text),
                token.text,
                i,
                tag
            ])

    if st.button("💾 Save Sentence Tags"):
        st.session_state.annotations[sentence_index] = tagged
        st.success("Tags saved for this sentence!")

    st.markdown("---")
    if st.button("📦 Export All Annotations to JSON"):
        final_json = {"annotations": []}
        for sent_idx, entities in sorted(st.session_state.annotations.items()):
            # Use sentences from session state and add bounds checking
            if sent_idx < len(st.session_state.sentences):
                sentence = st.session_state.sentences[sent_idx]
                final_json["annotations"].append([sentence, {"entities": entities}])
            # Remove the warning message since we'll silently skip invalid indices

        export_path = f"{st.session_state.base_filename}.json"
        with open(export_path, "w") as f:
            json.dump(final_json, f, indent=2)

        with open(export_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Full JSON",
                data=f,
                file_name=export_path,
                mime="application/json"
            )

# Add export functionality even when no file is currently uploaded
elif st.session_state.annotations:
    st.markdown("---")
    st.markdown("### Previous Annotations Available")
    st.info(f"You have {len(st.session_state.annotations)} annotated sentences stored.")
    
    if st.button("📦 Export All Annotations to JSON"):
        final_json = {"annotations": []}
        for sent_idx, entities in sorted(st.session_state.annotations.items()):
            # Use sentences from session state and add bounds checking
            if sent_idx < len(st.session_state.sentences):
                sentence = st.session_state.sentences[sent_idx]
                final_json["annotations"].append([sentence, {"entities": entities}])
            # Remove the warning message since we'll silently skip invalid indices

        # Use stored base filename or fallback to default
        filename = st.session_state.get('base_filename', 'all_tagged_sentences')
        export_path = f"{filename}.json"
        with open(export_path, "w") as f:
            json.dump(final_json, f, indent=2)

        with open(export_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Full JSON",
                data=f,
                file_name=export_path,
                mime="application/json"
            )

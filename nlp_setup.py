import nltk
from nltk.corpus import stopwords
import string
import re
import requests
import logging
from logger import logger

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

nltk.data.path.append("C:/Users/ADMIN/nltk_data")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def normalize(text):
    text = text.lower()
    text = re.sub(r'\b(\d+)\s*&\s*(\d+)\b', r'\1 and \2', text)

    text = text.replace('&', 'and')
    text = text.replace('&amp', 'and')
    text = text.replace('/', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('-', ' ')

    # Replace known phrases with their normalized forms
    replacements = {
        "plant load factor": "plf",
        "plant availability factor": "paf",
        "auxiliary consumption": "aux consumption",
        "maximum power": "max power",
        "minimum power": "min power",
        "iex price": "iex price",
        "iex cost": "iex price",
        "iex rate": "iex price",
        "banked unit": "banking unit",
        "gen energy": "generated energy",
        "procurement price": "last_price",
        "procurement price for": "last_price",
        "energy generated": "generated energy",
        "energy generation": "generated energy",
        "cost generated": "generated cost",
    }
    for k, v in sorted(replacements.items(), key=lambda x: -len(x[0])):  # longest first
        text = text.replace(k, v)

    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip(string.punctuation)
    return text


# ---------------------------
# NLP Helpers
# ---------------------------
def preprocess(text):
    try:
        # Clean and normalize the text
        # Handle numeric "and" patterns like "3 and 4" → "3 and 4" (or optionally → "3 & 4")
        text = normalize(text)
        print("DEBUG cleaned text:", text)

        # Tokenize
        tokens = word_tokenize(text)
        print("DEBUG: Tokens =", tokens)
        cleaned = " ".join(tokens)

        # Filtered and lemmatized tokens
        processed_tokens = [
            lemmatizer.lemmatize(tok)
            for tok in tokens
            if tok not in stop_words and len(tok) > 1 and not tok.isnumeric()
        ]

        # Multi-word and single-word plant-related keywords
        plant_keywords = [
            "plf", "paf", "variable cost","aux consumption", "max power", "min power",
            "rated capacity", "type", "plant", "plant details", "auxiliary consumption", "technical minimum", "maximum power", "minimum power",
            "plant load factor", "plant availability factor", "aux usage", "auxiliary usage", "var cost"
        ]


        procurement_keywords =["banking unit", "banking contribution","banking","banked unit", "generated energy",
                               "procurement price", "generation energy", "energy generated", "energy generation", "demand banked",
                               "energy", "produce", "banked", "energy banked", "generated cost", "generation cost", "cost generated",
                               "cost generation"

        ]

        #combine all
        all_keywords = plant_keywords + procurement_keywords

        matched_keywords = set()
        for keyword in all_keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text):
                matched_keywords.add(keyword)

        return processed_tokens, matched_keywords

    except Exception as e:
        logger.error(f"Preprocessing error: {e}")
        return [], set()

__all__ = ['normalize', 'preprocess']

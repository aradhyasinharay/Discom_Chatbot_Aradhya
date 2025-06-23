from normalizer import normalize
from nlp_setup import lemmatizer, stop_words
from nltk.tokenize import word_tokenize
from logger import logger
import re


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

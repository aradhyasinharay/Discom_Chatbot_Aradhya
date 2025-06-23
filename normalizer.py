import re
import string

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

from normalizer import normalize

def fuzzy_match(a, b):
    return normalize(a) == normalize(b) or normalize(a) in normalize(b) or normalize(b) in normalize(a)

import re

def clean_text(text):

    # Fix spaced letters like: S U M M A R Y
    text = re.sub(r'(?<=\b\w) (?=\w\b)', '', text)

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
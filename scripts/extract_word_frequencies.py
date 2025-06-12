import os
import re
import string
import pandas as pd
from collections import Counter

# --- CLEANING FUNCTION (Enriched) ---

def clean_text_advanced(text):
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Remove emails
    text = re.sub(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b', '', text)

    # Remove Ethereum addresses (0x…)
    text = re.sub(r'0x[a-fA-F0-9]{40,}', '', text)

    # Remove punctuation and digits
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\\d+', '', text)

    # Remove extra spaces
    text = re.sub(r'\\s+', ' ', text).strip()

    return text

# --- MINIMAL SYNTAXIC STOPWORDS (strict STS filtering) ---

STOPWORDS_MINIMAL = set([
    'the', 'and', 'of', 'to', 'in', 'for', 'is', 'on', 'that', 'with', 'as',
    'by', 'it', 'are', 'at', 'from', 'an', 'be', 'or', 'we', 'can', 'not',
    'have', 'has', 'our', 'also', 'more', 'which', 'their', 'will', 'all',
    'but', 'was', 'they', 'these', 'may', 'you', 'been', 'using', 'its',
    'if', 'do', 'does', 'did', 'because', 'however', 'therefore', 'thus',
    'when', 'then', 'now', 'always', 'never', 'this', 'a'
])

# --- TOKENIZER ---

def tokenize_strict(text, stopwords=STOPWORDS_MINIMAL):
    tokens = text.split()
    clean_tokens = [word for word in tokens if word not in stopwords and len(word) > 2]
    return clean_tokens

# --- MAIN PIPELINE ---

DATA_DIR = './data/corpus_txt'
OUTPUT_DIR = './outputs/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_corpus(data_dir):
    all_tokens = []

    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                cleaned = clean_text_advanced(content)
                tokens = tokenize_strict(cleaned)
                all_tokens.extend(tokens)

    return all_tokens

tokens = process_corpus(DATA_DIR)

counter = Counter(tokens)
total_tokens = sum(counter.values())

data = [
    {
        'word': word,
        'frequency': freq,
        'relative_per_1000': freq / total_tokens * 1000
    }
    for word, freq in counter.most_common()
]

df = pd.DataFrame(data)
df.to_csv(os.path.join(OUTPUT_DIR, 'word_frequencies.csv'), index=False)

print("Word frequencies extracted and saved successfully.")

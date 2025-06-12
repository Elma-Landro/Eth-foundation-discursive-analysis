import os
import re
import string
import pandas as pd
from collections import defaultdict
import itertools

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
    'by', 'it', 'are', 'at', 'from', 'an', 'be', 'or', 'we', 'can',
    'have', 'has', 'our', 'also', 'which', 'their', 'will', 'all',
    'but', 'was', 'they', 'these', 'may', 'you', 'been', 'its',
    'if', 'do', 'does', 'did', 'because', 'however', 'therefore', 'thus',
    'when', 'then', 'now', 'always', 'never', 'this', 'a',
    'very', 'most', 'some', 'many', 'such', 'would', 'could', 'should'
])

# --- TOKENIZER ---

def tokenize_strict(text, stopwords=STOPWORDS_MINIMAL):
    tokens = text.split()
    clean_tokens = [word for word in tokens if word not in stopwords and len(word) > 2]
    return clean_tokens

# --- CO-OCCURRENCE EXTRACTION ---

DATA_DIR = './data/corpus_txt'
OUTPUT_DIR = './outputs/'
WINDOW_SIZE = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_corpus(data_dir, window_size):
    cooccurrence_counts = defaultdict(int)

    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                cleaned = clean_text_advanced(content)
                tokens = tokenize_strict(cleaned)

                for i in range(len(tokens)):
                    window = tokens[i:i+window_size]
                    for pair in itertools.combinations(window, 2):
                        if pair[0] != pair[1]:
                            pair_sorted = tuple(sorted(pair))
                            cooccurrence_counts[pair_sorted] += 1

    return cooccurrence_counts

cooccurrences = process_corpus(DATA_DIR, WINDOW_SIZE)

# Convert to dataframe
data = [{'word1': pair[0], 'word2': pair[1], 'count': count} for pair, count in cooccurrences.items()]
df = pd.DataFrame(data)
df.sort_values(by='count', ascending=False, inplace=True)

df.to_csv(os.path.join(OUTPUT_DIR, 'cooccurrence_pairs.csv'), index=False)

print("Co-occurrence extraction completed and saved successfully.")


import os
import re
import string
import pandas as pd
from collections import Counter

# -----------------
# PARAMÈTRES
# -----------------

# Dossier contenant les fichiers texte extraits de la Fondation Ethereum
DATA_DIR = './data'

# Liste simple de stopwords (à étendre selon les besoins)
STOPWORDS = set([
    'the', 'and', 'of', 'to', 'in', 'for', 'is', 'on', 'that', 'with', 'as',
    'by', 'this', 'it', 'are', 'at', 'from', 'an', 'be', 'or', 'we', 'can',
    'not', 'have', 'has', 'our', 'also', 'more', 'which', 'their', 'will',
    'all', 'but', 'was', 'they', 'these', 'may', 'you', 'been', 'using', 'its'
])

# -----------------
# FONCTIONS
# -----------------

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    text = text.strip()
    return text

def tokenize(text):
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS and len(word) > 2]
    return tokens

def process_corpus(data_dir):
    all_tokens = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                clean = clean_text(content)
                tokens = tokenize(clean)
                all_tokens.extend(tokens)
    return all_tokens

# -----------------
# EXÉCUTION
# -----------------

if __name__ == '__main__':
    tokens = process_corpus(DATA_DIR)
    counter = Counter(tokens)
    total_tokens = sum(counter.values())

    data = []
    for word, freq in counter.most_common():
        rel_freq = freq / total_tokens * 1000  # fréquence pour 1000 mots
        data.append({'word': word, 'frequency': freq, 'relative_per_1000': rel_freq})

    os.makedirs('./outputs', exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv('./outputs/word_frequencies.csv', index=False)
    print("Extraction terminée : voir outputs/word_frequencies.csv")

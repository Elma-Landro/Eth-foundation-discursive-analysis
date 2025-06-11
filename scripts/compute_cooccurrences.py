
import os
import re
import string
import pandas as pd
from collections import Counter, defaultdict
from itertools import combinations

# Paramètres
DATA_DIR = './data'
WINDOW_SIZE = 5  # fenêtre glissante de cooccurrence

STOPWORDS = set([
    'the', 'and', 'of', 'to', 'in', 'for', 'is', 'on', 'that', 'with', 'as',
    'by', 'this', 'it', 'are', 'at', 'from', 'an', 'be', 'or', 'we', 'can',
    'not', 'have', 'has', 'our', 'also', 'more', 'which', 'their', 'will',
    'all', 'but', 'was', 'they', 'these', 'may', 'you', 'been', 'using', 'its'
])

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
    cooccurrence = defaultdict(int)
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                clean = clean_text(content)
                tokens = tokenize(clean)
                for i in range(len(tokens) - WINDOW_SIZE + 1):
                    window = tokens[i:i+WINDOW_SIZE]
                    for w1, w2 in combinations(set(window), 2):
                        pair = tuple(sorted((w1, w2)))
                        cooccurrence[pair] += 1
    return cooccurrence

if __name__ == '__main__':
    cooccurrence = process_corpus(DATA_DIR)

    data = []
    for pair, count in sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True):
        data.append({'word1': pair[0], 'word2': pair[1], 'count': count})

    os.makedirs('./outputs', exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv('./outputs/cooccurrence_pairs.csv', index=False)
    print("Cooccurrence terminée : voir outputs/cooccurrence_pairs.csv")

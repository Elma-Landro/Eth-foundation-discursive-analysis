
"""
Calcul des cooccurrences lexicales - Version 1.1
Ethereum Foundation Discursive Analysis

Corrections v1.1 :
- Correction regex email (échappement \b)
- Préservation des termes techniques crypto
- Intégration configuration centralisée
- Optimisation de la fenêtre glissante
"""

import os
import re
import string
import pandas as pd
from collections import defaultdict
import itertools
import sys
sys.path.append('.')
from config import *

def clean_text_advanced(text):
    """
    Nettoyage textuel avancé - Version harmonisée avec extract_word_frequencies.py
    """
    text = text.lower()

    # Suppression des URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # CORRECTION CRITIQUE v1.1 : Regex email corrigée
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    # Suppression des adresses Ethereum
    text = re.sub(r'0x[a-fA-F0-9]{40,}', '', text)

    # Suppression de la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # CORRECTION CRITIQUE v1.1 : Préservation des termes techniques
    if PRESERVE_CRYPTO_TERMS:
        temp_replacements = {}
        for i, term in enumerate(CRYPTO_TECHNICAL_TERMS):
            placeholder = f"CRYPTOTERM{i}PLACEHOLDER"
            if term in text:
                text = text.replace(term, placeholder)
                temp_replacements[placeholder] = term
    
    # Suppression des chiffres isolés
    text = re.sub(r'\b\d+\b', '', text)
    
    # Restauration des termes techniques
    if PRESERVE_CRYPTO_TERMS:
        for placeholder, original_term in temp_replacements.items():
            text = text.replace(placeholder, original_term)

    # Nettoyage des espaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def tokenize_strict(text):
    """
    Tokenisation stricte harmonisée
    """
    words = text.split()
    return [
        word for word in words 
        if len(word) > MIN_TOKEN_LENGTH and word not in STOPWORDS_MINIMAL
    ]

def compute_cooccurrences_sliding_window(words, window_size=COOCCURRENCE_WINDOW_SIZE):
    """
    Calcul des cooccurrences par fenêtre glissante
    
    Méthodologie :
    - Fenêtre glissante de taille configurable
    - Génération de toutes les paires dans chaque fenêtre
    - Tri alphabétique pour éviter les doublons (A,B) vs (B,A)
    
    Args:
        words (list): Liste des tokens
        window_size (int): Taille de la fenêtre glissante
        
    Returns:
        defaultdict: Dictionnaire des cooccurrences avec leurs fréquences
    """
    cooccurrences = defaultdict(int)
    
    # Parcours par fenêtre glissante
    for i in range(len(words) - window_size + 1):
        window = words[i:i + window_size]
        
        # Génération de toutes les paires dans la fenêtre
        for word1, word2 in itertools.combinations(window, 2):
            # Tri alphabétique pour normalisation
            pair = tuple(sorted([word1, word2]))
            cooccurrences[pair] += 1
    
    return cooccurrences

def main():
    """
    Pipeline principal de calcul des cooccurrences
    """
    print("=== Calcul des cooccurrences lexicales v1.1 ===")
    print(f"Fenêtre glissante: {COOCCURRENCE_WINDOW_SIZE} mots")
    print(f"Seuil minimal: {COOCCURRENCE_MIN_FREQUENCY} occurrences")
    
    if not os.path.exists(DATA_DIR):
        print(f"Erreur: Le dossier {DATA_DIR} n'existe pas.")
        return
    
    # Collection de tous les mots par document
    all_cooccurrences = defaultdict(int)
    file_count = 0
    
    # Traitement document par document
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(DATA_DIR, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    
                    # Pipeline de traitement
                    cleaned_text = clean_text_advanced(text)
                    words = tokenize_strict(cleaned_text)
                    
                    # Calcul des cooccurrences pour ce document
                    doc_cooccurrences = compute_cooccurrences_sliding_window(words)
                    
                    # Agrégation au niveau du corpus
                    for pair, count in doc_cooccurrences.items():
                        all_cooccurrences[pair] += count
                    
                    file_count += 1
                    
                    if VERBOSE_MODE and file_count % 50 == 0:
                        print(f"Traité {file_count} fichiers...")
                        
            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {e}")
    
    print(f"Traitement terminé: {file_count} fichiers")
    
    # Filtrage par seuil minimal
    filtered_cooccurrences = {
        pair: count for pair, count in all_cooccurrences.items() 
        if count >= COOCCURRENCE_MIN_FREQUENCY
    }
    
    print(f"Cooccurrences avant filtrage: {len(all_cooccurrences)}")
    print(f"Cooccurrences après filtrage (≥{COOCCURRENCE_MIN_FREQUENCY}): {len(filtered_cooccurrences)}")
    
    # Préparation des données pour export
    cooccurrence_data = []
    for (word1, word2), count in filtered_cooccurrences.items():
        cooccurrence_data.append({
            'word1': word1,
            'word2': word2,
            'cooccurrence_count': count
        })
    
    # Tri par fréquence décroissante
    cooccurrence_data.sort(key=lambda x: x['cooccurrence_count'], reverse=True)
    
    # Export CSV
    df = pd.DataFrame(cooccurrence_data)
    output_path = os.path.join(CSV_OUTPUT_DIR, 'cooccurrence_pairs.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    print(f"\nTop 10 des cooccurrences les plus fréquentes:")
    for item in cooccurrence_data[:10]:
        print(f"  ({item['word1']}, {item['word2']}): {item['cooccurrence_count']}")

if __name__ == "__main__":
    main()

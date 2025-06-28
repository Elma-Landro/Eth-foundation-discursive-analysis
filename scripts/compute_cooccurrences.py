
"""
Calcul des cooccurrences lexicales - Version 1.8 EXPRESSIONS COMPOSÉES
Ethereum Foundation Discursive Analysis

Corrections v1.8 :
- Synchronisation avec extract_word_frequencies v1.8
- Préservation expressions composées dans cooccurrences
- Correction problème majuscules/fragmentation
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

# Expressions composées à préserver (synchronisé avec extract_word_frequencies)
COMPOUND_EXPRESSIONS = {
    'zero knowledge': 'zero_knowledge',
    'ethereum foundation': 'ethereum_foundation', 
    'proof of stake': 'proof_of_stake',
    'proof of work': 'proof_of_work',
    'smart contract': 'smart_contract',
    'smart contracts': 'smart_contracts',
    'layer 2': 'layer_2',
    'layer two': 'layer_2',
    'web 3': 'web_3',
    'web3': 'web_3',
    'hard fork': 'hard_fork',
    'soft fork': 'soft_fork',
    'beacon chain': 'beacon_chain',
    'execution layer': 'execution_layer',
    'consensus layer': 'consensus_layer',
    'merkle tree': 'merkle_tree',
    'virtual machine': 'virtual_machine',
    'gas fee': 'gas_fee',
    'gas fees': 'gas_fees',
    'transaction fee': 'transaction_fee',
    'transaction fees': 'transaction_fees'
}

def preserve_compound_expressions(text):
    """
    Préserve les expressions composées importantes AVANT minuscules
    
    CORRECTION v1.9 synchronisée avec extract_word_frequencies
    """
    # Préservation expressions composées sur texte ORIGINAL
    text_preserved = text
    
    # Remplacement insensible à la casse
    for compound, replacement in COMPOUND_EXPRESSIONS.items():
        import re
        pattern = re.compile(re.escape(compound), re.IGNORECASE)
        text_preserved = pattern.sub(replacement, text_preserved)
    
    # Conversion minuscules APRÈS préservation
    text_lower = text_preserved.lower()
    
    return text_lower

def clean_text_v20_cooccurrence(text):
    """
    Nettoyage harmonisé avec extract_word_frequencies v2.0 - FRAGMENTATION CORRIGÉE
    """
    if not text:
        return ""
    
    # CORRECTION v2.0 : Préservation expressions composées EN PREMIER
    text_preserved = preserve_compound_expressions(text)
    
    # Suppression technique DOUCE (espaces, pas troncature)
    text_clean = re.sub(r'https?://[^\s]+', ' ', text_preserved)
    text_clean = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', ' ', text_clean)
    text_clean = re.sub(r'0x[a-fA-F0-9]{40,}', ' ', text_clean)
    
    # Normalisation espaces
    text_final = re.sub(r'\s+', ' ', text_clean).strip()
    
    return text_final

def tokenize_v18_cooccurrence(text):
    """
    Tokenisation harmonisée v1.8
    """
    if not text:
        return []
    
    # Suppression ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Suppression chiffres isolés
    text = re.sub(r'\b\d+\b', ' ', text)
    
    # Tokenisation
    words = text.split()
    
    # Filtrage
    filtered_words = [
        word for word in words 
        if len(word) > MIN_TOKEN_LENGTH and word not in STOPWORDS_MINIMAL
    ]
    
    return filtered_words

def compute_cooccurrences_sliding_window(words, window_size=COOCCURRENCE_WINDOW_SIZE):
    """
    Calcul des cooccurrences par fenêtre glissante
    """
    cooccurrences = defaultdict(int)
    
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
    Pipeline principal de calcul des cooccurrences v1.8 - CORRECTION MAJUSCULES
    """
    print("=== Calcul des cooccurrences lexicales v1.9 CORRECTION DÉFINITIVE MAJUSCULES ===")
    print(f"Fenêtre glissante: {COOCCURRENCE_WINDOW_SIZE} mots")
    print(f"Seuil minimal: {COOCCURRENCE_MIN_FREQUENCY} occurrences")
    print("CORRECTIONS v1.9 : préservation expressions composées SUR TEXTE ORIGINAL")
    print("Affichage étendu des cooccurrences pour calibrage")
    
    if not os.path.exists(DATA_DIR):
        print(f"Erreur: Le dossier {DATA_DIR} n'existe pas.")
        return
    
    all_cooccurrences = defaultdict(int)
    file_count = 0
    
    # Traitement document par document
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(DATA_DIR, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    
                    # Pipeline v2.0 - correction définitive fragmentation
                    cleaned_text = clean_text_v20_cooccurrence(text)
                    words = tokenize_v18_cooccurrence(cleaned_text)
                    
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
    output_path = os.path.join(CSV_OUTPUT_DIR, 'cooccurrence_pairs_v19_majuscules_fixed.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    print(f"\nTop 50 des cooccurrences les plus fréquentes (calibrage étendu):")
    for i, item in enumerate(cooccurrence_data[:50], 1):
        print(f"{i:3} | ({item['word1']}, {item['word2']}): {item['cooccurrence_count']}")
    
    # Diagnostic expressions composées dans cooccurrences
    print(f"\n=== DIAGNOSTIC EXPRESSIONS COMPOSÉES DANS COOCCURRENCES v1.9 ===")
    compound_cooccurrences = [
        item for item in cooccurrence_data[:50] 
        if any('_' in word for word in [item['word1'], item['word2']])
    ]
    
    if compound_cooccurrences:
        print("✅ Expressions composées détectées dans cooccurrences:")
        for item in compound_cooccurrences:
            print(f"  ({item['word1']}, {item['word2']}): {item['cooccurrence_count']}")
    else:
        print("⚠️  Aucune expression composée dans le top 20 des cooccurrences")

if __name__ == "__main__":
    main()


"""
Calcul des cooccurrences lexicales - Version 2.0 CORRECTIONS TECHNIQUES SYNCHRONISÉES
Ethereum Foundation Discursive Analysis

Corrections v2.0 :
- Synchronisation totale avec extract_word_frequencies v2.0
- Expressions composées avec bornes de mots et tri par longueur
- Préservation caractères utiles et logging technique
- Diagnostic avancé des cooccurrences
"""

import os
import re
import string
import pandas as pd
from collections import defaultdict
import itertools
import sys
import logging
from datetime import datetime
sys.path.append('.')
from config import *

# Configuration logging technique (synchronisé)
os.makedirs('logs', exist_ok=True)
cooc_logger = logging.getLogger('cooccurrences')
cooc_handler = logging.FileHandler(f'logs/cooccurrences_diagnostic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
cooc_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
cooc_logger.addHandler(cooc_handler)
cooc_logger.setLevel(logging.INFO)

# Expressions composées SYNCHRONISÉES (ordonnées par longueur décroissante)
COMPOUND_EXPRESSIONS_RAW = {
    'zero knowledge proof': 'zero_knowledge_proof',
    'ethereum foundation': 'ethereum_foundation', 
    'proof of stake': 'proof_of_stake',
    'proof of work': 'proof_of_work',
    'smart contract': 'smart_contract',
    'smart contracts': 'smart_contracts',
    'execution layer': 'execution_layer',
    'consensus layer': 'consensus_layer',
    'transaction fee': 'transaction_fee',
    'transaction fees': 'transaction_fees',
    'zero knowledge': 'zero_knowledge',
    'layer two': 'layer_2',
    'beacon chain': 'beacon_chain',
    'merkle tree': 'merkle_tree',
    'virtual machine': 'virtual_machine',
    'hard fork': 'hard_fork',
    'soft fork': 'soft_fork',
    'gas fees': 'gas_fees',
    'layer 2': 'layer_2',
    'gas fee': 'gas_fee',
    'web 3': 'web_3',
    'web3': 'web_3'
}

# TRI PAR LONGUEUR DÉCROISSANTE (synchronisé avec extract_word_frequencies)
COMPOUND_EXPRESSIONS = dict(sorted(COMPOUND_EXPRESSIONS_RAW.items(), key=lambda x: -len(x[0])))

def preserve_compound_expressions_v20_sync(text):
    """
    Préservation expressions composées v2.0 - SYNCHRONISÉE TOTALEMENT
    
    SYNCHRONISATION v2.0 avec extract_word_frequencies :
    - Bornes de mots (\b) identiques
    - Tri par longueur identique  
    - Logging synchronisé
    """
    text_preserved = text
    replacements_made = []
    
    # Remplacement avec bornes de mots (identique à extract_word_frequencies)
    for compound, replacement in COMPOUND_EXPRESSIONS.items():
        pattern = re.compile(rf'\b{re.escape(compound)}\b', re.IGNORECASE)
        matches_found = len(pattern.findall(text_preserved))
        
        if matches_found > 0:
            text_preserved = pattern.sub(replacement, text_preserved)
            replacements_made.append((compound, replacement, matches_found))
            cooc_logger.info(f"Cooc - Remplacement: '{compound}' → '{replacement}' ({matches_found})")
    
    # Conversion minuscules APRÈS préservation
    text_lower = text_preserved.lower()
    
    return text_lower

def clean_text_v20_cooccurrence_sync(text):
    """
    Nettoyage harmonisé TOTALEMENT avec extract_word_frequencies v2.0
    """
    if not text:
        return ""
    
    original_length = len(text)
    
    # SYNCHRONISATION : Préservation expressions composées EN PREMIER
    text_preserved = preserve_compound_expressions_v20_sync(text)
    
    # Suppression technique ULTRA-DOUCE (identique)
    text_clean = re.sub(r'https?://[^\s]+', '   ', text_preserved)
    text_clean = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '   ', text_clean)
    text_clean = re.sub(r'0x[a-fA-F0-9]{40,}', '   ', text_clean)
    
    # Normalisation espaces (identique)
    text_final = re.sub(r'\s+', ' ', text_clean).strip()
    
    final_length = len(text_final)
    compression_ratio = final_length / original_length if original_length > 0 else 0
    cooc_logger.info(f"Cooc - Nettoyage: {original_length} → {final_length} chars (ratio: {compression_ratio:.3f})")
    
    return text_final

def tokenize_v20_cooccurrence_sync(text):
    """
    Tokenisation synchronisée v2.0 avec protection caractères
    """
    if not text:
        return []
    
    # SYNCHRONISATION : Préservation des caractères utiles (identique)
    punctuation_to_remove = string.punctuation.replace('_', '').replace('-', '')
    text = text.translate(str.maketrans('', '', punctuation_to_remove))
    
    # Suppression chiffres isolés (identique)
    text = re.sub(r'\b\d+\b', ' ', text)
    
    # Tokenisation (identique)
    words = text.split()
    
    # Filtrage (identique)
    filtered_words = [
        word for word in words 
        if len(word) > MIN_TOKEN_LENGTH and word not in STOPWORDS_MINIMAL
    ]
    
    return filtered_words

def compute_cooccurrences_sliding_window(words, window_size=COOCCURRENCE_WINDOW_SIZE):
    """
    Calcul des cooccurrences par fenêtre glissante v2.0
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
    Pipeline principal cooccurrences v2.0 - SYNCHRONISÉ TOTALEMENT
    """
    print("=== Calcul des cooccurrences lexicales v2.0 CORRECTIONS TECHNIQUES SYNCHRONISÉES ===")
    print(f"Fenêtre glissante: {COOCCURRENCE_WINDOW_SIZE} mots")
    print(f"Seuil minimal: {COOCCURRENCE_MIN_FREQUENCY} occurrences")
    print("SYNCHRONISATION v2.0 : pipeline identique à extract_word_frequencies")
    print("- ✅ Expressions composées avec bornes (\\b) + tri longueur")
    print("- ✅ Préservation caractères utiles (_ et -)")
    print("- ✅ Logging technique dédié")
    print("- Affichage étendu cooccurrences pour calibrage final")
    
    cooc_logger.info("=== DÉBUT CALCUL COOCCURRENCES v2.0 ===")
    
    if not os.path.exists(DATA_DIR):
        error_msg = f"Erreur: Le dossier {DATA_DIR} n'existe pas."
        print(error_msg)
        cooc_logger.error(error_msg)
        return
    
    all_cooccurrences = defaultdict(int)
    file_count = 0
    
    cooc_logger.info(f"Début traitement corpus cooccurrences: {DATA_DIR}")
    
    # Traitement document par document
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(DATA_DIR, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    
                    # Pipeline v2.0 - synchronisé totalement
                    cleaned_text = clean_text_v20_cooccurrence_sync(text)
                    words = tokenize_v20_cooccurrence_sync(cleaned_text)
                    
                    # Calcul des cooccurrences pour ce document
                    doc_cooccurrences = compute_cooccurrences_sliding_window(words)
                    
                    # Agrégation au niveau du corpus
                    for pair, count in doc_cooccurrences.items():
                        all_cooccurrences[pair] += count
                    
                    file_count += 1
                    
                    if VERBOSE_MODE and file_count % 50 == 0:
                        print(f"Traité {file_count} fichiers...")
                        
            except Exception as e:
                error_msg = f"Erreur cooccurrences {filename}: {e}"
                print(error_msg)
                cooc_logger.error(error_msg)
    
    print(f"Traitement terminé: {file_count} fichiers")
    cooc_logger.info(f"Traitement terminé: {file_count} fichiers")
    
    # Filtrage par seuil minimal
    filtered_cooccurrences = {
        pair: count for pair, count in all_cooccurrences.items() 
        if count >= COOCCURRENCE_MIN_FREQUENCY
    }
    
    print(f"Cooccurrences avant filtrage: {len(all_cooccurrences)}")
    print(f"Cooccurrences après filtrage (≥{COOCCURRENCE_MIN_FREQUENCY}): {len(filtered_cooccurrences)}")
    
    cooc_logger.info(f"Cooccurrences avant filtrage: {len(all_cooccurrences)}")
    cooc_logger.info(f"Cooccurrences après filtrage: {len(filtered_cooccurrences)}")
    
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
    output_path = os.path.join(CSV_OUTPUT_DIR, 'cooccurrence_pairs_v20_technical_fixes.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    cooc_logger.info(f"Résultats exportés: {output_path}")
    
    print(f"\nTop 50 des cooccurrences les plus fréquentes (calibrage étendu v2.0):")
    for i, item in enumerate(cooccurrence_data[:50], 1):
        print(f"{i:3} | ({item['word1']}, {item['word2']}): {item['cooccurrence_count']}")
    
    # Diagnostic expressions composées dans cooccurrences v2.0
    print(f"\n=== DIAGNOSTIC EXPRESSIONS COMPOSÉES DANS COOCCURRENCES v2.0 ===")
    compound_cooccurrences = [
        item for item in cooccurrence_data[:50] 
        if any('_' in word for word in [item['word1'], item['word2']])
    ]
    
    if compound_cooccurrences:
        print("✅ Expressions composées détectées dans cooccurrences:")
        for item in compound_cooccurrences:
            print(f"  ({item['word1']}, {item['word2']}): {item['cooccurrence_count']}")
            cooc_logger.info(f"Expression composée cooccurrence: ({item['word1']}, {item['word2']}): {item['cooccurrence_count']}")
    else:
        print("⚠️  Aucune expression composée dans le top 50 des cooccurrences")
        cooc_logger.warning("Aucune expression composée dans top 50 cooccurrences")
    
    # Diagnostic technique : cooccurrences ethereum_foundation
    ethereum_foundation_coocs = [
        item for item in cooccurrence_data[:100]
        if 'ethereum_foundation' in [item['word1'], item['word2']]
    ]
    
    if ethereum_foundation_coocs:
        print(f"\n🔍 Cooccurrences avec 'ethereum_foundation' ({len(ethereum_foundation_coocs)}):")
        for item in ethereum_foundation_coocs[:10]:
            other_word = item['word2'] if item['word1'] == 'ethereum_foundation' else item['word1']
            print(f"  ethereum_foundation + {other_word}: {item['cooccurrence_count']}")
            cooc_logger.info(f"ethereum_foundation cooccurrence: {other_word}: {item['cooccurrence_count']}")
    
    cooc_logger.info("=== FIN CALCUL COOCCURRENCES v2.0 ===")

if __name__ == "__main__":
    main()

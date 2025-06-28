
"""
Extraction des fréquences lexicales - Version 1.8 CORRECTION MAJUSCULES
Ethereum Foundation Discursive Analysis

CORRECTION MAJUSCULES v1.8 :
- Préservation des mots complets avant minuscules 
- Détection expressions composées (zero knowledge, ethereum foundation)
- Correction du problème "thereum", "oundation"
"""

import os
import re
import string
import pandas as pd
from collections import Counter
import sys
sys.path.append('.')
from config import *
from sts_lexicon_corrected import STS_LEXICON_CORRECTED

# Expressions composées à préserver comme entités uniques
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
    Préserve les expressions composées importantes avant tokenisation
    
    Args:
        text (str): Texte d'entrée
        
    Returns:
        str: Texte avec expressions composées préservées
    """
    # Conversion préalable en minuscules pour la détection
    text_lower = text.lower()
    
    # Remplacement des expressions composées par des tokens uniques
    for compound, replacement in COMPOUND_EXPRESSIONS.items():
        text_lower = text_lower.replace(compound, replacement)
    
    return text_lower

def clean_text_v18_fixed(text):
    """
    Nettoyage v1.8 - CORRECTION MAJUSCULES
    
    CORRECTIONS :
    - Préservation expressions composées AVANT minuscules
    - Suppression propre URLs/emails SANS casser les mots
    - Conversion minuscules APRÈS préservation
    
    Args:
        text (str): Texte brut à nettoyer
        
    Returns:
        str: Texte nettoyé avec expressions préservées
    """
    if not text:
        return ""
    
    # ÉTAPE 1 : Préservation des expressions composées AVANT toute modification
    text = preserve_compound_expressions(text)
    
    # ÉTAPE 2 : Suppression des éléments techniques (URLs, emails, adresses crypto)
    # URLs complètes
    text = re.sub(r'https?://[^\s]+', ' ', text)
    
    # Emails 
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', ' ', text)
    
    # Adresses Ethereum (0x...)
    text = re.sub(r'0x[a-fA-F0-9]{40,}', ' ', text)
    
    # ÉTAPE 3 : Normalisation des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_with_punctuation_removal_v18(text):
    """
    Tokenisation v1.8 avec suppression ponctuation et filtrage
    
    Args:
        text (str): Texte nettoyé
        
    Returns:
        list: Liste des tokens valides
    """
    if not text:
        return []
    
    # Suppression de la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Suppression des chiffres isolés (mais pas les termes comme layer_2)
    text = re.sub(r'\b\d+\b', ' ', text)
    
    # Tokenisation par espaces
    words = text.split()
    
    # Filtrage : longueur minimale et stopwords
    filtered_words = [
        word for word in words 
        if len(word) > MIN_TOKEN_LENGTH and word not in STOPWORDS_MINIMAL
    ]
    
    return filtered_words

def categorize_word_with_sts_corrected(word, sts_lexicon):
    """
    Catégorisation STS d'un mot selon le lexique corrigé
    
    Args:
        word (str): Mot à catégoriser
        sts_lexicon (dict): Lexique STS structuré
        
    Returns:
        str: Catégorie STS ou '—' si non catégorisé
    """
    for category, word_set in sts_lexicon.items():
        if word in word_set:
            return category
    return '—'

def main():
    """
    Pipeline principal v1.8 - CORRECTION MAJUSCULES ET EXPRESSIONS
    """
    print("=== Extraction des fréquences lexicales v1.8 CORRECTION MAJUSCULES ===")
    print("CORRECTIONS v1.8 :")
    print("- Préservation expressions composées (zero_knowledge, ethereum_foundation)")
    print("- Correction problème majuscules (thereum → ethereum, oundation → foundation)")
    print("- Nettoyage amélioré préservant vocabulaire technique")
    
    # Vérification de l'existence du dossier
    if not os.path.exists(DATA_DIR):
        print(f"Erreur: Le dossier {DATA_DIR} n'existe pas.")
        return
    
    # Collection de tous les mots
    all_words = []
    file_count = 0
    
    # Traitement de chaque fichier
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(DATA_DIR, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    
                    # Pipeline v1.8 corrigé
                    cleaned_text = clean_text_v18_fixed(text)
                    words = tokenize_with_punctuation_removal_v18(cleaned_text)
                    all_words.extend(words)
                    
                    file_count += 1
                    
                    if VERBOSE_MODE and file_count % 50 == 0:
                        print(f"Traité {file_count} fichiers...")
                        
            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {e}")
    
    print(f"Traitement terminé: {file_count} fichiers, {len(all_words)} tokens totaux")
    
    # Calcul des fréquences
    word_frequencies = Counter(all_words)
    total_words = len(all_words)
    unique_words = len(word_frequencies)
    ttr = unique_words / total_words if total_words > 0 else 0
    
    # Préparation des données pour export avec catégorisation STS
    word_data = []
    sts_word_count = 0
    
    for word, count in word_frequencies.items():
        frequency = count / total_words
        category = categorize_word_with_sts_corrected(word, STS_LEXICON_CORRECTED)
        
        if category != '—':
            sts_word_count += count
        
        word_data.append({
            'word': word,
            'absolute_frequency': count,
            'relative_frequency': frequency,
            'percentage': frequency * 100,
            'sts_category': category
        })
    
    # Tri par fréquence décroissante
    word_data.sort(key=lambda x: x['absolute_frequency'], reverse=True)
    
    # Export CSV
    df = pd.DataFrame(word_data)
    output_path = os.path.join(CSV_OUTPUT_DIR, 'word_frequencies_sts_v18_corrected.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    
    # Analyse STS par catégorie
    print(f"\n=== ANALYSE STS OFFICIELLE (v1.8 CORRECTIONS) ===\n")
    
    categories_analysis = {}
    for category in STS_LEXICON_CORRECTED.keys():
        category_words = [item for item in word_data if item['sts_category'] == category]
        category_words.sort(key=lambda x: x['absolute_frequency'], reverse=True)
        categories_analysis[category] = category_words
    
    # Affichage par catégorie
    for category, words in categories_analysis.items():
        if words:
            print(f"🔹 {category.upper()} ({len(words)} termes):")
            for i, word_info in enumerate(words[:10]):
                print(f"  {word_info['word']}: {word_info['absolute_frequency']}")
            print()
    
    # Top 50 général avec correction expressions composées
    print(f"=== TOP 50 GÉNÉRAL (v1.8 CORRECTIONS - EXPRESSIONS COMPOSÉES) ===")
    for i, word_info in enumerate(word_data[:50], 1):
        category_display = word_info['sts_category'] if word_info['sts_category'] != '—' else '—'
        print(f"{i:3} | {word_info['word']:<25} | {word_info['absolute_frequency']:6} | {word_info['percentage']:6.2f}% | {category_display}")
    
    # Diagnostic expressions composées
    print(f"\n=== DIAGNOSTIC EXPRESSIONS COMPOSÉES v1.8 ===")
    compound_found = []
    for compound, replacement in COMPOUND_EXPRESSIONS.items():
        if replacement in word_frequencies:
            count = word_frequencies[replacement]
            compound_found.append((compound, replacement, count))
            print(f"✅ '{compound}' → '{replacement}': {count} occurrences")
    
    if not compound_found:
        print("⚠️  Aucune expression composée détectée - vérifier préservation")
    
    # Vérification ethereum/foundation
    ethereum_variants = [word for word in word_frequencies.keys() if 'ethereum' in word or 'thereum' in word]
    foundation_variants = [word for word in word_frequencies.keys() if 'foundation' in word or 'oundation' in word]
    
    print(f"\n🔍 Variantes ETHEREUM détectées ({len(ethereum_variants)}):")
    for variant in sorted(ethereum_variants, key=lambda x: word_frequencies[x], reverse=True)[:10]:
        print(f"   {variant}: {word_frequencies[variant]}")
    
    print(f"\n🔍 Variantes FOUNDATION détectées ({len(foundation_variants)}):")
    for variant in sorted(foundation_variants, key=lambda x: word_frequencies[x], reverse=True)[:10]:
        print(f"   {variant}: {word_frequencies[variant]}")
    
    # Statistiques globales
    print(f"\n=== STATISTIQUES GLOBALES v1.8 ===")
    print(f"Vocabulaire unique: {unique_words:,} termes")
    print(f"Tokens totaux: {total_words:,}")
    print(f"Richesse lexicale (TTR): {ttr:.4f}")
    print(f"Fréquence STS totale: {sts_word_count:,}")
    print(f"Part STS du corpus: {(sts_word_count/total_words)*100:.2f}%")

if __name__ == "__main__":
    main()

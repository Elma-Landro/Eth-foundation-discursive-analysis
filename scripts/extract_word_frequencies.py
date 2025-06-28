
"""
Extraction des fréquences lexicales - Version 1.1
Ethereum Foundation Discursive Analysis

Corrections v1.1 :
- Correction regex email (échappement \b)
- Préservation des termes techniques crypto
- Intégration configuration centralisée
- Documentation méthodologique renforcée
"""

import os
import re
import string
import pandas as pd
from collections import Counter
import sys
sys.path.append('.')
from config import *

def clean_text_advanced(text):
    """
    Nettoyage textuel avancé orienté STS - Version 1.2
    
    Approche méthodologique :
    - Correction de la troncature "thereum" → "ethereum"
    - Nettoyage minimal pour préserver les catégories indigènes
    - Préservation des termes techniques crypto (EIP, web3, etc.)
    - Suppression ciblée des artéfacts techniques (URLs, adresses ETH)
    
    Args:
        text (str): Texte brut à nettoyer
        
    Returns:
        str: Texte nettoyé
    """
    # CORRECTION CRITIQUE v1.2: Normalisation avant mise en minuscules
    # Pré-traitement pour éviter les troncatures
    text = re.sub(r'\s+', ' ', text.strip())  # Normalisation des espaces AVANT lower()
    
    text = text.lower()

    # Suppression des URLs (préservation du contenu discursif)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Suppression des emails - CORRECTION CRITIQUE v1.1
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    # Suppression des adresses Ethereum (artéfacts techniques)
    text = re.sub(r'0x[a-fA-F0-9]{40,}', '', text)

    # CORRECTION CRITIQUE v1.2 : Préservation termes complets AVANT suppression ponctuation
    # Sauvegarde complète des termes techniques ET des termes STS
    temp_replacements = {}
    
    if PRESERVE_CRYPTO_TERMS:
        for i, term in enumerate(CRYPTO_TECHNICAL_TERMS):
            placeholder = f"CRYPTOTERM{i}PLACEHOLDER"
            if term in text:
                text = text.replace(term, placeholder)
                temp_replacements[placeholder] = term
    
    # Sauvegarde des termes STS critiques pour éviter leur fragmentation
    sts_critical_terms = ['ethereum', 'blockchain', 'decentralized', 'consensus', 'governance', 'protocol']
    for i, term in enumerate(sts_critical_terms):
        placeholder = f"STSTERM{i}PLACEHOLDER"
        if term in text:
            text = text.replace(term, placeholder)
            temp_replacements[placeholder] = term

    # Suppression de la ponctuation (APRÈS sauvegarde)
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Suppression des chiffres isolés (mais préservation des termes comme "web3", "eip1559")
    text = re.sub(r'\b\d+\b', '', text)
    
    # Restauration de TOUS les termes sauvegardés
    for placeholder, original_term in temp_replacements.items():
        text = text.replace(placeholder, original_term)

    # Nettoyage final des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def tokenize_strict(text):
    """
    Tokenisation stricte avec filtrage par stopwords minimaux
    
    Approche méthodologique :
    - Stopwords minimaux pour préserver le vocabulaire technique
    - Filtrage par longueur pour éliminer les artéfacts
    - Conservation des termes composés pertinents
    
    Args:
        text (str): Texte à tokeniser
        
    Returns:
        list: Liste des tokens valides
    """
    words = text.split()
    
    # Filtrage : longueur minimale + stopwords
    valid_tokens = [
        word for word in words 
        if len(word) > MIN_TOKEN_LENGTH and word not in STOPWORDS_MINIMAL
    ]
    
    if LOG_PROCESSING_STEPS:
        print(f"Tokens avant filtrage: {len(words)}, après filtrage: {len(valid_tokens)}")
    
    return valid_tokens

def categorize_sts_terms(word_frequencies):
    """
    Catégorisation STS automatique pour codage axial
    
    Args:
        word_frequencies (Counter): Compteur de fréquences
        
    Returns:
        dict: Termes catégorisés par domaine STS
    """
    sts_categorized = {}
    
    for category, terms in STS_LEXICON.items():
        sts_categorized[category] = []
        for word, freq in word_frequencies.most_common():
            if word in terms:
                sts_categorized[category].append((word, freq))
    
    return sts_categorized

def main():
    """
    Pipeline principal d'extraction des fréquences lexicales - Version STS 1.2
    """
    print("=== Extraction des fréquences lexicales v1.2 STS ===")
    print(f"Configuration: stopwords enrichie, préservation crypto: {PRESERVE_CRYPTO_TERMS}")
    print(f"Lexique STS: {len(STS_LEXICON)} catégories sociotechniques")
    
    # Vérification de l'existence du dossier de données
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
                    
                    # Pipeline de traitement
                    cleaned_text = clean_text_advanced(text)
                    words = tokenize_strict(cleaned_text)
                    all_words.extend(words)
                    
                    file_count += 1
                    
                    if VERBOSE_MODE and file_count % 50 == 0:
                        print(f"Traité {file_count} fichiers...")
                        
            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {e}")
    
    print(f"Traitement terminé: {file_count} fichiers, {len(all_words)} tokens totaux")
    
    # Calcul des fréquences
    word_frequencies = Counter(all_words)
    
    # Catégorisation STS pour codage axial
    sts_categorized = categorize_sts_terms(word_frequencies)
    
    # Préparation des données pour export avec catégories STS
    sts_category_map = {}
    for category, terms in STS_LEXICON.items():
        for term in terms:
            sts_category_map[term] = category
    
    df = pd.DataFrame([
        {
            'word': word, 
            'frequency': freq, 
            'relative_frequency': freq/len(all_words),
            'sts_category': sts_category_map.get(word, 'uncategorized')
        }
        for word, freq in word_frequencies.most_common()
    ])
    
    # Export CSV enrichi
    output_path = os.path.join(CSV_OUTPUT_DIR, 'word_frequencies_sts.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    
    # Affichage des termes STS par catégorie (PRIORITÉ POUR CODAGE AXIAL)
    print(f"\n=== ANALYSE STS POUR CODAGE AXIAL ===")
    for category, terms_list in sts_categorized.items():
        if terms_list:
            print(f"\n🔹 {category.upper()} ({len(terms_list)} termes):")
            for word, freq in terms_list[:10]:  # Top 10 par catégorie
                print(f"  {word}: {freq}")
    
    # Top 30 général (après filtrage STS)
    print(f"\n=== TOP 30 GÉNÉRAL (post-nettoyage STS) ===")
    for word, freq in word_frequencies.most_common(30):
        category = sts_category_map.get(word, '')
        category_marker = f" [{category}]" if category != 'uncategorized' else ""
        print(f"  {word}: {freq}{category_marker}")
    
    # Diagnostic de correction
    print(f"\n=== Diagnostic corrections v1.2 ===")
    ethereum_variants = [word for word, freq in word_frequencies.items() if 'ethereum' in word or 'thereum' in word]
    print(f"Variants Ethereum détectés: {ethereum_variants}")
    
    # Statistiques méthodologiques STS
    print(f"\n=== Statistiques méthodologiques STS ===")
    print(f"Vocabulaire unique: {len(word_frequencies)} termes")
    print(f"Tokens totaux: {len(all_words)}")
    print(f"Richesse lexicale (TTR): {len(word_frequencies)/len(all_words):.4f}")
    
    sts_terms_count = sum(len(terms_list) for terms_list in sts_categorized.values())
    print(f"Termes STS identifiés: {sts_terms_count}")
    print(f"Couverture STS: {sts_terms_count/len(word_frequencies)*100:.2f}%")

if __name__ == "__main__":
    main()

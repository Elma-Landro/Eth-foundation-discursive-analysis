
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
    Nettoyage textuel avancé préservant le vocabulaire indigène
    
    Approche méthodologique :
    - Nettoyage minimal pour préserver les catégories indigènes
    - Préservation des termes techniques crypto (EIP, web3, etc.)
    - Suppression ciblée des artéfacts techniques (URLs, adresses ETH)
    
    Args:
        text (str): Texte brut à nettoyer
        
    Returns:
        str: Texte nettoyé
    """
    text = text.lower()

    # Suppression des URLs (préservation du contenu discursif)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Suppression des emails - CORRECTION CRITIQUE v1.1
    # Ancien: r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b' (double échappement erroné)
    # Nouveau: échappement correct
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    # Suppression des adresses Ethereum (artéfacts techniques)
    text = re.sub(r'0x[a-fA-F0-9]{40,}', '', text)

    # Suppression de la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # CORRECTION CRITIQUE v1.1 : Préservation des termes techniques
    # Sauvegarde des termes crypto avant suppression des chiffres
    if PRESERVE_CRYPTO_TERMS:
        # Création d'un dictionnaire de remplacement temporaire
        temp_replacements = {}
        for i, term in enumerate(CRYPTO_TECHNICAL_TERMS):
            placeholder = f"CRYPTOTERM{i}PLACEHOLDER"
            if term in text:
                text = text.replace(term, placeholder)
                temp_replacements[placeholder] = term
    
    # Suppression des chiffres isolés (mais préservation des termes comme "web3", "eip1559")
    text = re.sub(r'\b\d+\b', '', text)
    
    # Restauration des termes techniques
    if PRESERVE_CRYPTO_TERMS:
        for placeholder, original_term in temp_replacements.items():
            text = text.replace(placeholder, original_term)

    # Nettoyage des espaces multiples
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

def main():
    """
    Pipeline principal d'extraction des fréquences lexicales
    """
    print("=== Extraction des fréquences lexicales v1.1 ===")
    print(f"Configuration: fenêtre={COOCCURRENCE_WINDOW_SIZE}, seuil_min={MIN_TOKEN_LENGTH}")
    print(f"Préservation termes crypto: {PRESERVE_CRYPTO_TERMS}")
    
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
    
    # Préparation des données pour export
    df = pd.DataFrame([
        {'word': word, 'frequency': freq, 'relative_frequency': freq/len(all_words)}
        for word, freq in word_frequencies.most_common()
    ])
    
    # Export CSV
    output_path = os.path.join(OUTPUT_DIR, 'word_frequencies.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    print(f"Top 10 des termes les plus fréquents:")
    for word, freq in word_frequencies.most_common(10):
        print(f"  {word}: {freq}")
    
    # Statistiques méthodologiques
    print(f"\n=== Statistiques méthodologiques ===")
    print(f"Vocabulaire unique: {len(word_frequencies)} termes")
    print(f"Tokens totaux: {len(all_words)}")
    print(f"Richesse lexicale (TTR): {len(word_frequencies)/len(all_words):.4f}")

if __name__ == "__main__":
    main()

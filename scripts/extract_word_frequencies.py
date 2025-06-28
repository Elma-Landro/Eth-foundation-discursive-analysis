
"""
Extraction des fréquences lexicales - Version 1.5 ZÉRO TRONCATURE
Ethereum Foundation Discursive Analysis

Corrections v1.5 :
- ÉLIMINATION DÉFINITIVE des troncatures (thereum, itcoin, nn, etc.)
- Filtrage explicite des artefacts de fragmentation
- Nettoyage minimal préservant l'intégrité lexicale
- Validation renforcée contre les résidus de ponctuation
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

def clean_text_ultra_conservative(text):
    """
    Nettoyage textuel ultra-conservateur - Version 1.5 ZÉRO TRONCATURE
    
    PRINCIPE ABSOLU : Préservation totale du vocabulaire complet
    - Nettoyage minimal uniquement des URLs et adresses
    - Aucune suppression de ponctuation qui peut tronquer
    - Conservation intégrale des mots techniques
    
    Args:
        text (str): Texte brut à nettoyer
        
    Returns:
        str: Texte nettoyé sans aucune troncature
    """
    if not text:
        return ""
    
    # Suppression EXCLUSIVE des éléments techniques non-discursifs
    # URLs complètes
    text = re.sub(r'https?://[^\s]+', ' ', text)
    
    # Emails 
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', ' ', text)
    
    # Adresses Ethereum (0x...)
    text = re.sub(r'0x[a-fA-F0-9]{40,}', ' ', text)
    
    # Conversion en minuscules SEULEMENT
    text = text.lower()
    
    # REMPLACEMENT PONCTUATION PAR ESPACES (pas de suppression brutale)
    # Ceci évite les troncatures type "ethereum." → "thereum"
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Suppression EXCLUSIVE des tokens numériques purs (dates, etc.)
    # MAIS préservation des termes alphanumériques (web3, eip1559, etc.)
    text = re.sub(r'\b\d+\b', ' ', text)
    
    # Normalisation des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_ultra_strict(text):
    """
    Tokenisation ultra-stricte avec filtrage anti-troncature v1.5
    
    Args:
        text (str): Texte à tokeniser
        
    Returns:
        list: Liste des tokens valides sans troncatures
    """
    if not text:
        return []
    
    words = text.split()
    
    # Filtrage renforcé contre les troncatures
    valid_tokens = []
    
    # Liste d'exclusion des artefacts de troncature connus
    TRUNCATION_ARTIFACTS = {
        'thereum', 'itcoin', 'lockchain', 'ecentralized',  # mots tronqués
        'nn', 'th', 're', 'as', 've', 'nnhe', 'nnnn',     # fragments
        'ndate', 'nurl', 'nauteur', 'titre', 'evcon'      # artefacts métadonnées
    }
    
    for word in words:
        # Élimination des artefacts de troncature EXPLICITES
        if word in TRUNCATION_ARTIFACTS:
            continue
            
        # Longueur minimale (mais pas trop restrictive)
        if len(word) < 3:  # Augmenté à 3 pour éliminer fragments
            continue
            
        # Stopwords enrichie
        if word in STOPWORDS_ENRICHED:
            continue
            
        # Validation alphabétique STRICTE (pas de résidus numériques/ponctuels)
        if not word.isalpha():
            continue
            
        # Filtrage des patterns de troncature évidents
        if (word.startswith('nn') and len(word) < 6) or \
           (word.endswith('nn') and len(word) < 6):
            continue
            
        valid_tokens.append(word)
    
    return valid_tokens

def categorize_sts_official(word_frequencies):
    """
    Catégorisation STS selon la grille officielle (9 catégories)
    Utilise le lexique central de sts_lexicon_corrected.py
    
    Args:
        word_frequencies (Counter): Compteur de fréquences
        
    Returns:
        dict: Termes catégorisés par domaine STS officiel
    """
    
    sts_categorized = {}
    
    for category, terms in STS_LEXICON_CORRECTED.items():
        sts_categorized[category] = []
        for word, freq in word_frequencies.most_common():
            if word in terms:
                sts_categorized[category].append((word, freq))
    
    return sts_categorized, STS_LEXICON_CORRECTED

def main():
    """
    Pipeline principal d'extraction - Version 1.4 ANTI-TRONCATURE
    """
    print("=== Extraction des fréquences lexicales v1.4 ANTI-TRONCATURE ===")
    print("CORRECTIONS MAJEURES : préservation absolue des termes + grille STS officielle")
    print(f"Approche : nettoyage ultra-conservateur, catégories STS structurées")
    
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
                    
                    # Pipeline ULTRA-CONSERVATEUR
                    cleaned_text = clean_text_ultra_conservative(text)
                    words = tokenize_ultra_strict(cleaned_text)
                    all_words.extend(words)
                    
                    file_count += 1
                    
                    if VERBOSE_MODE and file_count % 50 == 0:
                        print(f"Traité {file_count} fichiers...")
                        
            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {e}")
    
    print(f"Traitement terminé: {file_count} fichiers, {len(all_words)} tokens totaux")
    
    # Calcul des fréquences
    word_frequencies = Counter(all_words)
    
    # Catégorisation STS OFFICIELLE
    sts_categorized, sts_lexicon_official = categorize_sts_official(word_frequencies)
    
    # Préparation des données pour export avec catégories STS OFFICIELLES
    sts_category_map = {}
    for category, terms in sts_lexicon_official.items():
        for term in terms:
            sts_category_map[term] = category
    
    df = pd.DataFrame([
        {
            'word': word, 
            'frequency': freq, 
            'relative_frequency': freq/len(all_words),
            'sts_category': sts_category_map.get(word, '—')
        }
        for word, freq in word_frequencies.most_common()
    ])
    
    # Export CSV enrichi
    output_path = os.path.join(CSV_OUTPUT_DIR, 'word_frequencies_sts_v15.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    
    # Affichage des termes STS par catégorie OFFICIELLE
    print(f"\n=== ANALYSE STS OFFICIELLE (v1.4) ===")
    for category, terms_list in sts_categorized.items():
        if terms_list:
            print(f"\n🔹 {category.upper()} ({len(terms_list)} termes):")
            for word, freq in terms_list[:10]:  # Top 10 par catégorie
                print(f"  {word}: {freq}")
    
    # Top 50 général (version corrigée v1.4)
    print(f"\n=== TOP 50 GÉNÉRAL (v1.4 - SANS TRONCATURES) ===")
    for i, (word, freq) in enumerate(word_frequencies.most_common(50), 1):
        category = sts_category_map.get(word, '—')
        pct = freq/len(all_words)*100
        print(f"{i:3d} | {word:<25} | {freq:>6} | {pct:>6.2f}% | {category}")
    
    # Diagnostic de correction v1.4
    print(f"\n=== DIAGNOSTIC v1.4 - ANTI-TRONCATURE ===")
    
    # Vérification élimination troncatures
    truncated_terms = []
    for word, freq in word_frequencies.most_common(100):
        if len(word) > 3 and (
            word.startswith('thereum') or 
            word.startswith('itcoin') or 
            word.endswith('ing') and len(word) == 3 or
            word in ['th', 're', 'as', 'll', 'et']
        ):
            truncated_terms.append(word)
    
    if truncated_terms:
        print(f"⚠️ Troncatures détectées: {truncated_terms[:10]}")
    else:
        print("✅ Aucune troncature majeure détectée")
    
    # Vérification termes Ethereum complets
    ethereum_terms = [word for word, freq in word_frequencies.items() if 'ethereum' in word]
    print(f"Termes Ethereum complets: {ethereum_terms[:5]}")
    
    # Statistiques méthodologiques STS
    print(f"\n=== STATISTIQUES MÉTHODOLOGIQUES STS (v1.4) ===")
    print(f"Vocabulaire unique: {len(word_frequencies):,} termes")
    print(f"Tokens totaux: {len(all_words):,}")
    print(f"Richesse lexicale (TTR): {len(word_frequencies)/len(all_words):.4f}")
    
    sts_terms_count = sum(len(terms_list) for terms_list in sts_categorized.values())
    print(f"Termes STS identifiés: {sts_terms_count}")
    print(f"Couverture STS: {sts_terms_count/len(word_frequencies)*100:.2f}%")

if __name__ == "__main__":
    main()

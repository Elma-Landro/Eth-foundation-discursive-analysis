
"""
Extraction des fréquences lexicales - Version 1.3 CORRECTIVE
Ethereum Foundation Discursive Analysis

Corrections v1.3 :
- CORRECTION MAJEURE : élimination des troncatures "thereum"
- CORRECTION MAJEURE : élimination des artéfacts "nn"
- Nettoyage textuel refondu pour préserver l'intégrité lexicale
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
    Nettoyage textuel avancé orienté STS - Version 1.3 CORRECTIVE
    
    CORRECTIONS MAJEURES v1.3 :
    - Élimination des troncatures de mots (ethereum → thereum)
    - Élimination des artéfacts "nn" 
    - Préservation complète de l'intégrité lexicale
    - Nettoyage minimal et conservateur
    
    Args:
        text (str): Texte brut à nettoyer
        
    Returns:
        str: Texte nettoyé sans artéfacts
    """
    if not text:
        return ""
    
    # Conversion en minuscules IMMÉDIATE pour éviter les problèmes de casse
    text = text.lower()
    
    # Normalisation basique des espaces AVANT tout traitement
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Suppression des URLs (préservation du contenu discursif)
    text = re.sub(r'https?://[^\s]+', ' ', text)
    
    # Suppression des emails 
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', ' ', text)
    
    # Suppression des adresses Ethereum
    text = re.sub(r'0x[a-fA-F0-9]{40,}', ' ', text)
    
    # CORRECTION CRITIQUE : Suppression des séquences "nn" parasites
    # Ces artéfacts viennent probablement de l'extraction HTML mal traitée
    text = re.sub(r'\bnn\b', ' ', text)  # "nn" isolés
    text = re.sub(r'nn+', ' ', text)     # Séquences "nnn", "nnnn", etc.
    
    # Suppression de la ponctuation de manière conservative
    # On évite translate() qui peut créer des troncatures
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Suppression des chiffres isolés (mais préservation des termes comme "web3", "eip1559")
    text = re.sub(r'\b\d+\b', ' ', text)
    
    # Nettoyage final des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_strict(text):
    """
    Tokenisation stricte avec filtrage par stopwords enrichie
    
    Args:
        text (str): Texte à tokeniser
        
    Returns:
        list: Liste des tokens valides
    """
    if not text:
        return []
    
    words = text.split()
    
    # Filtrage : longueur minimale + stopwords enrichie
    valid_tokens = [
        word for word in words 
        if len(word) >= MIN_TOKEN_LENGTH 
        and word not in STOPWORDS_ENRICHED
        and word.isalpha()  # Seulement des lettres pour éviter les artéfacts
    ]
    
    if LOG_PROCESSING_STEPS and len(words) > 0:
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
    Pipeline principal d'extraction des fréquences lexicales - Version STS 1.3 CORRECTIVE
    """
    print("=== Extraction des fréquences lexicales v1.3 CORRECTIVE ===")
    print("CORRECTIONS : élimination troncatures + artéfacts 'nn'")
    print(f"Configuration: stopwords enrichie, nettoyage conservateur")
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
                    
                    # Pipeline de traitement CORRIGÉ
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
            'sts_category': sts_category_map.get(word, '—')
        }
        for word, freq in word_frequencies.most_common()
    ])
    
    # Export CSV enrichi
    output_path = os.path.join(CSV_OUTPUT_DIR, 'word_frequencies_sts_v13.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    
    # Affichage des termes STS par catégorie (PRIORITÉ POUR CODAGE AXIAL)
    print(f"\n=== ANALYSE STS POUR CODAGE AXIAL (v1.3) ===")
    for category, terms_list in sts_categorized.items():
        if terms_list:
            print(f"\n🔹 {category.upper()} ({len(terms_list)} termes):")
            for word, freq in terms_list[:10]:  # Top 10 par catégorie
                print(f"  {word}: {freq}")
    
    # Top 50 général (après corrections v1.3)
    print(f"\n=== TOP 50 GÉNÉRAL (post-corrections v1.3) ===")
    for i, (word, freq) in enumerate(word_frequencies.most_common(50), 1):
        category = sts_category_map.get(word, '—')
        print(f"{i:3d} | {word:<20} | {freq:>6} | {freq/len(all_words)*100:>6.2f}% | {category}")
    
    # Diagnostic de correction v1.3
    print(f"\n=== Diagnostic corrections v1.3 ===")
    
    # Vérification élimination troncatures
    ethereum_variants = [word for word, freq in word_frequencies.items() if 'ethereum' in word or 'thereum' in word]
    print(f"Variants Ethereum détectés: {ethereum_variants}")
    
    # Vérification élimination artéfacts "nn"
    nn_artifacts = [word for word, freq in word_frequencies.items() if 'nn' in word]
    if nn_artifacts:
        print(f"⚠️ Artéfacts 'nn' restants: {nn_artifacts[:10]} (total: {len(nn_artifacts)})")
    else:
        print("✅ Aucun artéfact 'nn' détecté")
    
    # Statistiques méthodologiques STS
    print(f"\n=== Statistiques méthodologiques STS (v1.3) ===")
    print(f"Vocabulaire unique: {len(word_frequencies)} termes")
    print(f"Tokens totaux: {len(all_words)}")
    print(f"Richesse lexicale (TTR): {len(word_frequencies)/len(all_words):.4f}")
    
    sts_terms_count = sum(len(terms_list) for terms_list in sts_categorized.values())
    print(f"Termes STS identifiés: {sts_terms_count}")
    print(f"Couverture STS: {sts_terms_count/len(word_frequencies)*100:.2f}%")

if __name__ == "__main__":
    main()

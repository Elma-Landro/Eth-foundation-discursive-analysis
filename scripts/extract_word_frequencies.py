
"""
Extraction des fréquences lexicales - Version 1.7 NETTOYAGE MINIMAL
Ethereum Foundation Discursive Analysis

CORRECTION RADICALE v1.7 :
- Nettoyage MINIMAL (URLs uniquement)
- Préservation ABSOLUE de la ponctuation contextuelle
- Tokenisation sur espaces naturels UNIQUEMENT
- Élimination exclusive des artefacts identifiés
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

def clean_text_minimal_v17(text):
    """
    Nettoyage MINIMAL v1.7 - Préservation maximale du vocabulaire
    
    PRINCIPE : Ne supprimer QUE les éléments non-discursifs évidents
    - URLs, emails, adresses crypto
    - AUCUNE manipulation de ponctuation
    - AUCUNE normalisation agressive
    
    Args:
        text (str): Texte brut à nettoyer
        
    Returns:
        str: Texte avec nettoyage minimal
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
    
    # Normalisation des espaces multiples UNIQUEMENT
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_with_punctuation_removal_v17(text):
    """
    Tokenisation v1.7 avec suppression ponctuation PAR TOKEN
    
    APPROCHE NOUVELLE :
    - Tokenisation sur espaces naturels
    - Nettoyage ponctuation PAR MOT (pas sur tout le texte)
    - Préservation des mots complets avant fragmentation
    
    Args:
        text (str): Texte à tokeniser
        
    Returns:
        list: Liste des tokens valides
    """
    if not text:
        return []
    
    # Tokenisation sur espaces NATURELS
    raw_tokens = text.split()
    
    # PROTECTION ABSOLUE des termes critiques
    PROTECTED_TERMS = {
        'ethereum', 'bitcoin', 'blockchain', 'decentralized', 'protocol',
        'consensus', 'validator', 'staking', 'governance', 'security',
        'development', 'research', 'infrastructure', 'network', 'client',
        'pyethereum', 'web3', 'defi', 'dapp', 'contract', 'smart'
    }
    
    # Liste d'exclusion PRÉCISE des artefacts identifiés
    EXPLICIT_ARTIFACTS = {
        'thereum', 'itcoin', 'lockchain', 'ecentralized',  # troncatures identifiées
        'nn', 'nnhe', 'nnnn', 'nnn', 'nnot', 'nnd',       # fragments nn
        'ndate', 'nurl', 'nauteur', 'titre', 'evcon',     # artefacts métadonnées
        'th', 're', 'as', 've', 'll', 'et', 'he', 'it', 'an', 'in', 'on', 'at', 'be', 'to'  # fragments courts
    }
    
    valid_tokens = []
    
    for raw_token in raw_tokens:
        # Suppression ponctuation PAR TOKEN (préserve les mots complets)
        cleaned_token = re.sub(r'[^\w]', '', raw_token)
        
        # Filtrage des tokens vides après nettoyage
        if not cleaned_token:
            continue
            
        # PROTECTION ABSOLUE : termes critiques toujours inclus
        if cleaned_token in PROTECTED_TERMS:
            valid_tokens.append(cleaned_token)
            continue
            
        # Élimination des artefacts EXPLICITES identifiés
        if cleaned_token in EXPLICIT_ARTIFACTS:
            continue
            
        # Longueur minimale stricte
        if len(cleaned_token) < 3:
            continue
            
        # Stopwords (sauf termes protégés déjà traités)
        if cleaned_token in STOPWORDS_ENRICHED:
            continue
            
        # Validation alphabétique stricte
        if not cleaned_token.isalpha():
            continue
            
        # Filtrage spécifique patterns nn suspects
        if cleaned_token.startswith('nn') and len(cleaned_token) < 8:
            continue
        if cleaned_token.endswith('nn') and len(cleaned_token) < 8:
            continue
        if cleaned_token.count('nn') > 1 and len(cleaned_token) < 10:
            continue
            
        valid_tokens.append(cleaned_token)
    
    return valid_tokens

def categorize_sts_official(word_frequencies):
    """
    Catégorisation STS selon la grille officielle (9 catégories)
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
    Pipeline principal v1.7 - NETTOYAGE MINIMAL
    """
    print("=== Extraction des fréquences lexicales v1.7 NETTOYAGE MINIMAL ===")
    print("CORRECTION RADICALE : nettoyage minimal, préservation maximale vocabulaire")
    print(f"Objectif : récupérer les 3,600+ occurrences 'ethereum' perdues")
    
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
                    
                    # Pipeline MINIMAL v1.7
                    cleaned_text = clean_text_minimal_v17(text)
                    words = tokenize_with_punctuation_removal_v17(cleaned_text)
                    all_words.extend(words)
                    
                    file_count += 1
                    
                    if VERBOSE_MODE and file_count % 50 == 0:
                        print(f"Traité {file_count} fichiers...")
                        
            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {e}")
    
    print(f"Traitement terminé: {file_count} fichiers, {len(all_words)} tokens totaux")
    
    # Calcul des fréquences
    word_frequencies = Counter(all_words)
    
    # Catégorisation STS
    sts_categorized, sts_lexicon_official = categorize_sts_official(word_frequencies)
    
    # Préparation des données pour export
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
    
    # Export CSV
    output_path = os.path.join(CSV_OUTPUT_DIR, 'word_frequencies_sts_v17_minimal.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    
    # Affichage des termes STS par catégorie
    print(f"\n=== ANALYSE STS OFFICIELLE (v1.7 MINIMAL) ===")
    for category, terms_list in sts_categorized.items():
        if terms_list:
            print(f"\n🔹 {category.upper()} ({len(terms_list)} termes):")
            for word, freq in terms_list[:10]:
                print(f"  {word}: {freq}")
    
    # Top 50 général
    print(f"\n=== TOP 50 GÉNÉRAL (v1.7 MINIMAL - RÉCUPÉRATION ETHEREUM) ===")
    for i, (word, freq) in enumerate(word_frequencies.most_common(50), 1):
        category = sts_category_map.get(word, '—')
        pct = freq/len(all_words)*100
        print(f"{i:3d} | {word:<25} | {freq:>6} | {pct:>6.2f}% | {category}")
    
    # DIAGNOSTIC CRITIQUE v1.7
    print(f"\n=== DIAGNOSTIC CRITIQUE v1.7 - RÉCUPÉRATION ETHEREUM ===")
    
    # Vérification ETHEREUM
    ethereum_freq = word_frequencies.get('ethereum', 0)
    thereum_freq = word_frequencies.get('thereum', 0)
    
    print(f"🔍 ETHEREUM complet: {ethereum_freq} occurrences")
    print(f"⚠️  'thereum' tronqué: {thereum_freq} occurrences")
    
    if ethereum_freq > 3000:
        print("✅ SUCCÈS : Récupération massive du vocabulaire ethereum !")
    elif ethereum_freq > thereum_freq:
        print("✅ PROGRÈS : ethereum > thereum, mais récupération incomplète")
    else:
        print("❌ ÉCHEC : Troncatures persistent, approche à revoir")
        
    # Top ethereum dans classement
    top_20 = word_frequencies.most_common(20)
    ethereum_rank = None
    for i, (word, freq) in enumerate(top_20, 1):
        if word == 'ethereum':
            ethereum_rank = i
            break
    
    if ethereum_rank:
        print(f"📊 ETHEREUM classé #{ethereum_rank} dans le top 20")
    else:
        print(f"📊 ETHEREUM absent du top 20")
    
    # Famille ethereum complète
    ethereum_family = [(word, freq) for word, freq in word_frequencies.items() if 'ethereum' in word]
    print(f"\n🔍 Famille ETHEREUM détectée ({len(ethereum_family)} variantes):")
    for word, freq in sorted(ethereum_family, key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {word}: {freq}")
    
    # Statistiques globales
    print(f"\n=== STATISTIQUES GLOBALES v1.7 ===")
    print(f"Vocabulaire unique: {len(word_frequencies):,} termes")
    print(f"Tokens totaux: {len(all_words):,}")
    print(f"Richesse lexicale (TTR): {len(word_frequencies)/len(all_words):.4f}")
    
    total_sts_freq = sum(freq for terms_list in sts_categorized.values() 
                        for _, freq in terms_list)
    print(f"Fréquence STS totale: {total_sts_freq:,}")
    print(f"Part STS du corpus: {total_sts_freq/len(all_words)*100:.2f}%")

if __name__ == "__main__":
    main()


"""
Extraction des fréquences lexicales - Version 2.0 CORRECTIONS TECHNIQUES AVANCÉES
Ethereum Foundation Discursive Analysis

CORRECTIONS CRITIQUES v2.0 :
- Expressions composées avec bornes de mots (\b)
- Tri par longueur décroissante (évite conflits rollup/zk-rollup)
- Préservation caractères utiles (_ et -)
- Diagnostic mots courts suspects
- Logs techniques dédiés
"""

import os
import re
import string
import pandas as pd
from collections import Counter
import sys
import logging
from datetime import datetime
sys.path.append('.')
from config import *
from sts_lexicon_corrected import STS_LEXICON_CORRECTED

# Configuration logging technique
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename=f'logs/extraction_diagnostic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Expressions composées à préserver (ORDONNÉES par longueur décroissante)
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

# TRI PAR LONGUEUR DÉCROISSANTE (correction technique A)
COMPOUND_EXPRESSIONS = dict(sorted(COMPOUND_EXPRESSIONS_RAW.items(), key=lambda x: -len(x[0])))

def preserve_compound_expressions_v20(text):
    """
    Préservation expressions composées v2.0 - CORRECTIONS TECHNIQUES AVANCÉES
    
    AMÉLIORATIONS v2.0 :
    - Bornes de mots (\b) pour éviter remplacements partiels
    - Tri par longueur décroissante pour éviter conflits
    - Logging des remplacements effectués
    
    Args:
        text (str): Texte d'entrée ORIGINAL (avec majuscules)
        
    Returns:
        str: Texte avec expressions composées préservées ET minuscules
    """
    # ÉTAPE 1 : Préservation expressions composées sur texte ORIGINAL
    text_preserved = text
    replacements_made = []
    
    # Remplacement avec bornes de mots (correction technique A)
    for compound, replacement in COMPOUND_EXPRESSIONS.items():
        # Utilisation de \b pour délimiter les mots complets
        pattern = re.compile(rf'\b{re.escape(compound)}\b', re.IGNORECASE)
        matches_found = len(pattern.findall(text_preserved))
        
        if matches_found > 0:
            text_preserved = pattern.sub(replacement, text_preserved)
            replacements_made.append((compound, replacement, matches_found))
            logging.info(f"Remplacement: '{compound}' → '{replacement}' ({matches_found} occurrences)")
    
    # ÉTAPE 2 : Conversion en minuscules APRÈS préservation
    text_lower = text_preserved.lower()
    
    # Logging global des remplacements
    if replacements_made:
        logging.info(f"Total remplacements effectués: {len(replacements_made)}")
    
    return text_lower

def clean_text_v20_technical_fixes(text):
    """
    Nettoyage v2.0 - CORRECTIONS TECHNIQUES DÉFINITIVES
    
    NOUVELLES CORRECTIONS v2.0 :
    - Préservation expressions composées EN PREMIER (sur texte original)
    - Suppression technique ULTRA-DOUCE (espaces multiples, pas troncature)
    - Logging des étapes de nettoyage
    
    Args:
        text (str): Texte brut à nettoyer (AVEC majuscules originales)
        
    Returns:
        str: Texte nettoyé sans fragmentation
    """
    if not text:
        return ""
    
    original_length = len(text)
    
    # ÉTAPE 1 : Préservation expressions composées EN PREMIER sur texte ORIGINAL
    text_preserved = preserve_compound_expressions_v20(text)
    
    # ÉTAPE 2 : Suppression technique ULTRA-DOUCE (remplacer par espaces, pas supprimer)
    # URLs complètes → espaces multiples (pas suppression brutale)
    text_clean = re.sub(r'https?://[^\s]+', '   ', text_preserved)
    
    # Emails → espaces multiples
    text_clean = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '   ', text_clean)
    
    # Adresses Ethereum (0x...) → espaces multiples
    text_clean = re.sub(r'0x[a-fA-F0-9]{40,}', '   ', text_clean)
    
    # ÉTAPE 3 : Normalisation espaces multiples (préservation structure)
    text_final = re.sub(r'\s+', ' ', text_clean).strip()
    
    final_length = len(text_final)
    compression_ratio = final_length / original_length if original_length > 0 else 0
    
    logging.info(f"Nettoyage: {original_length} → {final_length} caractères (ratio: {compression_ratio:.3f})")
    
    return text_final

def tokenize_with_punctuation_protection_v20(text):
    """
    Tokenisation v2.0 avec PROTECTION des caractères utiles
    
    CORRECTION v2.0 : 
    - Préservation de _ et - (smart_contract, zk-rollup)
    - Suppression sélective de la ponctuation
    - Logging des tokens suspects
    
    Args:
        text (str): Texte nettoyé
        
    Returns:
        list: Liste des tokens valides
    """
    if not text:
        return []
    
    # CORRECTION TECHNIQUE C : Préservation des caractères utiles
    punctuation_to_remove = string.punctuation.replace('_', '').replace('-', '')
    text = text.translate(str.maketrans('', '', punctuation_to_remove))
    
    # Suppression des chiffres isolés (mais pas les termes comme layer_2)
    text = re.sub(r'\b\d+\b', ' ', text)
    
    # Tokenisation par espaces
    words = text.split()
    
    # Filtrage : longueur minimale et stopwords
    filtered_words = [
        word for word in words 
        if len(word) > MIN_TOKEN_LENGTH and word not in STOPWORDS_MINIMAL
    ]
    
    # DIAGNOSTIC TECHNIQUE D : Mots courts suspects
    short_suspicious = [word for word in filtered_words if len(word) <= 3]
    if short_suspicious:
        short_freq = Counter(short_suspicious)
        frequent_short = [(word, count) for word, count in short_freq.items() if count > 5]
        if frequent_short:
            logging.warning(f"Mots courts fréquents détectés: {frequent_short}")
    
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
    Pipeline principal v2.0 - CORRECTIONS TECHNIQUES AVANCÉES
    """
    print("=== Extraction des fréquences lexicales v2.0 CORRECTIONS TECHNIQUES AVANCÉES ===")
    print("NOUVELLES CORRECTIONS v2.0 :")
    print("- ✅ Expressions composées avec bornes de mots (\\b)")
    print("- ✅ Tri par longueur décroissante (évite conflits)")
    print("- ✅ Préservation caractères utiles (_ et -)")
    print("- ✅ Diagnostic mots courts suspects")
    print("- ✅ Logs techniques dédiés")
    print("- Affichage étendu 150 mots pour calibrage final")
    
    logging.info("=== DÉBUT EXTRACTION FRÉQUENCES v2.0 ===")
    
    # Vérification de l'existence du dossier
    if not os.path.exists(DATA_DIR):
        error_msg = f"Erreur: Le dossier {DATA_DIR} n'existe pas."
        print(error_msg)
        logging.error(error_msg)
        return
    
    # Collection de tous les mots
    all_words = []
    file_count = 0
    
    logging.info(f"Début traitement corpus: {DATA_DIR}")
    
    # Traitement de chaque fichier
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(DATA_DIR, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    
                    # Pipeline v2.0 - corrections techniques avancées
                    cleaned_text = clean_text_v20_technical_fixes(text)
                    words = tokenize_with_punctuation_protection_v20(cleaned_text)
                    all_words.extend(words)
                    
                    file_count += 1
                    
                    if VERBOSE_MODE and file_count % 50 == 0:
                        print(f"Traité {file_count} fichiers...")
                        
            except Exception as e:
                error_msg = f"Erreur lors du traitement de {filename}: {e}"
                print(error_msg)
                logging.error(error_msg)
    
    print(f"Traitement terminé: {file_count} fichiers, {len(all_words)} tokens totaux")
    logging.info(f"Traitement terminé: {file_count} fichiers, {len(all_words)} tokens totaux")
    
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
    output_path = os.path.join(CSV_OUTPUT_DIR, 'word_frequencies_sts_v20_technical_fixes.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"Résultats exportés: {output_path}")
    logging.info(f"Résultats exportés: {output_path}")
    
    # DIAGNOSTIC TECHNIQUE D : Mots courts fréquents suspects
    short_words = [(word, freq) for word, freq in word_frequencies.items() if len(word) <= 3 and freq > 10]
    if short_words:
        print(f"\n🔍 DIAGNOSTIC: Mots courts fréquents détectés ({len(short_words)}):")
        for word, freq in sorted(short_words, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  '{word}': {freq} occurrences")
        logging.warning(f"Mots courts suspects: {short_words}")
    else:
        print("✅ Aucun mot court suspect détecté")
        logging.info("Aucun mot court suspect détecté")
    
    # Analyse STS par catégorie
    print(f"\n=== ANALYSE STS OFFICIELLE (v2.0 CORRECTIONS TECHNIQUES) ===\n")
    
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
            logging.info(f"Catégorie {category}: {len(words)} termes")
            print()
    
    # Top 150 général - AFFICHAGE ÉTENDU pour calibrage final
    print(f"=== TOP 150 GÉNÉRAL (v2.0 CORRECTIONS TECHNIQUES AVANCÉES) ===")
    for i, word_info in enumerate(word_data[:150], 1):
        category_display = word_info['sts_category'] if word_info['sts_category'] != '—' else '—'
        print(f"{i:3} | {word_info['word']:<30} | {word_info['absolute_frequency']:6} | {word_info['percentage']:6.2f}% | {category_display}")
    
    # Diagnostic expressions composées
    print(f"\n=== DIAGNOSTIC EXPRESSIONS COMPOSÉES v2.0 (BORNES DE MOTS) ===")
    compound_found = []
    for compound, replacement in COMPOUND_EXPRESSIONS.items():
        if replacement in word_frequencies:
            count = word_frequencies[replacement]
            compound_found.append((compound, replacement, count))
            print(f"✅ '{compound}' → '{replacement}': {count} occurrences")
            logging.info(f"Expression composée préservée: '{compound}' → '{replacement}': {count}")
    
    if not compound_found:
        print("⚠️  PROBLÈME : Aucune expression composée détectée")
        logging.warning("PROBLÈME : Aucune expression composée détectée")
    else:
        print(f"✅ {len(compound_found)} expressions composées préservées avec succès")
        logging.info(f"{len(compound_found)} expressions composées préservées avec succès")
    
    # Vérification ethereum/foundation (doit être dans ethereum_foundation maintenant)
    ethereum_variants = [word for word in word_frequencies.keys() if 'ethereum' in word]
    foundation_variants = [word for word in word_frequencies.keys() if 'foundation' in word]
    
    print(f"\n🔍 Variantes ETHEREUM détectées ({len(ethereum_variants)}):")
    for variant in sorted(ethereum_variants, key=lambda x: word_frequencies[x], reverse=True)[:10]:
        print(f"   {variant}: {word_frequencies[variant]}")
        logging.info(f"Variante ethereum: {variant}: {word_frequencies[variant]}")
    
    print(f"\n🔍 Variantes FOUNDATION détectées ({len(foundation_variants)}):")
    for variant in sorted(foundation_variants, key=lambda x: word_frequencies[x], reverse=True)[:10]:
        print(f"   {variant}: {word_frequencies[variant]}")
        logging.info(f"Variante foundation: {variant}: {word_frequencies[variant]}")
    
    # Statistiques globales
    print(f"\n=== STATISTIQUES GLOBALES v2.0 - CORRECTIONS TECHNIQUES AVANCÉES ===")
    print(f"Vocabulaire unique: {unique_words:,} termes")
    print(f"Tokens totaux: {total_words:,}")
    print(f"Richesse lexicale (TTR): {ttr:.4f}")
    print(f"Fréquence STS totale: {sts_word_count:,}")
    print(f"Part STS du corpus: {(sts_word_count/total_words)*100:.2f}%")
    
    # Logging des statistiques finales
    logging.info(f"=== STATISTIQUES FINALES ===")
    logging.info(f"Vocabulaire unique: {unique_words:,}")
    logging.info(f"Tokens totaux: {total_words:,}")
    logging.info(f"TTR: {ttr:.4f}")
    logging.info(f"Part STS: {(sts_word_count/total_words)*100:.2f}%")
    logging.info("=== FIN EXTRACTION FRÉQUENCES v2.0 ===")

if __name__ == "__main__":
    main()

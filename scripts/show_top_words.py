
"""
Affichage du Top 50 des mots les plus fréquents avec statistiques complètes
Ethereum Foundation Discursive Analysis
"""

import pandas as pd
import os
import sys
sys.path.append('.')
from config import CSV_OUTPUT_DIR

def show_top_50_words():
    """
    Affiche les 50 mots les plus fréquents avec leurs statistiques
    """
    # Chemin du fichier des fréquences
    input_file = os.path.join(CSV_OUTPUT_DIR, 'word_frequencies_sts.csv')
    
    if not os.path.exists(input_file):
        print(f"❌ Fichier {input_file} non trouvé.")
        print("Veuillez d'abord exécuter l'extraction des fréquences.")
        return
    
    # Lecture des données
    df = pd.read_csv(input_file)
    
    # Calcul des statistiques générales
    total_tokens = df['frequency'].sum()
    unique_words = len(df)
    ttr = unique_words / total_tokens  # Type-Token Ratio
    
    print("=" * 80)
    print("📊 TOP 50 DES MOTS LES PLUS FRÉQUENTS - ANALYSE STS")
    print("=" * 80)
    print(f"Corpus analysé : {total_tokens:,} tokens totaux")
    print(f"Vocabulaire unique : {unique_words:,} termes")
    print(f"Richesse lexicale (TTR) : {ttr:.4f}")
    print()
    
    # Top 50 avec statistiques détaillées
    top_50 = df.head(50)
    
    print("RANG | TERME                    | FRÉQ.  | % CORPUS | CATÉGORIE STS")
    print("-" * 80)
    
    for i, row in top_50.iterrows():
        rang = i + 1
        terme = row['word']
        freq = row['frequency']
        pct = row['relative_frequency'] * 100
        categorie = row['sts_category'] if row['sts_category'] != 'uncategorized' else '—'
        
        # Formatage pour alignement
        terme_fmt = f"{terme:<24}"
        freq_fmt = f"{freq:>6,}"
        pct_fmt = f"{pct:>6.2f}%"
        cat_fmt = f"{categorie:<20}"
        
        print(f"{rang:>4} | {terme_fmt} | {freq_fmt} | {pct_fmt} | {cat_fmt}")
    
    print("-" * 80)
    
    # Analyse par catégorie STS
    print("\n🎯 RÉPARTITION PAR CATÉGORIE STS (Top 50)")
    print("-" * 50)
    
    sts_stats = top_50[top_50['sts_category'] != 'uncategorized']['sts_category'].value_counts()
    
    for categorie, count in sts_stats.items():
        pct_cat = (count / 50) * 100
        print(f"{categorie:<25} : {count:>2} termes ({pct_cat:>5.1f}%)")
    
    uncategorized = len(top_50[top_50['sts_category'] == 'uncategorized'])
    if uncategorized > 0:
        pct_uncat = (uncategorized / 50) * 100
        print(f"{'Non catégorisé':<25} : {uncategorized:>2} termes ({pct_uncat:>5.1f}%)")
    
    print("=" * 80)
    
    return top_50

if __name__ == "__main__":
    show_top_50_words()

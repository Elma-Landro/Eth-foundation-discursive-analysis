
"""
Configuration centralisée pour le pipeline d'analyse discursive
Ethereum Foundation Blog Analysis v1.1

Auteur: Elma Landro
Date: 2025
Objectif: Centraliser tous les paramètres modifiables pour faciliter 
         l'exploration méthodologique et maintenir la cohérence.
"""

import os

# === CHEMINS ET DOSSIERS ===
DATA_DIR = "./data/corpus_txt"
OUTPUT_DIR = "./outputs"
INDIVIDUAL_ARTICLES_DIR = "./data/corpus_raw/individual_articles"

# Création automatique des dossiers de sortie
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === PARAMÈTRES DE NETTOYAGE TEXTUEL ===

# Stopwords minimaux pour préserver le vocabulaire indigène
# Approche STS : conservation des termes techniques et conceptuels
STOPWORDS_MINIMAL = {
    'the', 'and', 'of', 'to', 'in', 'for', 'is', 'on', 'that', 'with', 'as',
    'by', 'it', 'are', 'at', 'from', 'an', 'be', 'or', 'we', 'can',
    'have', 'has', 'our', 'also', 'which', 'their', 'will', 'all',
    'but', 'was', 'they', 'these', 'may', 'you', 'been', 'its',
    'if', 'do', 'does', 'did', 'because', 'however', 'therefore', 'thus',
    'when', 'then', 'now', 'always', 'never', 'this', 'a',
    'very', 'most', 'some', 'many', 'such', 'would', 'could', 'should'
}

# Longueur minimale des tokens (pour éliminer les artéfacts)
MIN_TOKEN_LENGTH = 2

# === PARAMÈTRES DE COOCCURRENCES ===

# Taille de la fenêtre glissante pour capturer les relations contextuelles
# Justification : 5 mots permettent de capturer les relations locales sans trop de bruit
COOCCURRENCE_WINDOW_SIZE = 5

# Seuil minimal de fréquence pour les cooccurrences (filtrage du bruit)
COOCCURRENCE_MIN_FREQUENCY = 2

# === PARAMÈTRES DE VISUALISATION ===

# Nombre de termes les plus fréquents à afficher
TOP_WORDS_DISPLAY = 30

# Seuil pour le réseau lexical (élimination des liens faibles)
NETWORK_THRESHOLD = 5

# Paramètres pour le nuage de mots
WORDCLOUD_WIDTH = 800
WORDCLOUD_HEIGHT = 400
WORDCLOUD_MAX_WORDS = 100

# === PARAMÈTRES AVANCÉS ===

# Préservation des termes techniques crypto (nouveauté v1.1)
PRESERVE_CRYPTO_TERMS = True

# Liste des termes techniques à préserver absolument
CRYPTO_TECHNICAL_TERMS = {
    'web3', 'eip', 'layer2', 'defi', 'nft', 'dao', 'dapp', 'evm', 'pos', 'pow',
    'eth2', 'beacon', 'shard', 'rollup', 'zk', 'erc20', 'erc721', 'erc1155'
}

# === LOGGING ET DEBUGGING ===
VERBOSE_MODE = True
LOG_PROCESSING_STEPS = True

# === MÉTADONNÉES DE VERSION ===
VERSION = "1.1"
LAST_UPDATE = "2025-01-XX"
METHODOLOGICAL_NOTES = """
Version 1.1 - Correctifs critiques :
- Correction de la regex email (échappement \b)
- Préservation des termes techniques crypto (EIP, web3, etc.)
- Centralisation des paramètres pour reproductibilité
- Documentation précise de chaque choix méthodologique
"""

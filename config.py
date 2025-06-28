
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

# CORPUS SOURCES (non modifiables - reproductibilité)
CORPUS_TXT_DIR = "./data/corpus_txt"           # Corpus principal nettoyé
CORPUS_RAW_DIR = "./data/corpus_raw"           # Données brutes d'extraction
INDIVIDUAL_ARTICLES_DIR = "./data/corpus_raw/individual_articles"

# OUTPUTS GÉNÉRÉS (résultats d'analyse)
OUTPUT_DIR = "./outputs"                       # Dossier principal des résultats
CSV_OUTPUT_DIR = "./outputs/csv"               # Fichiers CSV (fréquences, cooccurrences)
VISUALIZATIONS_DIR = "./outputs/visualizations" # Graphiques et réseaux
NETWORKS_DIR = "./outputs/networks"            # Fichiers de réseaux (GraphML, etc.)

# Création automatique de la structure d'outputs
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)
os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)
os.makedirs(NETWORKS_DIR, exist_ok=True)

# Alias pour compatibilité (à utiliser CORPUS_TXT_DIR à l'avenir)
DATA_DIR = CORPUS_TXT_DIR

# === PARAMÈTRES DE NETTOYAGE TEXTUEL ===

# Stopwords enrichie pour analyse STS précise
STOPWORDS_ENRICHED = {
    # Articles, pronoms, auxiliaires
    'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
    
    # Prépositions et conjonctions
    'of', 'to', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'among', 'under', 'over', 'within', 'without',
    'and', 'or', 'but', 'nor', 'so', 'yet', 'because', 'since', 'although', 'though', 'while', 'whereas',
    'if', 'unless', 'until', 'when', 'where', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose',
    
    # Adverbes de liaison et marqueurs discursifs (critiques pour STS)
    'also', 'however', 'therefore', 'thus', 'hence', 'consequently', 'moreover', 'furthermore', 'nevertheless',
    'nonetheless', 'meanwhile', 'likewise', 'similarly', 'conversely', 'instead', 'otherwise', 'accordingly',
    'indeed', 'certainly', 'obviously', 'clearly', 'particularly', 'especially', 'specifically', 'generally',
    
    # Quantificateurs et intensifieurs (bruit lexical)
    'all', 'some', 'any', 'many', 'much', 'more', 'most', 'less', 'least', 'few', 'several', 'both',
    'each', 'every', 'either', 'neither', 'one', 'two', 'three', 'first', 'second', 'third', 'last',
    'very', 'quite', 'rather', 'pretty', 'fairly', 'extremely', 'highly', 'really', 'truly', 'actually',
    
    # Connecteurs temporels
    'now', 'then', 'today', 'tomorrow', 'yesterday', 'always', 'never', 'often', 'sometimes', 'usually',
    'frequently', 'rarely', 'seldom', 'once', 'twice', 'again', 'still', 'yet', 'already', 'soon',
    
    # Verbes génériques (peu informatifs pour STS)
    'get', 'got', 'getting', 'give', 'given', 'giving', 'take', 'taken', 'taking', 'make', 'made', 'making',
    'come', 'came', 'coming', 'go', 'went', 'going', 'see', 'saw', 'seen', 'seeing', 'know', 'knew', 'known',
    'think', 'thought', 'thinking', 'say', 'said', 'saying', 'tell', 'told', 'telling', 'become', 'became',
    
    # Mots de politesse et formules (présents dans blogs)
    'please', 'thank', 'thanks', 'welcome', 'hello', 'hi', 'bye', 'goodbye', 'regards', 'sincerely'
}

# Alias pour compatibilité
STOPWORDS_MINIMAL = STOPWORDS_ENRICHED

# === LEXIQUE STS POUR CODAGE AXIAL ===

# Catégories sociotechniques émergentes identifiées dans le corpus Ethereum
STS_LEXICON = {
    'governance': {
        'dao', 'governance', 'vote', 'voting', 'proposal', 'community', 'foundation', 'board', 'decision',
        'consensus', 'stakeholder', 'participant', 'member', 'contributor', 'committee', 'council',
        'decentralized', 'centralized', 'autonomy', 'autonomous', 'democratic', 'participation'
    },
    
    'technical_infrastructure': {
        'blockchain', 'block', 'chain', 'network', 'protocol', 'node', 'client', 'server', 'peer',
        'consensus', 'mining', 'miner', 'validator', 'staking', 'proof', 'algorithm', 'hash', 'merkle',
        'transaction', 'tx', 'gas', 'fee', 'throughput', 'latency', 'scalability', 'performance'
    },
    
    'development_practices': {
        'development', 'developer', 'coding', 'programming', 'software', 'code', 'implementation',
        'deployment', 'testing', 'debugging', 'optimization', 'upgrade', 'update', 'version',
        'github', 'repository', 'commit', 'pull', 'request', 'issue', 'bug', 'feature', 'api'
    },
    
    'security_trust': {
        'security', 'secure', 'vulnerability', 'attack', 'threat', 'risk', 'audit', 'review',
        'cryptography', 'encryption', 'signature', 'verification', 'authentication', 'authorization',
        'trust', 'trustless', 'immutable', 'tamper', 'resistant', 'robust', 'safe', 'safety'
    },
    
    'economic_models': {
        'economic', 'economy', 'token', 'eth', 'ether', 'currency', 'value', 'price', 'market',
        'trading', 'exchange', 'liquidity', 'supply', 'demand', 'inflation', 'deflation',
        'incentive', 'reward', 'penalty', 'cost', 'benefit', 'profit', 'investment', 'funding'
    },
    
    'social_adoption': {
        'adoption', 'user', 'community', 'ecosystem', 'platform', 'application', 'dapp', 'service',
        'interface', 'experience', 'usability', 'accessibility', 'education', 'awareness',
        'mainstream', 'enterprise', 'business', 'industry', 'institution', 'regulation', 'compliance'
    }
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

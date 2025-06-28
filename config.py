
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

# Stopwords enrichie pour analyse STS précise - VERSION CORRIGÉE
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
    
    # Quantificateurs et intensifieurs (bruit lexical) - AJOUTS CRITIQUES
    'all', 'some', 'any', 'many', 'much', 'more', 'most', 'less', 'least', 'few', 'several', 'both',
    'each', 'every', 'either', 'neither', 'one', 'two', 'three', 'first', 'second', 'third', 'last',
    'very', 'quite', 'rather', 'pretty', 'fairly', 'extremely', 'highly', 'really', 'truly', 'actually',
    'only', 'such', 'not', 'new', 'other', 'there', 'like', 'than', 'way', 'well', 'same', 'just', 'set', 'non',
    'even', 'out', 'use', 'need', 'support', 'team', 'work', 'time', 'data', 'number', 'users', 'using',
    
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

# === LEXIQUE STS POUR CODAGE AXIAL - GRILLE STRUCTURÉE ===

# 🧭 Catégories STS (analytico-théoriques)
STS_LEXICON = {
    'protocolaire': {
        'eip', 'eips', 'hardfork', 'fork', 'consensus', 'upgrade', 'protocol', 'specification', 'standard',
        'improvement', 'proposal', 'ethereum', 'beacon', 'merge', 'pos', 'pow', 'casper', 'finality',
        'epoch', 'slot', 'validator', 'attestation', 'committee', 'sync', 'checkpoint'
    },
    
    'infrastructurel': {
        'network', 'scaling', 'layer', 'rollup', 'rollups', 'optimistic', 'arbitrum', 'optimism',
        'zk', 'zkrollup', 'polygon', 'shard', 'sharding', 'shards', 'execution', 'consensus',
        'beacon', 'chain', 'block', 'blockchain', 'node', 'nodes', 'client', 'clients', 'peer',
        'infrastructure', 'architecture', 'latency', 'throughput', 'performance', 'capacity'
    },
    
    'gouvernance': {
        'staking', 'stake', 'staker', 'slashing', 'validator', 'validators', 'delegate', 'delegation',
        'governance', 'dao', 'vote', 'voting', 'proposal', 'decision', 'foundation', 'board',
        'community', 'coordination', 'consensus', 'stakeholder', 'participant', 'member',
        'contributor', 'committee', 'council', 'democratic', 'participation', 'funding'
    },
    
    'sécurité': {
        'security', 'vulnerability', 'audit', 'bug', 'exploit', 'attack', 'threat', 'risk',
        'cryptography', 'encryption', 'signature', 'verification', 'proof', 'zk', 'zero',
        'knowledge', 'formal', 'verification', 'safety', 'secure', 'trust', 'trustless',
        'immutable', 'tamper', 'resistant', 'robust', 'authentication', 'authorization'
    },
    
    'usages': {
        'wallet', 'wallets', 'interface', 'user', 'experience', 'usability', 'accessibility',
        'dapp', 'dapps', 'application', 'applications', 'service', 'platform', 'adoption',
        'mainstream', 'enterprise', 'business', 'end', 'frontend', 'backend', 'mobile',
        'web', 'browser', 'metamask', 'etherscan', 'tools', 'tooling'
    },
    
    'recherche': {
        'research', 'paper', 'academic', 'study', 'analysis', 'theory', 'theoretical',
        'model', 'modeling', 'simulation', 'experiment', 'formal', 'mathematics',
        'cryptographic', 'algorithm', 'optimization', 'design', 'specification',
        'whitepaper', 'yellowpaper', 'documentation', 'technical', 'science'
    },
    
    'développement': {
        'solidity', 'vyper', 'foundry', 'hardhat', 'truffle', 'remix', 'compiler',
        'development', 'developer', 'coding', 'programming', 'software', 'code',
        'implementation', 'deployment', 'testing', 'debugging', 'github', 'repository',
        'commit', 'pull', 'request', 'issue', 'feature', 'api', 'sdk', 'library',
        'framework', 'toolchain', 'ide', 'environment'
    },
    
    'defi_finance': {
        'defi', 'amm', 'mev', 'liquidity', 'flashloan', 'yield', 'farming', 'swap',
        'uniswap', 'compound', 'aave', 'maker', 'dai', 'usdc', 'token', 'tokens',
        'erc20', 'erc721', 'nft', 'nfts', 'market', 'trading', 'exchange', 'price',
        'value', 'economic', 'economy', 'financial', 'monetary', 'currency', 'eth',
        'ether', 'gas', 'fee', 'fees', 'cost', 'incentive', 'reward'
    },
    
    'discours_vision': {
        'decentralized', 'decentralization', 'centralized', 'trustless', 'permissionless',
        'censorship', 'resistant', 'open', 'transparent', 'immutable', 'autonomous',
        'sovereignty', 'freedom', 'innovation', 'disruption', 'transformation',
        'future', 'vision', 'philosophy', 'values', 'principles', 'ethos', 'mission',
        'scalable', 'sustainable', 'inclusive', 'accessible', 'global', 'universal'
    }
}

# 🏷️ Catégories indigènes EF (provenant des métadonnées)
EF_INDIGENOUS_CATEGORIES = {
    'research_development': {
        'research', 'development', 'experimental', 'prototype', 'proof', 'concept',
        'design', 'specification', 'academic', 'paper', 'study', 'analysis'
    },
    
    'updates_upgrades': {
        'update', 'upgrade', 'fork', 'hardfork', 'merge', 'transition', 'migration',
        'announcement', 'release', 'version', 'changelog', 'improvement'
    },
    
    'events_community': {
        'devcon', 'conference', 'hackathon', 'meetup', 'event', 'community',
        'workshop', 'talk', 'presentation', 'gathering', 'summit'
    },
    
    'security': {
        'security', 'vulnerability', 'audit', 'bug', 'bounty', 'exploit', 'patch',
        'fix', 'advisory', 'disclosure', 'responsible'
    },
    
    'staking_merge': {
        'staking', 'stake', 'validator', 'beacon', 'merge', 'pos', 'proof', 'stake',
        'transition', 'consensus', 'finality', 'slashing'
    },
    
    'layer2_scaling': {
        'layer', 'scaling', 'rollup', 'rollups', 'optimistic', 'zk', 'arbitrum',
        'optimism', 'polygon', 'shard', 'sharding', 'throughput'
    },
    
    'wallet_ux': {
        'wallet', 'interface', 'user', 'experience', 'usability', 'mobile',
        'web', 'browser', 'frontend', 'design', 'accessibility'
    },
    
    'ecosystem_adoption': {
        'ecosystem', 'adoption', 'partnership', 'integration', 'enterprise',
        'business', 'industry', 'mainstream', 'education', 'outreach'
    },
    
    'governance_coordination': {
        'governance', 'coordination', 'foundation', 'grant', 'funding', 'team',
        'organization', 'decision', 'process', 'structure'
    },
    
    'media_philosophy': {
        'culture', 'philosophy', 'values', 'vision', 'mission', 'ethos',
        'decentralization', 'freedom', 'innovation', 'future'
    },
    
    'announcements': {
        'announcement', 'news', 'press', 'release', 'statement', 'official',
        'communication', 'update', 'information'
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

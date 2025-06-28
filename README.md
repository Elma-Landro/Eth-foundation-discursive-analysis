
# ETH Foundation Discursive Analysis - Version 1.1

## 🔄 Nouvelles fonctionnalités v1.1 (Correctifs critiques)

### Corrections techniques majeures
- **✅ Correction regex email** : Échappement `\b` corrigé dans les fonctions de nettoyage
- **✅ Préservation des termes techniques crypto** : Conservation de EIP, web3, layer2, etc.
- **✅ Configuration centralisée** : Nouveau fichier `config.py` pour la reproductibilité
- **✅ Documentation méthodologique renforcée** : Justification de chaque choix technique

### Améliorations méthodologiques
- **Approche STS préservée** : Nettoyage minimal pour conserver les catégories indigènes
- **Paramètres configurables** : Tous les seuils et paramètres modifiables via `config.py`
- **Robustesse technique** : Gestion d'erreurs améliorée et logging détaillé

---

## 📋 Vue d'ensemble du projet

Ce pipeline d'analyse discursive computationnelle permet l'extraction et l'analyse lexicale du corpus des blogposts de la Fondation Ethereum (567 articles, 2013-2025). 

**Approche méthodologique** : Science and Technology Studies (STS) avec préservation du vocabulaire indigène pour faciliter l'induction de catégories émergentes (théorie ancrée).

## 🗂️ Structure du projet

```
├── config.py                          # 🆕 Configuration centralisée v1.1
├── data/                               # 📚 CORPUS SOURCES (non modifiables)
│   ├── corpus_raw/                     # Données brutes d'extraction
│   │   ├── individual_articles/        # 567 articles individuels
│   │   ├── ethereum_blog_articles.csv  # Métadonnées
│   │   └── ethereum_blog_complete.json # Export complet
│   └── corpus_txt/                     # 567 fichiers texte nettoyés
├── scripts/                            # 🛠️ MODULES D'ANALYSE
│   ├── extract_word_frequencies.py     # 🔄 Module fréquences (v1.1)
│   ├── compute_cooccurrences.py        # 🔄 Module cooccurrences (v1.1)
│   ├── visualize_frequencies.py        # Module visualisation fréquences
│   ├── visualize_lexical_network.py    # Module réseau lexical
│   └── module_segmentation_corpus.py   # Utilitaire segmentation thématique
├── outputs/                            # 📊 RÉSULTATS D'ANALYSE
│   ├── csv/                            # Données brutes (CSV)
│   ├── visualizations/                 # Graphiques et nuages de mots
│   └── networks/                       # Fichiers réseaux (GraphML)
├── notebooks/
│   └── ETH_Foundation_Master_Pipeline.ipynb  # Notebook interactif
└── corpus_documentation/               # Documentation d'extraction
```

## ⚙️ Configuration centralisée (Nouveauté v1.1)

Le fichier `config.py` centralise tous les paramètres modifiables :

```python
# Paramètres de nettoyage
PRESERVE_CRYPTO_TERMS = True  # Conservation des termes EIP, web3, etc.
MIN_TOKEN_LENGTH = 2          # Longueur minimale des tokens

# Paramètres de cooccurrences
COOCCURRENCE_WINDOW_SIZE = 5  # Taille fenêtre glissante
COOCCURRENCE_MIN_FREQUENCY = 2  # Seuil de filtrage

# Paramètres de visualisation
TOP_WORDS_DISPLAY = 30        # Nombre de termes affichés
NETWORK_THRESHOLD = 5         # Seuil réseau lexical
```

## 🚀 Installation et exécution

### Prérequis
```bash
pip install pandas matplotlib wordcloud networkx
```

### Exécution du pipeline complet

**Option 1 : Via Jupyter Notebook (recommandé)**
```bash
jupyter notebook notebooks/ETH_Foundation_Master_Pipeline.ipynb
```

**Option 2 : Modules individuels**
```bash
# 1. Extraction des fréquences
python scripts/extract_word_frequencies.py

# 2. Calcul des cooccurrences
python scripts/compute_cooccurrences.py

# 3. Visualisations
python scripts/visualize_frequencies.py
python scripts/visualize_lexical_network.py
```

## 📊 Outputs générés

### Données structurées
- `word_frequencies.csv` : Fréquences absolues et relatives
- `cooccurrence_pairs.csv` : Paires de cooccurrences avec comptages

### Visualisations
- `top_words_bar_chart.png` : Top 30 des termes les plus fréquents
- `wordcloud.png` : Nuage de mots global
- `lexical_network.png` : Réseau de cooccurrences
- `lexical_network.graphml` : Réseau exportable vers Gephi

## 🔬 Méthodologie détaillée

### 1. Nettoyage textuel (Approche minimaliste STS)
```python
def clean_text_advanced(text):
    # Suppression URLs, emails, adresses Ethereum
    # PRÉSERVATION des termes techniques crypto (EIP, web3, layer2...)
    # Suppression chiffres isolés MAIS conservation termes composés
```

**Justification** : Nettoyage minimal pour préserver le vocabulaire indigène et permettre l'induction de catégories émergentes.

### 2. Cooccurrences par fenêtre glissante
- **Fenêtre** : 5 mots (configurable)
- **Algorithme** : `itertools.combinations` sur chaque fenêtre
- **Normalisation** : Tri alphabétique des paires pour éviter (A,B) vs (B,A)

### 3. Visualisations réseau
- **Filtrage** : Seuil minimal de 5 cooccurrences (configurable)
- **Layout** : Algorithme de ressort (`spring_layout`)
- **Export** : Format GraphML pour analyses Gephi

## 📈 Statistiques du corpus

- **Articles** : 567 blogposts (2013-2025)
- **Tokens uniques** : ~15,000-20,000 (après nettoyage)
- **Cooccurrences** : ~50,000-100,000 paires (avant filtrage)
- **Richesse lexicale (TTR)** : ~0.15-0.20

## 🔍 Correctifs critiques v1.2 STS

### Problème 1 : Stopwords insuffisantes → Analyse STS polluée
**Avant** : Liste minimale → "more", "not", "his" dans top 10
**Après** : Stopwords enrichie (150+ termes) + marqueurs discursifs
**Impact** : Émergence des termes STS réellement structurants

### Problème 2 : Troncature "thereum" au lieu d'"ethereum"  
**Avant** : Nettoyage destructif sur termes critiques
**Après** : Sauvegarde préventive des termes STS + crypto avant ponctuation
**Impact** : Préservation intégrale du vocabulaire sociotechnique

### Problème 3 : Absence de catégorisation STS
**Avant** : Fréquences brutes sans orientation analytique
**Après** : Lexique STS intégré (6 catégories) + export enrichi
**Impact** : Codage axial direct, prêt pour théorie ancrée

### Nouveauté v1.2 : Pipeline STS complet
- **Lexique sociotechnique** : governance, technical_infrastructure, security_trust, etc.
- **Export enrichi** : `word_frequencies_sts.csv` avec catégories
- **Affichage orienté** : Top termes par domaine STS pour codage axial

## 🎯 Vers la théorie ancrée

Ce pipeline v1.1 constitue la base robuste pour :
- **Clustering thématique** : Regroupement des cooccurrences
- **Détection de n-grammes** : Expressions composées
- **Évolution temporelle** : Analyse diachronique du vocabulaire
- **Induction de catégories** : Émergence de thématiques indigènes

## 📚 Documentation complète

- `Methodological_Appendix_v1_clean.md` : Justifications théoriques STS
- `Execution_Guide_v1.md` : Guide d'exécution pas-à-pas
- `corpus_documentation/` : Documentation d'extraction du corpus

## 📞 Support et contributions

Pour questions méthodologiques ou techniques :
- Consulter d'abord `Methodological_Appendix_v1_clean.md`
- Vérifier les paramètres dans `config.py`
- Examiner les logs de traitement pour debugging

---

**Version** : 1.1  
**Dernière mise à jour** : 2025-01-XX  
**Approche** : Science and Technology Studies (STS) + Théorie ancrée  
**Licence** : MIT

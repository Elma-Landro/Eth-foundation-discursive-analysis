
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
├── data/
│   ├── corpus_raw/                     # Données brutes d'extraction
│   └── corpus_txt/                     # 567 fichiers texte individuels
├── scripts/
│   ├── extract_word_frequencies.py     # 🔄 Module fréquences (v1.1)
│   ├── compute_cooccurrences.py        # 🔄 Module cooccurrences (v1.1)
│   ├── visualize_frequencies.py        # Module visualisation fréquences
│   ├── visualize_lexical_network.py    # Module réseau lexical
│   └── module_segmentation_corpus.py   # Utilitaire segmentation thématique
├── outputs/                            # Résultats CSV et visualisations
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

## 🔍 Correctifs critiques v1.1

### Problème 1 : Regex email défaillante
**Avant** : `r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'`
**Après** : `r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'`
**Impact** : Suppression correcte des emails, réduction du bruit lexical

### Problème 2 : Perte des termes techniques
**Avant** : Suppression aveugle avec `re.sub(r'\d+', '', text)`
**Après** : Sauvegarde temporaire des termes crypto + restauration
**Impact** : Préservation de EIP1559, web3, layer2, etc.

### Problème 3 : Paramètres dispersés
**Avant** : Valeurs codées en dur dans chaque script
**Après** : Centralisation dans `config.py`
**Impact** : Reproductibilité et exploration paramétrique facilités

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

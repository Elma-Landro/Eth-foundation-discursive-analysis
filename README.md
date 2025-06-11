
# ETH Foundation Discursive Analysis

Ce projet permet de réaliser une extraction lexicale de base sur le corpus des blogposts de la Fondation Ethereum.

## Structure du projet

- `data/` : mettre ici les 657 fichiers texte (.txt)
- `scripts/` : contient le script Python d'extraction
- `outputs/` : reçoit les fichiers de résultats (CSV)

## Exécution du script

Installer les dépendances (voir requirements.txt), puis lancer :

```bash
python scripts/extract_word_frequencies.py
```

Le résultat se trouve dans `outputs/word_frequencies.csv`.

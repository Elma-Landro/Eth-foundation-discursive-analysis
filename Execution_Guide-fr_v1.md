
# Guide d’exécution locale — Ethereum Foundation Discursive Analysis

## Objectif

Ce guide fournit les instructions pas à pas pour exécuter le pipeline d’analyse lexicale et discursive sur le corpus de la Fondation Ethereum, depuis votre machine locale.

---

## 1️⃣ Cloner le dépôt GitHub

Ouvrir un terminal et exécuter la commande suivante pour récupérer le repository en local :

```bash
git clone https://github.com/Elma-Landro/Eth-foundation-discursive-analysis.git
```

Cela créera un dossier local contenant tous les fichiers du projet.

---

## 2️⃣ Se positionner dans le répertoire du projet

Naviguer dans le dossier cloné :

```bash
cd Eth-foundation-discursive-analysis
```

---

## 3️⃣ Vérifier la présence des scripts

Vous pouvez lister les scripts présents avec :

```bash
ls scripts/
```

Vous devez y voir apparaître notamment : `corpus_file_counter.py` ainsi que les autres scripts d’analyse.

---

## 4️⃣ Exécuter les scripts Python

### Remarque importante :

Sur la plupart des systèmes modernes (Ubuntu, Debian), la commande `python` pointe désormais vers `python3`.  
Nous utiliserons donc systématiquement `python3` dans les commandes suivantes.

---

### Exemple d’exécution du script de vérification du corpus :

```bash
python3 scripts/corpus_file_counter.py
```

Cela retournera le nombre de fichiers `.txt` détectés dans le répertoire de travail :

```
Total .txt files found in './data/corpus_raw/individual_articles/': 567
```

---

## 5️⃣ Exécution des autres modules d’analyse

De la même manière, vous pourrez exécuter tous les autres scripts Python de votre dossier `scripts/` avec :

```bash
python3 scripts/nom_du_script.py
```

ou piloter l'ensemble de votre pipeline via le Master Notebook situé dans le dossier `notebooks/`.

---

## 6️⃣ Environnement Python et dépendances

Assurez-vous d’avoir installé les librairies nécessaires.  
Depuis la racine du projet, vous pouvez installer les dépendances en une seule commande (si vous avez `pip` disponible) :

```bash
pip3 install -r requirements.txt
```

---

## 7️⃣ Mise à jour future du repository

Pour synchroniser votre copie locale avec les nouvelles versions du repository distant :

```bash
git pull
```

---

## Remarque finale

Ce guide est conçu pour assurer la reproductibilité intégrale de l’analyse du corpus dans un cadre de recherche critique et rigoureux.

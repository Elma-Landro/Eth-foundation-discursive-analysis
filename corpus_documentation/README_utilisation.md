# Instructions d'utilisation pour débutants

## Fichiers fournis

Vous disposez maintenant de tous les éléments nécessaires pour extraire les publications du blog Ethereum Foundation :

### 1. Documentation complète
- **guide_extraction_ethereum.md** : Guide complet en format Markdown
- **guide_extraction_ethereum.pdf** : Même guide en format PDF pour impression/lecture
- **ethereum_blog_analysis.md** : Analyse détaillée de la structure du blog
- **extraction_strategy.md** : Stratégie technique détaillée

### 2. Script d'extraction prêt à l'emploi
- **ethereum_blog_extractor.py** : Script Python complet avec commentaires détaillés
- **evaluate_extraction_methods.py** : Script de validation des méthodes

## Comment procéder (étapes simples)

### Étape 1 : Préparation
1. Assurez-vous d'avoir Python 3 installé sur votre ordinateur
2. Ouvrez un terminal/invite de commande
3. Installez les dépendances nécessaires :
   ```bash
   pip install requests beautifulsoup4 pandas lxml tqdm python-dateutil
   ```

### Étape 2 : Téléchargement des fichiers
1. Téléchargez le fichier `ethereum_blog_extractor.py` depuis ce sandbox
2. Placez-le dans un dossier dédié sur votre ordinateur
3. Ouvrez un terminal dans ce dossier

### Étape 3 : Exécution
1. Lancez la commande :
   ```bash
   python3 ethereum_blog_extractor.py
   ```
2. Confirmez quand le script vous demande si vous voulez continuer
3. Attendez 20-35 minutes que l'extraction se termine
4. Les résultats seront dans le dossier `ethereum_blog_data/`

### Étape 4 : Vérification des résultats
Vous devriez obtenir :
- **ethereum_blog_complete.json** : Toutes les données (principal)
- **ethereum_blog_articles.csv** : Métadonnées pour Excel/analyses
- **individual_articles/** : 567 fichiers texte individuels
- **extraction_report.txt** : Rapport de l'extraction

## Support et dépannage

Si vous rencontrez des difficultés :
1. Vérifiez que toutes les dépendances sont installées
2. Assurez-vous d'avoir une connexion internet stable
3. Le script sauvegarde automatiquement tous les 50 articles
4. En cas d'interruption, relancez simplement le script

## Utilisation des données

Une fois l'extraction terminée, vous pourrez :
- Analyser les 567 articles couvrant 2013-2025
- Utiliser les fichiers CSV dans Excel pour des statistiques
- Importer le JSON dans des outils d'analyse textuelle
- Lire les articles individuels en format texte

Le corpus représente plus de 11 années d'évolution de l'écosystème Ethereum, soit environ 3 Mo de contenu textuel structuré.


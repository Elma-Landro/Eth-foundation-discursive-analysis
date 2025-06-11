#!/usr/bin/env python3
"""
SCRIPT D'EXTRACTION COMPLET - BLOG ETHEREUM FOUNDATION
Implémentation de la stratégie d'extraction optimale

Ce script est conçu pour être utilisé par des débutants en programmation.
Chaque étape est largement commentée et expliquée.

Utilisation :
    python3 ethereum_blog_extractor.py

Le script va :
1. Récupérer toutes les URLs d'articles depuis le sitemap
2. Extraire le contenu de chaque article
3. Nettoyer et structurer les données
4. Sauvegarder dans plusieurs formats (JSON, CSV, TXT)
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import re
import time
import os
from datetime import datetime
from urllib.parse import urljoin
import pandas as pd
from tqdm import tqdm
import logging

# Configuration du logging pour suivre le processus
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ethereum_extraction.log'),
        logging.StreamHandler()
    ]
)

class EthereumBlogExtractor:
    """
    Classe principale pour l'extraction du blog Ethereum Foundation
    
    Cette classe encapsule toute la logique d'extraction pour la rendre
    facilement utilisable et modifiable.
    """
    
    def __init__(self):
        """Initialisation de l'extracteur avec la configuration par défaut"""
        
        # URLs de base du site Ethereum
        self.base_url = "https://blog.ethereum.org"
        self.sitemap_url = "https://blog.ethereum.org/sitemap-0.xml"
        
        # Configuration pour être respectueux du serveur
        self.delay_between_requests = 1.0  # 1 seconde entre chaque requête
        self.max_retries = 3               # Nombre de tentatives en cas d'échec
        self.timeout = 30                  # Timeout par requête en secondes
        self.batch_size = 50               # Sauvegarde tous les 50 articles
        
        # Pattern pour identifier les URLs d'articles
        # Format attendu : /YYYY/MM/DD/slug-title
        self.article_pattern = re.compile(r'https://blog\.ethereum\.org/(\d{4})/(\d{2})/(\d{2})/(.+)')
        
        # Stockage des données extraites
        self.articles = []
        self.failed_urls = []
        
        # Métadonnées de l'extraction
        self.extraction_metadata = {
            'extraction_date': datetime.now().isoformat(),
            'total_articles_found': 0,
            'successfully_extracted': 0,
            'failed_extractions': 0,
            'source': self.base_url
        }
        
        logging.info("Extracteur Ethereum Blog initialisé")
    
    def get_article_urls_from_sitemap(self):
        """
        Étape 1 : Récupération de toutes les URLs d'articles depuis le sitemap
        
        Le sitemap est un fichier XML officiel qui liste toutes les pages du site.
        C'est la méthode la plus fiable pour obtenir une liste complète.
        
        Returns:
            list: Liste des URLs d'articles trouvées
        """
        logging.info("Récupération des URLs depuis le sitemap...")
        
        try:
            # Téléchargement du sitemap XML
            response = requests.get(self.sitemap_url, timeout=self.timeout)
            response.raise_for_status()  # Lève une exception si erreur HTTP
            
            # Parsing du XML avec BeautifulSoup
            soup = BeautifulSoup(response.content, 'xml')
            
            # Extraction de toutes les URLs
            urls = []
            for url_tag in soup.find_all('url'):
                loc_tag = url_tag.find('loc')
                if loc_tag:
                    url = loc_tag.text.strip()
                    
                    # Vérification que l'URL correspond au pattern d'un article
                    if self.article_pattern.match(url):
                        urls.append(url)
            
            # Tri chronologique (du plus ancien au plus récent)
            urls.sort()
            
            self.extraction_metadata['total_articles_found'] = len(urls)
            logging.info(f"✓ {len(urls)} URLs d'articles trouvées dans le sitemap")
            
            return urls
            
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du sitemap : {e}")
            return []
    
    def extract_article_content(self, url):
        """
        Étape 2 : Extraction du contenu d'un article individuel
        
        Pour chaque URL d'article, cette fonction :
        - Télécharge la page HTML
        - Extrait le titre, auteur, date, contenu
        - Nettoie et structure les données
        
        Args:
            url (str): URL de l'article à extraire
            
        Returns:
            dict: Données structurées de l'article ou None si échec
        """
        
        try:
            # Téléchargement de la page de l'article
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parsing HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction du titre principal (balise H1)
            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else "Titre non trouvé"
            
            # Extraction de l'auteur et de la date
            # Format attendu : "Posted by [Auteur] on [Date]"
            author = "Auteur non trouvé"
            publication_date = "Date non trouvée"
            
            # Recherche dans tout le texte de la page
            for text in soup.stripped_strings:
                if "Posted by" in text and " on " in text:
                    # Utilisation d'expressions régulières pour extraire auteur et date
                    author_match = re.search(r'Posted by (.+?) on', text)
                    date_match = re.search(r'on (.+)$', text)
                    
                    if author_match:
                        author = author_match.group(1).strip()
                    if date_match:
                        publication_date = date_match.group(1).strip()
                    break
            
            # Extraction de la catégorie (si disponible)
            category = "Non catégorisé"
            category_tags = soup.find_all(['span', 'div'], class_=re.compile(r'category|tag'))
            if category_tags:
                category = category_tags[0].get_text(strip=True)
            
            # Extraction du contenu principal
            # Tentative avec plusieurs sélecteurs possibles
            content_selectors = [
                'article',           # Balise article HTML5
                '.post-content',     # Classe CSS commune
                '.content',          # Classe CSS générique
                'main',              # Balise main HTML5
                '.entry-content'     # Autre classe CSS commune
            ]
            
            content = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Extraction du texte en préservant les paragraphes
                    content = content_elem.get_text(separator='\\n\\n', strip=True)
                    break
            
            # Si aucun sélecteur spécifique ne fonctionne, extraction de tout le texte
            if not content:
                content = soup.get_text(separator='\\n\\n', strip=True)
            
            # Nettoyage du contenu
            content = self.clean_content(content)
            
            # Extraction des métadonnées de l'URL
            url_match = self.article_pattern.match(url)
            year, month, day, slug = url_match.groups() if url_match else ("", "", "", "")
            
            # Construction de l'objet article structuré
            article_data = {
                'id': f"{year}-{month}-{day}-{slug}",
                'url': url,
                'title': title,
                'author': author,
                'publication_date': publication_date,
                'year': year,
                'month': month,
                'day': day,
                'slug': slug,
                'category': category,
                'content': content,
                'word_count': len(content.split()) if content else 0,
                'character_count': len(content) if content else 0,
                'extraction_metadata': {
                    'extracted_at': datetime.now().isoformat(),
                    'extraction_success': True,
                    'content_length': len(content) if content else 0
                }
            }
            
            return article_data
            
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction de {url} : {e}")
            return None
    
    def clean_content(self, content):
        """
        Nettoyage et normalisation du contenu textuel
        
        Args:
            content (str): Contenu brut extrait
            
        Returns:
            str: Contenu nettoyé
        """
        if not content:
            return ""
        
        # Suppression des espaces multiples et normalisation
        content = re.sub(r'\\s+', ' ', content)
        
        # Suppression des caractères de contrôle
        content = re.sub(r'[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F\\x7F]', '', content)
        
        # Normalisation des sauts de ligne
        content = re.sub(r'\\n\\n+', '\\n\\n', content)
        
        return content.strip()
    
    def extract_all_articles(self):
        """
        Étape 3 : Extraction complète de tous les articles
        
        Cette fonction orchestre l'extraction de tous les articles :
        1. Récupère les URLs depuis le sitemap
        2. Extrait chaque article individuellement
        3. Sauvegarde périodiquement les résultats
        4. Gère les erreurs et reprises
        """
        logging.info("Début de l'extraction complète...")
        
        # Récupération de toutes les URLs
        urls = self.get_article_urls_from_sitemap()
        
        if not urls:
            logging.error("Aucune URL trouvée, arrêt de l'extraction")
            return
        
        logging.info(f"Extraction de {len(urls)} articles...")
        
        # Barre de progression pour suivre l'avancement
        with tqdm(total=len(urls), desc="Extraction des articles") as pbar:
            
            for i, url in enumerate(urls):
                # Extraction de l'article
                article_data = self.extract_article_content(url)
                
                if article_data:
                    self.articles.append(article_data)
                    self.extraction_metadata['successfully_extracted'] += 1
                    pbar.set_postfix({
                        'Succès': self.extraction_metadata['successfully_extracted'],
                        'Échecs': len(self.failed_urls)
                    })
                else:
                    self.failed_urls.append(url)
                    self.extraction_metadata['failed_extractions'] += 1
                
                # Mise à jour de la barre de progression
                pbar.update(1)
                
                # Sauvegarde intermédiaire tous les N articles
                if (i + 1) % self.batch_size == 0:
                    self.save_intermediate_results(i + 1)
                
                # Délai respectueux entre les requêtes
                time.sleep(self.delay_between_requests)
        
        logging.info(f"Extraction terminée : {len(self.articles)} articles extraits avec succès")
        
        # Finalisation des métadonnées
        self.finalize_metadata()
    
    def save_intermediate_results(self, current_count):
        """
        Sauvegarde intermédiaire pour éviter la perte de données
        
        Args:
            current_count (int): Nombre d'articles traités jusqu'à présent
        """
        filename = f"ethereum_articles_partial_{current_count}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': self.extraction_metadata,
                    'articles': self.articles,
                    'failed_urls': self.failed_urls
                }, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Sauvegarde intermédiaire : {filename}")
            
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde intermédiaire : {e}")
    
    def finalize_metadata(self):
        """Finalisation des métadonnées d'extraction"""
        
        if self.articles:
            # Calcul des statistiques
            word_counts = [article['word_count'] for article in self.articles]
            
            self.extraction_metadata.update({
                'completion_date': datetime.now().isoformat(),
                'average_word_count': sum(word_counts) / len(word_counts) if word_counts else 0,
                'total_words': sum(word_counts),
                'date_range': {
                    'earliest': min(article['publication_date'] for article in self.articles),
                    'latest': max(article['publication_date'] for article in self.articles)
                }
            })
    
    def save_results(self, output_dir="ethereum_blog_data"):
        """
        Sauvegarde finale dans plusieurs formats
        
        Args:
            output_dir (str): Répertoire de sortie pour les fichiers
        """
        logging.info("Sauvegarde des résultats finaux...")
        
        # Création du répertoire de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Format JSON complet (principal)
        json_file = os.path.join(output_dir, "ethereum_blog_complete.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': self.extraction_metadata,
                'articles': self.articles,
                'failed_urls': self.failed_urls
            }, f, indent=2, ensure_ascii=False)
        
        # 2. Format CSV pour analyses statistiques
        csv_file = os.path.join(output_dir, "ethereum_blog_articles.csv")
        if self.articles:
            df = pd.DataFrame(self.articles)
            # Suppression de la colonne 'content' pour le CSV (trop volumineux)
            df_csv = df.drop('content', axis=1)
            df_csv.to_csv(csv_file, index=False, encoding='utf-8')
        
        # 3. Articles individuels en TXT
        txt_dir = os.path.join(output_dir, "individual_articles")
        os.makedirs(txt_dir, exist_ok=True)
        
        for article in self.articles:
            filename = f"{article['id']}.txt"
            filepath = os.path.join(txt_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Titre: {article['title']}\\n")
                f.write(f"Auteur: {article['author']}\\n")
                f.write(f"Date: {article['publication_date']}\\n")
                f.write(f"URL: {article['url']}\\n")
                f.write(f"Catégorie: {article['category']}\\n")
                f.write("\\n" + "="*50 + "\\n\\n")
                f.write(article['content'])
        
        # 4. Rapport d'extraction
        report_file = os.path.join(output_dir, "extraction_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'EXTRACTION - BLOG ETHEREUM FOUNDATION\\n")
            f.write("="*50 + "\\n\\n")
            f.write(f"Date d'extraction: {self.extraction_metadata['extraction_date']}\\n")
            f.write(f"Articles trouvés: {self.extraction_metadata['total_articles_found']}\\n")
            f.write(f"Extractions réussies: {self.extraction_metadata['successfully_extracted']}\\n")
            f.write(f"Extractions échouées: {self.extraction_metadata['failed_extractions']}\\n")
            f.write(f"Taux de succès: {(self.extraction_metadata['successfully_extracted']/self.extraction_metadata['total_articles_found']*100):.1f}%\\n")
            
            if 'average_word_count' in self.extraction_metadata:
                f.write(f"Nombre moyen de mots par article: {self.extraction_metadata['average_word_count']:.0f}\\n")
                f.write(f"Nombre total de mots: {self.extraction_metadata['total_words']:,}\\n")
        
        logging.info(f"Résultats sauvegardés dans le répertoire : {output_dir}")
        logging.info(f"Fichiers créés :")
        logging.info(f"  - {json_file} (données complètes JSON)")
        logging.info(f"  - {csv_file} (métadonnées CSV)")
        logging.info(f"  - {txt_dir}/ (articles individuels)")
        logging.info(f"  - {report_file} (rapport d'extraction)")

def main():
    """
    Fonction principale - Point d'entrée du script
    
    Cette fonction lance l'extraction complète et gère les erreurs globales.
    """
    print("="*60)
    print("EXTRACTEUR BLOG ETHEREUM FOUNDATION")
    print("="*60)
    print()
    print("Ce script va extraire tous les articles du blog Ethereum Foundation")
    print("depuis décembre 2013 jusqu'à aujourd'hui.")
    print()
    print("Estimation du temps d'exécution : 20-35 minutes")
    print("Données extraites : ~567 articles (~3 Mo de texte)")
    print()
    
    # Demande de confirmation
    response = input("Voulez-vous continuer ? (o/n) : ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("Extraction annulée.")
        return
    
    try:
        # Création et lancement de l'extracteur
        extractor = EthereumBlogExtractor()
        
        # Extraction complète
        extractor.extract_all_articles()
        
        # Sauvegarde des résultats
        extractor.save_results()
        
        print()
        print("="*60)
        print("EXTRACTION TERMINÉE AVEC SUCCÈS !")
        print("="*60)
        print(f"Articles extraits : {extractor.extraction_metadata['successfully_extracted']}")
        print(f"Échecs : {extractor.extraction_metadata['failed_extractions']}")
        print("Consultez le répertoire 'ethereum_blog_data' pour les résultats.")
        
    except KeyboardInterrupt:
        print("\\nExtraction interrompue par l'utilisateur.")
        logging.info("Extraction interrompue par l'utilisateur")
        
    except Exception as e:
        print(f"\\nErreur inattendue : {e}")
        logging.error(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    main()


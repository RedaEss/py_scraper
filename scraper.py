# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import sys
import os

def scrape_basta_media():
    """Scrape les articles de Basta Media"""
    url = "https://portail.basta.media/"
    
    try:
        print("🔍 Début du scraping Basta Media...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Ciblage de la section "À la une"
        une_section = soup.find('div', class_=['home-une', 'slider--une', 'cartouche'])
        
        if not une_section:
            print("❌ Section 'À la une' non trouvée")
            return []
        
        print("✅ Section 'À la une' trouvée")
        
        # Extraction des articles
        articles = une_section.find_all('div', class_=['resume', 'resume--md', 'article', 'hentry'])
        
        if not articles:
            articles = une_section.find_all(class_=['resume--md'])
        
        print(f"📰 {len(articles)} articles trouvés")
        
        results = []
        for article in articles:
            # Titre
            title_elem = article.find(class_='resume-titre')
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Résumé
            summary_elem = article.find(class_=['resume-chapo', 'chapo', 'summary'])
            summary = summary_elem.get_text(strip=True) if summary_elem else None
            
            # Lien
            link_elem = article.find('a')
            link = link_elem.get('href') if link_elem else None
            
            # Nettoyer le lien
            if link and not link.startswith(('http://', 'https://')):
                if link.startswith('/'):
                    link = f"https://portail.basta.media{link}"
                else:
                    link = f"https://portail.basta.media/{link}"
            
            if title and len(title) > 10:
                results.append({
                    'title': title,
                    'summary': summary,
                    'link': link,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
        
        # Dédupliquer
        seen_titles = set()
        unique_results = []
        for article in results:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_results.append(article)
        
        print(f"✅ {len(unique_results)} articles uniques extraits")
        return unique_results
        
    except Exception as e:
        print(f"❌ Erreur lors du scraping: {e}")
        return []

def export_results(data):
    """Exporte les résultats en CSV et JSON dans /results"""
    if not data:
        print("❌ Aucune donnée à exporter")
        return False
    
    try:
        # Le dossier /results est monté depuis l'hôte via Docker
        output_dir = "/results"
        
        # Créer le dossier de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        # Date pour le nom des fichiers
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Export CSV
        csv_filename = f"{output_dir}/{current_date}_basta_articles.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"💾 CSV exporté: {csv_filename}")
        
        # Export JSON
        json_filename = f"{output_dir}/{current_date}_basta_articles.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 JSON exporté: {json_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        return False

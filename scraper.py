# scraper.py - TRADUCTION EXACTE DU CODE R FONCTIONNEL
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import os
import re

def scrape_basta_une():
    """Traduction exacte de la fonction R scrape_basta_une()"""
    url = "https://portail.basta.media/"
    
    try:
        print(" Ciblage de la section 'À la une'...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cibler spécifiquement le slider "À la une" - MÊME SÉLECTEUR QUE R
        une_section = soup.select_one('.home-une.slider--une.cartouche')
        
        if not une_section:
            print(" Section 'À la une' non trouvée")
            return []
        
        print(" Section 'À la une' trouvée!")
        
        # Extraire les articles de la une - MÊME SÉLECTEUR QUE R
        articles = une_section.select('.resume.resume--md.article.hentry')
        
        if len(articles) == 0:
            # Fallback: chercher les résumés directement - MÊME QUE R
            articles = une_section.select('.resume--md, [class*="resume"]')
        
        print(f" Articles trouvés dans la une: {len(articles)}")
        
        if len(articles) > 0:
            results = []
            for article in articles:
                # Titre - cibler spécifiquement la classe resume-titre - MÊME QUE R
                title_elem = article.select_one('.resume-titre')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                else:
                    # Fallback: chercher dans h2, h3, h4 - MÊME QUE R
                    title_elem = article.select_one('h2, h3, h4')
                    title = title_elem.get_text(strip=True) if title_elem else None
                
                # Résumé - chercher le chapô ou premier paragraphe - MÊME QUE R
                summary_elem = article.select_one('.resume-chapo, .chapo, p, .summary')
                summary = summary_elem.get_text(strip=True) if summary_elem else None
                
                # Lien - chercher le lien de l'article - MÊME QUE R
                link_elem = article.select_one('a')
                link = link_elem.get('href') if link_elem else None
                
                # Nettoyer et compléter le lien - MÊME LOGIQUE QUE R
                if link and not re.match(r'^https?://', link):
                    if link.startswith('/'):
                        link = f"https://portail.basta.media{link}"
                    else:
                        link = f"https://portail.basta.media/{link}"
                
                # Date du jour
                scraped_date = datetime.now().strftime('%Y-%m-%d')
                
                if title and len(title) > 10:
                    results.append({
                        'title': title,
                        'summary': summary,
                        'link': link,
                        'date': scraped_date
                    })
            
            # Filtrer les résultats valides - MÊME LOGIQUE QUE R
            seen_titles = set()
            unique_results = []
            for article in results:
                if article['title'] not in seen_titles:
                    seen_titles.add(article['title'])
                    unique_results.append(article)
            
            return unique_results
        else:
            print(" Aucun article trouvé dans la section 'À la une'")
            return []
        
    except Exception as e:
        print(f" Erreur lors du scraping: {e}")
        return []

def scrape_basta_direct_titles():
    """Traduction exacte de la fonction R scrape_basta_direct_titles()"""
    url = "https://portail.basta.media/"
    
    try:
        print("🔍 Extraction directe des titres 'resume-titre'...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraire directement tous les titres avec la classe resume-titre - MÊME QUE R
        title_elements = soup.select('.resume-titre')
        titles = [elem.get_text(strip=True) for elem in title_elements]
        
        # Extraire les liens correspondants - MÊME QUE R
        link_elements = soup.select('.resume-titre a')
        links = [elem.get('href') for elem in link_elements]
        
        # Compléter les liens si nécessaire - MÊME LOGIQUE QUE R
        full_links = []
        for link in links:
            if link and not re.match(r'^https?://', link):
                if link.startswith('/'):
                    full_links.append(f"https://portail.basta.media{link}")
                else:
                    full_links.append(f"https://portail.basta.media/{link}")
            else:
                full_links.append(link)
        
        # Date du jour
        scraped_date = datetime.now().strftime('%Y-%m-%d')
        
        # Créer le dataframe - MÊME LOGIQUE QUE R
        if len(titles) > 0:
            # S'assurer de la même longueur - MÊME QUE R
            min_length = min(len(titles), len(full_links))
            results = []
            
            for i in range(min_length):
                results.append({
                    'title': titles[i],
                    'summary': None,  # Les résumés ne sont pas directement disponibles - MÊME QUE R
                    'link': full_links[i],
                    'date': scraped_date
                })
            
            # Limiter aux 5 premiers (la une) - MÊME QUE R
            results = results[:5]
            
            print(f" {len(results)} titres extraits directement")
            return results
        else:
            print(" Aucun titre trouvé")
            return []
        
    except Exception as e:
        print(f" Erreur: {e}")
        return []

def export_results(data):
    """Exporte les résultats en CSV et JSON"""
    if not data:
        print(" Aucune donnée à exporter")
        return False
    
    try:
        output_dir = "/results"
        os.makedirs(output_dir, exist_ok=True)
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Export CSV avec Pandas
        csv_filename = f"{output_dir}/{current_date}_basta_articles.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f" CSV exporté: {csv_filename}")
        
        # Export JSON
        json_filename = f"{output_dir}/{current_date}_basta_articles.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f" JSON exporté: {json_filename}")
        
        return True
        
    except Exception as e:
        print(f" Erreur lors de l'export: {e}")
        return False

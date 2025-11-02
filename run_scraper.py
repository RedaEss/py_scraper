# run_scraper.py - TRADUCTION EXACTE DE LA LOGIQUE R
from scraper import scrape_basta_une, scrape_basta_direct_titles, export_results
import sys

def main():
    print(" SCRAPER BASTA MEDIA - PYTHON (TRADUCTION R)")
    print("=" * 50)
    
    # Méthode 1: Scraper la section "À la une" - MÊME LOGIQUE QUE R
    print("\n1. Extraction de la section 'À la une'...")
    data_une = scrape_basta_une()
    
    # Méthode 2: Extraction directe des titres (fallback) - MÊME QUE R
    if len(data_une) == 0:
        print("\n2. Fallback: extraction directe des titres...")
        data_une = scrape_basta_direct_titles()
    
    # Résultats finaux
    final_data = data_une
    
    if len(final_data) > 0:
        print(f"\n RÉSULTATS TROUVÉS:")
        print("====================")
        
        # Afficher les résultats - MÊME FORMAT QUE R
        for i, article in enumerate(final_data, 1):
            print(f"\n{i}. {article['title']}")
            if article['summary'] and len(article['summary']) > 0:
                print(f"    {article['summary'][:100]}...")
            else:
                print("    [Résumé non disponible]")
            print(f"    {article['link']}")
            print(f"    {article['date']}")
        
        # Export
        success = export_results(final_data)
        
        if success:
            print(f"\n Fichiers exportés avec {len(final_data)} articles")
            sys.exit(0)  # Succès
        else:
            print("\n❌ ÉCHEC de l'export")
            sys.exit(1)  # Échec
    else:
        print("\n❌ AUCUN ARTICLE TROUVÉ")
        print("Conseils:")
        print("1. Vérifiez que le site https://portail.basta.media/ est accessible")
        print("2. Les sélecteurs CSS peuvent avoir changé")
        sys.exit(1)  # Échec

if __name__ == "__main__":
    main()

# run_scraper.py
from scraper import scrape_basta_media, export_results
import sys

def main():
    print("🚀 SCRAPER BASTA MEDIA - PYTHON")
    print("=" * 40)
    
    # Scraping
    articles = scrape_basta_media()
    
    if articles:
        print(f"\n✅ RÉSULTATS TROUVÉS:")
        print("=" * 20)
        
        # Affichage des résultats
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            if article['summary']:
                print(f"   📝 {article['summary'][:100]}...")
            print(f"   🔗 {article['link']}")
            print(f"   📅 {article['date']}")
        
        # Export dans /results
        success = export_results(articles)
        
        if success:
            print(f"\n🎯 SCRAPING RÉUSSI - {len(articles)} articles exportés vers /results")
            sys.exit(0)
        else:
            print("\n❌ ÉCHEC de l'export")
            sys.exit(1)
    else:
        print("\n❌ AUCUN ARTICLE TROUVÉ")
        sys.exit(1)

if __name__ == "__main__":
    main()

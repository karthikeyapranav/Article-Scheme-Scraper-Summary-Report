from scrapers.microsoft_research import MicrosoftResearchScraper
from scrapers.myscheme import MySchemeScraper
import os

def main():
    os.makedirs('output', exist_ok=True) # Ensure output directory exists

    # Scrape Microsoft Research Blog
    print("\n--- Starting Microsoft Research Blog Scraping ---")
    ms_scraper = MicrosoftResearchScraper()
    ms_scraper.scrape(max_pages=2)  # Scrape 2 pages for demo
    ms_scraper.save_to_json("microsoft_research.json")
    ms_scraper.save_to_csv("microsoft_research.csv")
    ms_scraper.generate_report(
        "Microsoft Research Blog",
        "Page structure for articles is generally consistent, making extraction of titles, links, and excerpts straightforward. Full content extraction might need adaptable selectors for varied article layouts. Pagination is URL-based.",
        "No explicit anti-bot mechanisms (e.g., CAPTCHA, complex JS obfuscation) beyond basic cookie banners were encountered.",
        "Data completeness is high for basic article details. Full content extraction attempts to get all visible text, but specific sections like 'related articles' are excluded unless targeted. Date and authors are often present."
    )
    print("--- Microsoft Research Blog Scraping Completed ---\n")
    
    # Scrape MyScheme Portal (focusing on Agriculture for now)
    print("\n--- Starting MyScheme Portal Scraping (Agriculture Category) ---")
    scheme_scraper = MySchemeScraper()
    scheme_scraper.scrape_agriculture_schemes(max_schemes=10) # Scrape 10 schemes from Agriculture
    scheme_scraper.save_to_json("myscheme_agriculture.json")
    scheme_scraper.save_to_csv("myscheme_agriculture.csv")
    scheme_scraper.generate_report(
        "MyScheme Portal (Agriculture)",
        "The MyScheme portal uses dynamic content loading, requiring scrolling to reveal all categories and schemes. Category and scheme card selectors need to be robust due to potential variations in HTML structure. Detail pages for schemes often use accordion-like structures for Eligibility and FAQs, which require specific handling (e.g., clicking to reveal content if not initially visible).",
        "No explicit anti-bot mechanisms like CAPTCHAs or IP blocking were observed during testing. However, rapid requests might trigger rate limiting.",
        "Data completeness for schemes is generally good for title, link, and main content. Eligibility and FAQs are extracted where clearly identifiable, but their presence and exact formatting can vary between schemes, potentially leading to 'N/A' or incomplete FAQ lists for some entries. The 'content' field aims to capture all major text."
    )
    print("--- MyScheme Portal Scraping Completed ---\n")

if __name__ == "__main__":
    main()
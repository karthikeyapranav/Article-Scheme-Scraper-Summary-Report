from playwright.sync_api import sync_playwright
import time
import json
import os
from .base_scraper import BaseScraper

class MySchemeScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.myscheme.gov.in/"
        
        # --- List of specific scheme URLs to scrape (MANUALLY PROVIDED) ---
        self.specific_scheme_urls = [
            "https://www.myscheme.gov.in/schemes/icdpsva-srgu",
            "https://www.myscheme.gov.in/schemes/anby",
            "https://www.myscheme.gov.in/schemes/ncrfs",
            "https://www.myscheme.gov.in/schemes/fapllf",  # Your 4th link
            "https://www.myscheme.gov.in/schemes/cdpnerqucsecoc" # Your 5th link
        ]
    
    def scrape_agriculture_schemes(self, max_schemes=50): # max_schemes now controls how many of the provided links to scrape
        self.data = [] # Reset data for each scrape call
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False) # Keep headless=False for debugging
            context = browser.new_context()
            
            print(f"Scraping specific scheme URLs directly. Total URLs provided: {len(self.specific_scheme_urls)}")
            
            scraped_count = 0
            for scheme_link in self.specific_scheme_urls:
                if scraped_count >= max_schemes:
                    print(f"Reached max_schemes ({max_schemes}) based on provided links. Stopping.")
                    break
                
                # Extract a title placeholder from the URL for logging purposes
                title_from_url = scheme_link.split('/')[-1].replace('-', ' ').upper()
                
                print(f"\nScraping scheme: {title_from_url} ({scheme_link})")
                
                scheme_page = context.new_page()
                try:
                    scheme_page.goto(scheme_link, wait_until="domcontentloaded", timeout=60000)
                    time.sleep(3) # Give page time to load content after basic DOM is ready

                    # Get the actual title from the page once loaded (more robust)
                    actual_title_element = scheme_page.locator("h1.scheme-title, h1.text-dark, h3.scheme-heading, h2.main-title").first
                    actual_title = actual_title_element.inner_text().strip() if actual_title_element.count() > 0 else title_from_url
                    print(f"Actual title found: {actual_title}")

                    # Scroll to load all content on the detail page (important for dynamic sections)
                    print(f"Scrolling on detail page for {actual_title}...")
                    last_scheme_height = scheme_page.evaluate("document.body.scrollHeight")
                    for i in range(5): # Multiple scrolls to ensure all dynamic content loads
                        scheme_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(1) # Give a small pause for content to render after scroll
                        new_scheme_height = scheme_page.evaluate("document.body.scrollHeight")
                        if new_scheme_height == last_scheme_height:
                            print(f"Reached end of scrollable content after {i+1} scrolls.")
                            break
                        last_scheme_height = new_scheme_height
                    time.sleep(1) # Final buffer after scrolling
                    print("Finished scrolling on detail page.")

                    # Extract full content (more comprehensive selectors)
                    content = "N/A"
                    content_selectors = [
                        ".scheme-details-wrapper", "main.container-fluid", "div[role='main']",
                        ".scheme-details", ".content-area", "div.container-fluid .card-body",
                        "div#scheme-detail-content", "div.container.py-4", "div.col-lg-7.col-md-12",
                        "div.scheme-description", "section.py-4", "div.content-section"
                    ]
                    for sel in content_selectors:
                        try:
                            elem = scheme_page.locator(sel).first
                            if elem.count() > 0 and elem.is_visible():
                                content = elem.inner_text(timeout=5000).strip()
                                break
                        except:
                            pass
                    if content == "N/A":
                        print(f"Warning: Could not extract robust content for {actual_title}. Falling back to body.")
                        content = scheme_page.locator("body").inner_text(timeout=5000).strip()

                    # Extract eligibility
                    eligibility = "N/A"
                    eligibility_selectors = [
                        "h2:has-text('Eligibility Criteria') + div", "h3:has-text('Eligibility Criteria') + div",
                        "//div[@id='eligibility-criteria-section']", ".eligibility-section",
                        "div.accordion-item:has(button:has-text('Eligibility')) div.accordion-body",
                        "div[data-component-name='Eligibility']", "//h3[contains(text(),'Eligibility')]/following-sibling::div[1]",
                        "//p[contains(text(),'Eligibility')]//ancestor::div[contains(@class, 'card-body')]",
                        "//strong[contains(text(),'Eligibility')]/ancestor::div[contains(@class, 'card-body')]",
                        "//div[contains(@class, 'card-header') and .//h4[contains(text(), 'Eligibility')]]/following-sibling::div[contains(@class, 'card-body')]",
                        "div.scheme-detail-section:has(h4:has-text('Eligibility Criteria')) div.card-body",
                        "div.container.py-4:has(h4:has-text('Eligibility Criteria')) div.mt-4",
                        "div:has(span.scheme-details-label:has-text('Eligibility Criteria')) ~ div",
                        "div.col-lg-7.col-md-12 div.mt-4:has(h4:has-text('Eligibility Criteria')) + div",
                        "div.details-section:has(h4:has-text('Eligibility Criteria')) div.content"
                    ]
                    for selector in eligibility_selectors:
                        try:
                            elem = scheme_page.locator(selector).first
                            if elem.count() > 0 and elem.is_visible():
                                eligibility = elem.inner_text().strip()
                                break
                        except:
                            pass
                    
                    # Extract FAQs
                    faqs = []
                    faq_selectors = [
                        "h2:has-text('FAQs') + div", "h3:has-text('FAQs') + div",
                        "//div[@id='faq-section']", ".faq-section",
                        "div.accordion-item:has(button:has-text('FAQ'))",
                        "div[data-component-name='FAQs']", "//h3[contains(text(),'FAQs')]/following-sibling::div[1]",
                        "div.col-lg-7.col-md-12.accordion",
                        "div.scheme-detail-section:has(h4:has-text('FAQs')) div.card-body",
                        "div.container.py-4:has(h4:has-text('FAQs')) div.mt-4",
                        "div:has(span.scheme-details-label:has-text('FAQs')) ~ div",
                        "div.col-lg-7.col-md-12 div.mt-4:has(h4:has-text('FAQs')) + div",
                        "div.details-section:has(h4:has-text('FAQs')) div.content"
                    ]

                    for selector in faq_selectors:
                        try:
                            faq_container = scheme_page.locator(selector).first
                            if faq_container.count() > 0 and faq_container.is_visible():
                                # Click all accordion headers to reveal answers
                                accordion_buttons = faq_container.locator("button.accordion-button, .faq-question, .card-header, h4").all()
                                for button in accordion_buttons:
                                    if button.is_visible() and ("collapsed" in button.get_attribute("class", timeout=1000) or button.get_attribute("aria-expanded", timeout=1000) == "false"):
                                        try:
                                            button.click(timeout=2000)
                                            time.sleep(0.5)
                                        except:
                                            pass

                                items = faq_container.locator("div.accordion-item, .faq-item, div.card, div.row.mb-2").all()
                                for item in items:
                                    try:
                                        question_elem = item.locator("button.accordion-button, .question, h4, .faq-question, .card-header, strong, .scheme-details-label").first
                                        answer_elem = item.locator(".accordion-body, .answer, .faq-answer, p, .card-body, .mt-2").first
                                        
                                        question = question_elem.inner_text().strip() if question_elem.count() > 0 else ""
                                        answer = answer_elem.inner_text().strip() if answer_elem.count() > 0 else ""
                                        if question and answer:
                                            faqs.append({"question": question, "answer": answer})
                                    except Exception as faq_item_e:
                                        pass
                                break
                        except Exception as faq_outer_e:
                            pass

                    self.data.append({
                        "category": "Agriculture, Rural & Environment", # Category remains constant for these schemes
                        "title": actual_title,
                        "link": scheme_link,
                        "content": content,
                        "eligibility": eligibility,
                        "faqs": faqs
                    })
                    print(f"Successfully scraped: {actual_title}")
                    scraped_count += 1
                    
                except Exception as e:
                    print(f"Error scraping full scheme details from {scheme_link}: {e}")
                finally:
                    scheme_page.close() # Close the individual scheme page tab
                    
            browser.close()

if __name__ == "__main__":
    scraper = MySchemeScraper()
    # Scrape all provided links or up to a higher max_schemes if you provide more
    scraper.scrape_agriculture_schemes(max_schemes=50) # Set to scrape all 5 provided links and potentially more if added
    scraper.save_to_json("myscheme_agriculture.json")
    scraper.save_to_csv("myscheme_agriculture.csv")
    print("\nMyScheme Scraping Report:")
    print(f"Total schemes scraped: {len(scraper.data)}")
    if scraper.data:
        print("Example scheme:")
        print(f"Title: {scraper.data[0]['title']}")
        print(f"Content length: {len(scraper.data[0]['content'])} chars")
        print(f"Eligibility: {scraper.data[0]['eligibility'][:100]}..." if scraper.data[0]['eligibility'] else "N/A")
        print(f"FAQs found: {len(scraper.data[0]['faqs'])}")
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import json
import os
from .base_scraper import BaseScraper # Import BaseScraper

class MicrosoftResearchScraper(BaseScraper): # Inherit from BaseScraper
    def __init__(self):
        super().__init__() # Call parent constructor
        self.base_url = "https://www.microsoft.com/en-us/research/blog/"
        # self.data is now inherited from BaseScraper
    
    # save_to_json is inherited, no need to redefine unless custom logic is needed.
    # save_to_csv is inherited.

    # This method was incorrectly defined outside the class in your original code.
    # It should be a static or class method, or integrated into the scrape logic.
    # For now, I'll remove it as its functionality is implicitly handled within scrape.
    # def extract_article_details(page):
    #     date = page.locator(".publication-date").inner_text()
    #     authors = [author.inner_text() for author in page.locator(".author-name").all()]
    #     return {"date": date, "authors": authors}

    def scrape(self, max_pages=1):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False) # Set headless to True for faster scraping
            context = browser.new_context()
            
            page_num = 1
            while page_num <= max_pages:
                page = context.new_page()
                url = f"{self.base_url}page/{page_num}/" if page_num > 1 else self.base_url
                print(f"Navigating to: {url}")
                
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000) # Increased timeout
                    time.sleep(2)
                    
                    # Simplified cookie handling (might need more robust solutions if it reappears)
                    try:
                        accept_buttons = [
                            "#onetrust-accept-btn-handler",
                            "text=Accept All Cookies",
                            "text=Agree",
                            "text=Consent",
                            "button:has-text('Accept')"
                        ]
                        for btn in accept_buttons:
                            if page.locator(btn).count() > 0 and page.locator(btn).is_visible():
                                page.locator(btn).click()
                                print("Closed cookie banner")
                                time.sleep(1)
                                break
                    except Exception as e:
                        print(f"No cookie banner found or error closing: {e}")
                        pass
                    
                    # Wait for articles
                    page.wait_for_selector("article", timeout=30000) # Increased timeout
                    
                    # Get all articles
                    articles = page.locator("article").all()
                    print(f"Found {len(articles)} articles on page {page_num}")
                    
                    for i, article in enumerate(articles):
                        try:
                            # Extract basic info
                            title_element = article.locator("h2, h3").first
                            link_element = article.locator("a").first
                            excerpt_element = article.locator("p").first

                            title = title_element.inner_text(timeout=5000) if title_element.count() > 0 else "N/A"
                            link = link_element.get_attribute("href") if link_element.count() > 0 else "N/A"
                            excerpt = excerpt_element.inner_text(timeout=5000) if excerpt_element.count() > 0 else "N/A"
                            
                            if link == "N/A":
                                print(f"Skipping article {i+1} on page {page_num} due to missing link.")
                                continue

                            # Ensure absolute URL
                            if not link.startswith("http"):
                                link = f"https://www.microsoft.com{link}"
                            
                            # Visit article page
                            article_page = context.new_page()
                            try:
                                print(f"Visiting article: {link}")
                                article_page.goto(link, wait_until="domcontentloaded", timeout=60000)
                                time.sleep(2)
                                
                                # Get main content. Microsoft Research blog articles typically have content within main or specific content divs.
                                content_selector = "div.content-area, div.msr-blog-post-content, article.msr-blog-post"
                                content = ""
                                if article_page.locator(content_selector).count() > 0:
                                    content = article_page.locator(content_selector).first.inner_text(timeout=10000)
                                else:
                                    print(f"Could not find main content for {link} with common selectors. Extracting body text.")
                                    content = article_page.locator("body").inner_text(timeout=10000)

                                # Further extraction: Date and Authors, if available on the article page
                                article_date = "N/A"
                                authors = []
                                try:
                                    date_element = article_page.locator(".publication-date, .msr-blog-post-date").first
                                    if date_element.count() > 0:
                                        article_date = date_element.inner_text()
                                except:
                                    pass # Date not found

                                try:
                                    author_elements = article_page.locator(".author-name, .msr-blog-post-author").all()
                                    authors = [author.inner_text() for author in author_elements]
                                except:
                                    pass # Authors not found

                                self.data.append({
                                    "title": title,
                                    "link": link,
                                    "excerpt": excerpt,
                                    "content": content,
                                    "date": article_date,
                                    "authors": authors
                                })
                                print(f"Scraped: {title}")
                                
                            except Exception as e:
                                print(f"Error scraping full article content from {link}: {e}")
                            finally:
                                article_page.close()
                                
                        except Exception as e:
                            print(f"Error processing article card on page {page_num}: {e}")
                            continue # Continue to the next article even if one fails
                            
                except Exception as e:
                    print(f"Error on page {page_num}: {e}")
                finally:
                    page.close()
                    page_num += 1
            
            browser.close()

if __name__ == "__main__":
    scraper = MicrosoftResearchScraper()
    scraper.scrape(max_pages=1)
    scraper.save_to_json("microsoft_research.json")
    scraper.save_to_csv("microsoft_research.csv") # Now this will work
    # Example for report generation (will be called from main.py)
    # scraper.generate_report(
    #     "Microsoft Research Blog",
    #     "Pagination is straightforward. Content selectors might need refinement for robustness across different article layouts.",
    #     "No explicit anti-bot mechanisms encountered (e.g., CAPTCHA, complex JS obfuscation) beyond basic cookie banners.",
    #     "Data completeness depends on the robustness of content selectors; some articles might have varied structures."
    # )
    print("Microsoft Research Blog Scraping completed successfully!")
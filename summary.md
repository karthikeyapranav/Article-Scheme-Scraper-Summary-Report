# MyScheme Portal Scraping Summary (Agriculture Category)

This document summarizes the approach taken and the current status of the MyScheme portal scraper specifically for the Agriculture, Rural & Environment category.

## Scraping Strategy

The MyScheme portal presents significant challenges for automated data extraction due to its highly dynamic nature and the unreliability of its API endpoints for comprehensive listing data. Consequently, the chosen and most reliable strategy is a **direct URL-based scraping approach** using Playwright.

### Phase 1: Direct URL Input
- **Action:** The scraper is pre-configured with a list of specific, full URLs to individual scheme detail pages (e.g., `https://www.myscheme.gov.in/schemes/icdpsva-srgu`).
- **Rationale:** This completely bypasses the problematic category listing pages and their unstable DOM structures or API calls, ensuring the scraper always targets known, valid scheme pages.

### Phase 2: Detailed Page Extraction (via Playwright)
- **Action:** For each provided URL, Playwright launches a headless (or visible, for debugging) browser instance. It navigates to the scheme's detail page, waits for content to load, and performs simulated user actions.
- **Key Operations:**
    - **Navigation:** Uses `goto()` to load the full scheme page.
    - **Waiting:** Employs `time.sleep()` strategically to allow JavaScript-rendered content to appear after initial page load.
    - **Scrolling:** Executes JavaScript `window.scrollTo` commands to ensure all lazy-loaded content (e.g., long descriptions, all FAQs) becomes visible in the browser's viewport.
    - **Element Locating:** Utilizes robust CSS and XPath selectors (`scheme_page.locator()`) to identify specific elements like the scheme title, main content sections, eligibility criteria, and FAQ questions/answers. Multiple alternative selectors are provided for each data point to account for minor variations in page structure.
    - **Interaction:** Clicks on accordion buttons within the FAQ sections to reveal hidden answers, simulating user interaction.
    - **Data Extraction:** Extracts the `inner_text()` of located elements.

## Data Points Extracted

For each scraped scheme, the following information is collected:

-   `category`: Always "Agriculture, Rural & Environment" as per the scope.
-   `title`: The official title of the scheme.
-   `link`: The direct URL to the scheme's detail page.
-   `content`: The full description or main body text of the scheme.
-   `eligibility`: The eligibility criteria for the scheme.
-   `faqs`: A list of dictionaries, each containing a "question" and its corresponding "answer".

## Output Format

The extracted data is stored in two formats for versatility:

-   `output/myscheme_agriculture.json`: Ideal for programmatic use, data exchange, and debugging.
-   `output/myscheme_agriculture.csv`: Easily viewable in spreadsheet applications for quick analysis.

## Limitations and Future Considerations

1.  **Manual URL Input:** The primary limitation is the current necessity for manual provision of scheme URLs. This scraper cannot automatically discover new schemes as they are added to the portal without manual intervention.
2.  **Selector Maintenance:** While robust, the CSS/XPath selectors for detail pages may still require occasional updates if MyScheme.gov.in undergoes significant design changes.
3.  **Scalability for All Schemes:** To scrape *all* schemes across *all* categories, a more complex solution would be required, potentially involving:
    * **Continuous API Monitoring:** Regularly testing API endpoints for changes and adapting the request payload/parsing logic.
    * **Machine Learning for Element Detection:** More advanced techniques to identify content dynamically without rigid selectors.
    * **Human-in-the-Loop:** A system where a human confirms new URLs or fixes broken selectors when automated methods fail.

This scraper provides a highly reliable solution for collecting detailed data from specific MyScheme entries, given its current architectural challenges.
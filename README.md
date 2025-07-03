# MyScheme Portal Scraper (Agriculture Category)

This project contains a Python-based web scraper designed to extract detailed information about specific agricultural schemes from the MyScheme portal (myscheme.gov.in).

## Overview

Due to the highly dynamic and frequently changing nature of the MyScheme portal's category listing pages and their underlying APIs, this scraper operates by processing a predefined list of direct URLs to individual scheme detail pages. This approach has proven to be the most reliable for consistent data extraction from this particular website.

The scraper uses:
- **Playwright:** For browser automation, allowing it to navigate to scheme pages, wait for dynamic content to load, scroll, interact with UI elements (like FAQ accordions), and extract visible text.
- **Python's `requests` (briefly attempted for API, but reverted):** While an API-based approach was explored, it was found to be unreliable due to changing API endpoints and payloads.

## Features

- Scrapes detailed information for a list of specified scheme URLs.
- Extracts:
    - Scheme Title
    - Scheme Link (the URL itself)
    - Full Scheme Content/Description
    - Eligibility Criteria
    - Frequently Asked Questions (FAQs) - including questions and answers.
- Handles dynamic content loading on detail pages through scrolling and strategic pauses.
- Interacts with accordion elements (e.g., for FAQs) to reveal hidden content.
- Saves extracted data to both JSON and CSV formats.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Installation Steps

1.  **Clone the repository (or set up your project structure):**
    ```bash
    git clone <your-repo-link>
    cd scheme_scraper # Or your project directory name
    ```

2.  **Install Python dependencies:**
    This project requires `playwright` and `requests`.

    ```bash
    pip install playwright requests
    ```

3.  **Install Playwright browser binaries:**
    After installing the Playwright Python library, you need to install the browser engines (Chromium, Firefox, WebKit) that Playwright controls.

    ```bash
    playwright install
    ```
    *(Note: You only need Chromium for this project, but `playwright install` installs all by default, which is usually fine.)*

## Usage

1.  **Define Scheme URLs:**
    Open the `scrapers/myscheme.py` file.
    Locate the `self.specific_scheme_urls` list within the `MySchemeScraper` class's `__init__` method.
    Add or remove the direct URLs of the MyScheme pages you wish to scrape from this list.

    ```python
    self.specific_scheme_urls = [
        "[https://www.myscheme.gov.in/schemes/icdpsva-srgu](https://www.myscheme.gov.in/schemes/icdpsva-srgu)",
        "[https://www.myscheme.gov.in/schemes/anby](https://www.myscheme.gov.in/schemes/anby)",
        "[https://www.myscheme.gov.in/schemes/ncrfs](https://www.myscheme.gov.in/schemes/ncrfs)",
        "[https://www.myscheme.gov.in/schemes/fapllf](https://www.myscheme.gov.in/schemes/fapllf)",
        "[https://www.myscheme.gov.in/schemes/cdpnerqucsecoc](https://www.myscheme.gov.in/schemes/cdpnerqucsecoc)"
    ]
    ```

2.  **Run the Scraper:**
    Navigate to your project's root directory in your terminal (where `main.py` is located).
    Execute the `main.py` script:

    ```bash
    python main.py
    ```

    A Chromium browser window will open, and you will observe it navigating to each specified scheme page, scrolling, and interacting with elements.

## Output

The scraped data will be saved in the `output/` directory (created automatically if it doesn't exist) as:

-   `myscheme_agriculture.json`: Structured data in JSON format.
-   `myscheme_agriculture.csv`: Tabular data in CSV format.
-   `summary_report_myscheme_portal_(agriculture).txt`: A brief summary of the scraping run.

## Troubleshooting

-   **`Page.wait_for_selector: Timeout ... exceeded.`**: This error indicates that Playwright could not find a specific HTML element within the given time. While this version of the code uses specific URLs, if this error occurs on a *detail page*, it means the selectors for content, eligibility, or FAQs might need updating. Inspect the specific scheme page manually (with `headless=False` during runtime) and adjust the selectors in `myscheme.py` accordingly.
-   **`playwright install` fails**: Ensure you have a stable internet connection and sufficient disk space. Sometimes, running `pip install --upgrade playwright` first, then `playwright install`, can help.
-   **No data in output files**: Check the console output for any `Error scraping full scheme details from...` messages. This will indicate which links failed.
-   **Website Changes**: MyScheme is a dynamic website. If the structure of individual scheme detail pages changes significantly, the existing CSS/XPath selectors in `myscheme.py` for content, eligibility, and FAQs may become outdated. Manual inspection and updating of these selectors will be required.

## Contribution

If you identify more robust selectors or improvements for this scraper, feel free to suggest them!
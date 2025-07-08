# 🌐 Government & Enterprise Web Scrapers with Playwright: MyScheme + Microsoft Blogs

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.44%2B-2f96bd.svg?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Web Scraping](https://img.shields.io/badge/Web%20Scraping-Dynamic%20Content-orange.svg)](https://en.wikipedia.org/wiki/Web_scraping)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains **two robust Playwright-based web scrapers** in Python designed to handle highly dynamic content:

- **🟢 MyScheme Scraper:** Targets Indian Government Agricultural Schemes ([myscheme.gov.in](https://www.myscheme.gov.in))  
- **🔵 Microsoft Blog/Documentation Scraper:** Targets dynamic content feeds and technical documentation pages from Microsoft domains (e.g., [learn.microsoft.com](https://learn.microsoft.com), [techcommunity.microsoft.com](https://techcommunity.microsoft.com))

---

## 🎯 Why Two Scrapers?

Modern websites frequently load content dynamically using JavaScript. This makes traditional scraping tools like `requests + BeautifulSoup` insufficient. Both **MyScheme** and **Microsoft Docs/Blogs** fall into this category:

| Feature | MyScheme | Microsoft Docs/Blogs |
|--------|----------|-----------------------|
| Dynamic JS Content | ✅ | ✅ |
| Collapsible Sections (FAQs, Accordions) | ✅ | ✅ |
| API Instability | ✅ | ✅ |
| Requires Browser Automation | ✅ | ✅ |

This repo demonstrates **browser-based scraping using Playwright** to robustly extract all such content.

---

## 🟢 Scraper 1: MyScheme Agricultural Schemes (myscheme.gov.in)

### 🧩 Challenges:
- JS-rendered scheme descriptions, eligibility, and FAQs.
- Dynamic collapsible content.
- Inconsistent API responses.

### 🛠️ Approach:
- Use **Playwright** to launch a browser.
- Navigate to **direct scheme detail URLs**.
- Expand and scroll content.
- Scrape:
  - Scheme title
  - Full description
  - Eligibility criteria
  - FAQ (Q&A pairs)

### 📁 Output:
- `myscheme_agriculture.json`
- `myscheme_agriculture.csv`
- `summary_report_myscheme_portal_(agriculture).txt`

> ✨ Located in the `/scrapers/myscheme_scraper.py`

---

## 🔵 Scraper 2: Microsoft Documentation / Blog Scraper

### 🧩 Challenges:
- Blogs and docs pages often render content dynamically.
- Documentation might use complex nested structures (shadow DOM, lazy loading).
- Volatile HTML structures and selectors.
- Rate-limiting and bot detection on Microsoft domains.

### 🛠️ Approach:
- Use **Playwright** to open Microsoft blog/doc pages.
- Wait for content blocks to render using `page.wait_for_selector`.
- Expand hidden sections (e.g., “Show More”, code blocks, FAQs).
- Scrape:
  - Blog/document title
  - Author, publish date (if available)
  - Main article content
  - Tags or categories (if present)

### 📁 Output:
- `microsoft_docs_output.json`
- `microsoft_docs_output.csv`
- `microsoft_summary_report.txt`

> ✨ Located in the `/scrapers/microsoft_scraper.py`

---

🚀 Setup & Run
🔧 Install Dependencies

pip install -r requirements.txt
playwright install
▶️ Run MyScheme Scraper

python scrapers/myscheme_scraper.py
▶️ Run Microsoft Scraper

python scrapers/microsoft_scraper.py
🛠 Common Playwright Tricks Used
page.wait_for_selector() – Waits for dynamic content to load.

page.click() – Expands accordion or hidden sections.

page.evaluate("window.scrollTo(...)") – Triggers lazy-loaded content.

Headless mode toggle for debugging.

try-except for selector failures and fallback parsing.

⚠️ Troubleshooting
Timeout on selector: Page changed; inspect and update selectors.

Empty fields: Element not found or dynamically added late.

Bot detection: Use random delays and headers if scraping Microsoft at scale.

🤝 Contribution
Contributions welcome! Feel free to submit PRs with:

Updated selectors

Retry mechanisms

Headless fallback logic

Output format improvements (Markdown export, PDF, etc.)



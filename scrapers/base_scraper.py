import json
from typing import Dict, List
import pandas as pd
import os

class BaseScraper:
    def __init__(self):
        self.data = []
    
    def save_to_json(self, filename: str):
        os.makedirs('output', exist_ok=True)
        with open(f'output/{filename}', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to output/{filename}")
    
    def save_to_csv(self, filename: str):
        os.makedirs('output', exist_ok=True)
        df = pd.DataFrame(self.data)
        df.to_csv(f'output/{filename}', index=False)
        print(f"Data saved to output/{filename}")
    
    def generate_report(self, scraper_name: str, page_structure_challenges: str, anti_bot_mechanisms: str, data_completeness_evaluation: str):
        report = {
            "scraper_name": scraper_name,
            "total_items_scraped": len(self.data),
            "page_structure_challenges": page_structure_challenges,
            "anti_bot_mechanisms": anti_bot_mechanisms,
            "data_completeness_evaluation": data_completeness_evaluation,
            "example_item": self.data[0] if self.data else "No data scraped to provide an example."
        }
        report_filename = f'output/summary_report_{scraper_name.lower().replace(" ", "_")}.txt'
        os.makedirs('output', exist_ok=True)
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(f"--- Summary Report for {scraper_name} ---\n\n")
            f.write(json.dumps(report, indent=2, ensure_ascii=False))
            f.write("\n\n")
        print(f"Summary report generated at {report_filename}")
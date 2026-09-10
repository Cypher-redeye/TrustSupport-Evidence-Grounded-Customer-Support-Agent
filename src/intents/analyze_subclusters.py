import json
from pathlib import Path
from src.config import settings
import re

def analyze_splits():
    sample_file = Path(settings.processed_data_dir) / "intent_discovery_sample.jsonl"
    
    ban_count = 0
    stats_reset_count = 0
    hacked_count = 0
    
    access_count = 0
    payment_count = 0
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        for line in f:
            req = json.loads(line)
            text = req['text'].lower()
            
            # 1. Ban Appeal Analysis
            if re.search(r'\b(ban|banned|suspended|unban)\b', text):
                ban_count += 1
            if re.search(r'\b(stats reset|reset my stats|lost all my stats)\b', text):
                stats_reset_count += 1
            if re.search(r'\b(hacked|stolen|compromised|unauthorized)\b', text):
                hacked_count += 1
                
            # 2. Purchase vs Download Analysis
            if re.search(r'\b(download|pre-load|preload|install|installing|code|digital copy|redeem)\b', text):
                access_count += 1
            if re.search(r'\b(buy|bought|purchased|payment|charged|refund|money back|dollars|store)\b', text):
                payment_count += 1
                
    print(f"--- ACCOUNT BAN APPEAL CATEGORIES ---")
    print(f"Bans/Suspensions: {ban_count}")
    print(f"Stats Resets: {stats_reset_count}")
    print(f"Hacked/Compromised: {hacked_count}")
    print(f"--- PURCHASE & DOWNLOAD CATEGORIES ---")
    print(f"Access/Download/Licenses: {access_count}")
    print(f"Payment/Purchase/Transactions: {payment_count}")

if __name__ == "__main__":
    analyze_splits()

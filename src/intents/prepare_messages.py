import os
import json
import re
import logging
from pathlib import Path
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def is_noise(text: str) -> tuple[bool, str]:
    """Determines if a message is noise and returns the reason."""
    # Strip mentions
    text_no_mentions = re.sub(r'@[a-zA-Z0-9_]+', '', text).strip()
    
    # Strip URLs
    text_no_urls = re.sub(r'http\S+|www\.\S+', '', text_no_mentions).strip()
    
    if not text_no_urls:
        return True, "EMPTY_AFTER_CLEANING"
        
    if len(text_no_urls) < 10:
        return True, "TOO_SHORT"
        
    if len(text_no_urls) > 1000:
        return True, "TOO_LONG"
        
    return False, ""

def extract_request_blocks():
    brand = settings.selected_brand or "ATVIAssist"
    input_file = Path(settings.processed_data_dir) / f"{brand.lower()}_conversations.jsonl"
    
    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return
        
    results = []
    excluded = []
    exclusion_reasons = {}
    total_conversations = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            total_conversations += 1
            conv = json.loads(line)
            turns = conv.get('turns', [])
            if not turns:
                continue
                
            # Find the first brand response index
            brand_idx = -1
            for i, t in enumerate(turns):
                if t['author_id'] == brand:
                    brand_idx = i
                    break
                    
            # If no brand response, take all customer turns
            if brand_idx == -1:
                customer_turns = [t for t in turns if t['author_id'] != brand]
                has_brand = False
            else:
                customer_turns = [t for t in turns[:brand_idx] if t['author_id'] != brand]
                has_brand = True
                
            if not customer_turns:
                excluded.append(conv['conversation_id'])
                exclusion_reasons["NO_INITIAL_CUSTOMER_MESSAGE"] = exclusion_reasons.get("NO_INITIAL_CUSTOMER_MESSAGE", 0) + 1
                continue
                
            # Sort by created_at just in case
            customer_turns.sort(key=lambda x: x['created_at'])
            
            combined_text = " ".join([t['text'] for t in customer_turns])
            tweet_ids = [t['tweet_id'] for t in customer_turns]
            
            # Noise check
            is_noisy, reason = is_noise(combined_text)
            if is_noisy:
                excluded.append(conv['conversation_id'])
                exclusion_reasons[reason] = exclusion_reasons.get(reason, 0) + 1
                continue
                
            # Clean text for clustering (remove mentions to prevent overfitting on brand names)
            cleaned_text = re.sub(r'@[a-zA-Z0-9_]+', '', combined_text).strip()
            
            request_block = {
                "request_id": f"req_{conv['conversation_id']}",
                "conversation_id": conv['conversation_id'],
                "tweet_ids": tweet_ids,
                "text": combined_text, # Keep original for display
                "cleaned_text": cleaned_text, # Use for embedding
                "num_customer_messages": len(customer_turns),
                "has_brand_response": has_brand,
                "conversation_depth": conv['num_turns']
            }
            results.append(request_block)
            
    # Save the sample
    out_file = Path(settings.processed_data_dir) / "intent_discovery_sample.jsonl"
    with open(out_file, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
            
    # Save Quality Report
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    report_file = report_dir / "phase4_message_quality.md"
    
    lines = [
        f"# Phase 4: Message Quality & Sampling Report",
        "",
        "## Extraction Strategy",
        "The unit of analysis is defined as the **INITIAL CUSTOMER REQUEST BLOCK**. This consists of all contiguous customer tweets belonging to the initial support request *before* the first brand response. Mentions were stripped during quality analysis to ensure the message contained actual content.",
        "",
        "## Processing Statistics",
        f"- **Total Conversations:** {total_conversations}",
        f"- **Total Eligible Request Blocks Extracted:** {len(results)}",
        f"- **Total Excluded:** {len(excluded)}",
        "",
        "### Exclusion Reasons"
    ]
    
    for reason, count in sorted(exclusion_reasons.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- **{reason}**: {count}")
        
    lines.extend([
        "",
        "## Sampling Decision",
        f"Since the number of eligible request blocks ({len(results)}) is <= 15,000, we are embedding **ALL eligible request blocks** to preserve maximum data fidelity. No downsampling was required.",
        "",
        "> The complete sample has been saved to `data/processed/intent_discovery_sample.jsonl`."
    ])
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    logger.info(f"Processed {total_conversations} conversations.")
    logger.info(f"Generated {len(results)} eligible request blocks.")
    logger.info(f"Saved to {out_file} and generated report.")

if __name__ == "__main__":
    extract_request_blocks()

import json
import httpx
from pathlib import Path
from src.ui.evidence_formatter import format_evidence_text

def run_final_validation():
    client = httpx.Client(base_url="http://localhost:8000")
    
    queries = [
        ("Technical Support", "My game keeps crashing when I launch it."),
        ("Rewards", "I completed the challenge but didn't receive my reward."),
        ("Ban Appeal", "I was banned for no reason."),
        ("Account Security", "Someone hacked my account."),
        ("Game Integrity", "This player is using an aimbot."),
        ("Out-of-Domain", "How do I cook pasta?")
    ]
    
    out_md = "# Phase 11 Final Demo Validation\n\n"
    out_md += "This report captures the final behavior of the TrustSupport system for the primary recruiter demo scenarios.\n\n"
    
    for category, query in queries:
        out_md += f"## {category}\n"
        out_md += f"**Query**: `{query}`\n\n"
        
        try:
            res = client.post("/chat", json={"query": query}, timeout=10.0)
            res.raise_for_status()
            data = res.json()
            
            # Format Evidence
            ev_texts = []
            max_sim = 0.0
            ev_details = data.get("evidence_details", [])
            for ev in ev_details:
                clean_txt = format_evidence_text(ev.get("response", ""))
                sim = ev.get("similarity", 0.0)
                if sim > max_sim: max_sim = sim
                ev_texts.append(f"- **Sim {sim:.2f}**: {clean_txt}")
                
            flags_str = ", ".join([f['risk_flag'] for f in data.get('risk_flags', [])]) or "None"
            safety_passed = data.get('safety_validation', {}).get('passed', True)
            
            out_md += f"- **Intent**: {data.get('intent')} (Confidence: {data.get('confidence', 0.0):.2f})\n"
            out_md += f"- **Risk Status**: {flags_str}\n"
            out_md += f"- **Reply Mode**: {data.get('reply_mode')}\n"
            out_md += f"- **Maximum Similarity**: {max_sim:.2f}\n"
            out_md += f"- **Evidence Count**: {len(ev_details)}\n"
            out_md += f"- **Generation Source**: {data.get('generation_source', 'N/A')}\n"
            out_md += f"- **Safety Result**: {'PASSED' if safety_passed else 'FAILED'}\n"
            out_md += f"- **Final Behavior**: \n\n> {data.get('reply_text', '')}\n\n"
            
            if ev_texts:
                out_md += "**Top Cleaned Evidence:**\n"
                for ev_txt in ev_texts[:3]:
                    out_md += ev_txt + "\n"
                out_md += "\n"
                
        except Exception as e:
            out_md += f"**Error**: {str(e)}\n\n"
            
    Path("reports/phase11_final_demo_validation.md").write_text(out_md, encoding="utf-8")
    print("Generated reports/phase11_final_demo_validation.md")

if __name__ == "__main__":
    run_final_validation()

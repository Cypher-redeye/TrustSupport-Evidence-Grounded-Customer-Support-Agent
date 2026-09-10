import json
import os
import time
from tqdm import tqdm
from src.agent.support_agent import SupportAgent

def run_stress_test():
    input_file = "data/golden/end_to_end_evaluation.jsonl"
    report_file = "reports/phase8_stress_test.md"
    
    with open(input_file, "r") as f:
        queries = [json.loads(line) for line in f]
        
    # Multiply by 5 for 500 total requests
    stress_queries = queries * 5
    
    agent = SupportAgent(use_mock_generator=False)
    
    results = {
        "total": len(stress_queries),
        "success": 0,
        "exceptions": 0,
        "fallbacks": 0,
        "escalations": 0,
        "abstentions": 0
    }
    
    print(f"Running stress test on {len(stress_queries)} queries...")
    start_time = time.time()
    
    for item in tqdm(stress_queries, desc="Stress Testing"):
        try:
            res = agent.respond(item["query"])
            results["success"] += 1
            
            if res.get("fallback_used", False):
                results["fallbacks"] += 1
                
            if res["reply_mode"] == "ESCALATE":
                results["escalations"] += 1
                
            elif res["reply_mode"] == "ABSTAIN":
                results["abstentions"] += 1
                
        except Exception as e:
            results["exceptions"] += 1
            
    total_time = time.time() - start_time
    
    report_lines = [
        "# Phase 8 Stress Test Report\n",
        f"**Total Queries Processed:** {results['total']}\n",
        f"**Total Time:** {total_time:.2f} seconds\n",
        f"**Throughput:** {(results['total'] / total_time):.2f} queries/sec\n\n",
        "## Metrics\n",
        f"- **Successful Executions:** {results['success']} ({(results['success']/results['total'])*100:.1f}%)\n",
        f"- **Unhandled Exceptions:** {results['exceptions']} ({(results['exceptions']/results['total'])*100:.1f}%)\n",
        f"- **Template Fallbacks Triggered:** {results['fallbacks']} ({(results['fallbacks']/results['total'])*100:.1f}%)\n",
        f"- **Escalation Rate:** {(results['escalations']/results['total'])*100:.1f}%\n",
        f"- **Abstention Rate:** {(results['abstentions']/results['total'])*100:.1f}%\n"
    ]
    
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"Stress test report generated at {report_file}")

if __name__ == "__main__":
    run_stress_test()

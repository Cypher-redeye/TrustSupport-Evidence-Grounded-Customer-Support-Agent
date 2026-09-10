import time
import os
import csv
from statistics import mean
from src.agent.support_agent import SupportAgent

def run_benchmark():
    agent = SupportAgent(use_mock_generator=False)
    
    queries = [
        "I can't connect to the game servers today.",
        "My twitch drops are not showing up in my inventory.",
        "The game crashes when I load into a match.",
        "I completed the challenge but didn't get the camo.",
        "My game is downloading extremely slowly on Xbox."
    ] * 10 # 50 queries total
    
    results = []
    
    print("Running latency benchmark (50 iterations)...")
    for q in queries:
        start_total = time.time()
        res = agent.respond(q)
        total_time = (time.time() - start_total) * 1000
        
        metrics = res.get("metrics", {})
        results.append({
            "classification_ms": metrics.get("classification_ms", 0),
            "retrieval_ms": metrics.get("retrieval_ms", 0),
            "generation_ms": metrics.get("generation_ms", 0),
            "total_ms": total_time
        })
        
    csv_file = "results/latency_benchmark.csv"
    report_file = "reports/phase8_latency_report.md"
    
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["classification_ms", "retrieval_ms", "generation_ms", "total_ms"])
        writer.writeheader()
        writer.writerows(results)
        
    # Calculate means
    mean_class = mean([r["classification_ms"] for r in results])
    mean_ret = mean([r["retrieval_ms"] for r in results])
    mean_gen = mean([r["generation_ms"] for r in results])
    mean_total = mean([r["total_ms"] for r in results])
    
    report_lines = [
        "# Phase 8 Latency Benchmark Report\\n",
        "**Test Conditions:** 50 sequential queries (CPU/Template Fallback Generator)\\n",
        "| Component | Average Latency (ms) |",
        "|---|---|",
        f"| Intent Classification & Risk | {mean_class:.2f} ms |",
        f"| FAISS Evidence Retrieval | {mean_ret:.2f} ms |",
        f"| Reply Generation (Template) | {mean_gen:.2f} ms |",
        f"| **Total End-to-End Latency** | **{mean_total:.2f} ms** |"
    ]
    
    with open(report_file, "w") as f:
        f.write("\\n".join(report_lines).replace("\\\\n", "\\n"))
        
    print(f"Latency benchmark generated at {report_file}")

if __name__ == "__main__":
    run_benchmark()

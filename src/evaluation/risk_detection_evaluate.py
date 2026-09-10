import json
from sentence_transformers import SentenceTransformer
from src.intents.risk_detector import HybridRiskDetector

test_queries = [
    # Safe Queries
    {"query": "How do I cook pasta?", "expected": []},
    {"query": "When does the new season start?", "expected": []},
    {"query": "I can't connect to the game server", "expected": []},
    {"query": "Where is the battle pass?", "expected": []},
    {"query": "Why is my ping so high?", "expected": []},
    
    # Regex Hits
    {"query": "unban my account please", "expected": ["BAN_APPEAL"]},
    {"query": "someone hacked my profile", "expected": ["ACCOUNT_COMPROMISED"]},
    {"query": "I want a refund", "expected": ["PAYMENT"]},
    {"query": "I will sue you", "expected": ["LEGAL_THREAT"]},
    {"query": "my stats reset completely", "expected": ["PROGRESSION_DATA_LOSS"]},
    {"query": "report hacker in game", "expected": ["GAME_INTEGRITY"]},
    
    # Semantic Hits (Adversarial / Typos / Paraphrases)
    {"query": "I am filing a class action against your studio", "expected": ["LEGAL_THREAT"]},
    {"query": "my profile was accessed by someone else", "expected": ["ACCOUNT_COMPROMISED"]},
    {"query": "give me my money back immediately", "expected": ["PAYMENT"]},
    {"query": "this guy is using an aimbot in my lobby", "expected": ["GAME_INTEGRITY"]},
    {"query": "i got suspended unfairly", "expected": ["BAN_APPEAL"]},
    {"query": "contacting my attorney tomorrow", "expected": ["LEGAL_THREAT"]},
    {"query": "h4cked account help", "expected": ["ACCOUNT_COMPROMISED"]},
    {"query": "lost all my progress", "expected": ["PROGRESSION_DATA_LOSS"]},
    {"query": "he is exploiting the map glitch", "expected": ["GAME_INTEGRITY"]},
]

def evaluate_mode(detector, mode):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    escalation_tp = 0
    escalation_fn = 0
    
    for item in test_queries:
        expected = item["expected"]
        results = detector.detect(item["query"], mode=mode)
        predicted = [r["risk_flag"] for r in results]
        
        expected_set = set(expected)
        predicted_set = set(predicted)
        
        # Calculate precision/recall components
        true_positives += len(expected_set.intersection(predicted_set))
        false_positives += len(predicted_set - expected_set)
        false_negatives += len(expected_set - predicted_set)
        
        # Escalation Recall logic (Any of BAN_APPEAL, LEGAL_THREAT, ACCOUNT_COMPROMISED)
        escalation_flags = {"BAN_APPEAL", "LEGAL_THREAT", "ACCOUNT_COMPROMISED"}
        expected_escalation = bool(expected_set.intersection(escalation_flags))
        predicted_escalation = bool(predicted_set.intersection(escalation_flags))
        
        if expected_escalation:
            if predicted_escalation:
                escalation_tp += 1
            else:
                escalation_fn += 1
                
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    escalation_recall = escalation_tp / (escalation_tp + escalation_fn) if (escalation_tp + escalation_fn) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "escalation_recall": escalation_recall
    }

def run_evaluation():
    print("Loading encoder...")
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    detector = HybridRiskDetector(encoder)
    
    modes = ["regex", "semantic", "hybrid"]
    results = {}
    
    for mode in modes:
        print(f"Evaluating mode: {mode}...")
        results[mode] = evaluate_mode(detector, mode)
        
    print("\n# Risk Detection Evaluation Results")
    print("| Metric | Regex Only | Semantic Only | Hybrid |")
    print("|--------|------------|---------------|--------|")
    
    def format_row(metric_name, key):
        reg = f"{results['regex'][key]:.2%}"
        sem = f"{results['semantic'][key]:.2%}"
        hyb = f"{results['hybrid'][key]:.2%}"
        return f"| {metric_name} | {reg} | {sem} | {hyb} |"
        
    print(format_row("Precision", "precision"))
    print(format_row("Recall", "recall"))
    print(format_row("F1", "f1"))
    print(format_row("Escalation Recall", "escalation_recall"))
    
if __name__ == "__main__":
    run_evaluation()

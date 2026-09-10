import sys
from src.agent.support_agent import SupportAgent
import json

queries = [
    "I bought 2400 COD points and they haven't appeared in my account yet.",
    "I keep getting dev error 6068 when I launch the game. Help.",
    "This guy is an aimbot hacker check his profile.",
    "I got banned for no reason unban me please",
    "Where is the new gun you promised?",
    "My game crashes on startup",
    "I want a refund for the game",
    "Someone hacked my account",
    "I didn't receive my twitch drop rewards",
    "My battle pass progression is stuck at tier 50",
    "Is this game cross platform?",
    "How do I clear my cache on xbox?",
    "I want to appeal my enforcement action",
    "I am going to sue you",
    "How to cook pasta"
]

def run_eval():
    print("Initializing SupportAgent...")
    # NOTE: Set use_mock_generator=False to test actual API if GEMINI_API_KEY is in env
    # If not in env, it will safely fallback to TEMPLATE.
    agent = SupportAgent(use_mock_generator=False)
    
    for i, q in enumerate(queries):
        print(f"\n=============================================")
        print(f"QUERY {i+1}: {q}")
        print(f"=============================================")
        
        try:
            res = agent.respond(q)
            
            print(f"INTENT: {res['intent']} (Confidence: {res['confidence']:.2f})")
            print(f"RISK FLAGS: {res['risk_flags']}")
            print(f"REPLY MODE: {res['reply_mode']}")
            print(f"GENERATION SOURCE: {res['generation_source']} (Model: {res['generation_model']})")
            print(f"FALLBACK USED: {res['fallback_used']}")
            print(f"SAFETY PASSED: {res['safety_validation']['passed']}")
            print(f"EVIDENCE COUNT: {len(res['evidence_ids'])} (Max Sim: {res['max_similarity']:.2f})")
            print(f"\nREPLY:\n{res['reply_text']}")
            
        except Exception as e:
            print(f"ERROR processing query: {e}")

if __name__ == "__main__":
    run_eval()

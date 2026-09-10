import pytest
from src.intents.classifier import IntentClassifier

@pytest.fixture(scope="module")
def classifier():
    return IntentClassifier()

def test_ood_queries(classifier):
    ood_texts = [
        "How is the weather today?",
        "What is the capital of France?",
        "Can you recommend a pizza?",
        "Write me a Python sorting algorithm",
        "Hello, my name is John Doe."
    ]
    
    for text in ood_texts:
        res = classifier.predict(text)
        # OOD queries should not be HIGH confidence.
        # They should either be UNKNOWN, LOW, or at most MEDIUM if they coincidentally overlap somehow.
        assert res["confidence_level"] in ["UNKNOWN", "LOW", "MEDIUM"], f"OOD text '{text}' produced unexpected HIGH confidence."

def test_in_domain_prediction(classifier):
    # This should definitely trigger high/medium confidence
    res = classifier.predict("I bought COD points but never received them")
    assert res["intent"] == "PROGRESSION_AND_REWARDS"
    assert res["confidence_level"] in ["HIGH", "MEDIUM"]
    assert res["should_escalate"] == False

def test_escalation(classifier):
    # This should trigger escalation because of BAN_APPEAL
    res = classifier.predict("I was banned for no reason unban me")
    flag_names = [f["risk_flag"] for f in res["risk_flags"]]
    assert "BAN_APPEAL" in flag_names
    assert res["should_escalate"] == True

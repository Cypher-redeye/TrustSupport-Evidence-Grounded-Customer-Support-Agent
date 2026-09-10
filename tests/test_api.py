import pytest
from fastapi.testclient import TestClient
from src.api.main import app

def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "api_version" in data
        assert "agent_loaded" in data

def test_chat_empty_query():
    with TestClient(app) as client:
        response = client.post("/chat", json={"query": ""})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["code"] == "EMPTY_QUERY"

def test_chat_whitespace_query():
    with TestClient(app) as client:
        response = client.post("/chat", json={"query": "   "})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["code"] == "EMPTY_QUERY"

def test_chat_normal_query():
    with TestClient(app) as client:
        response = client.post("/chat", json={"query": "My game crashed when I tried to load a match"})
        assert response.status_code == 200
        data = response.json()
        assert "reply_text" in data
        assert "intent" in data
        assert data["should_escalate"] is False

def test_chat_ood_query():
    with TestClient(app) as client:
        response = client.post("/chat", json={"query": "How do I cook pasta?"})
        assert response.status_code == 200
        data = response.json()
        assert data["reply_mode"] in ["ABSTAIN", "CLARIFY"]
        assert "I don't have enough specific information" in data["reply_text"] or "Could you provide more specific details" in data["reply_text"]

def test_chat_ban_appeal():
    with TestClient(app) as client:
        response = client.post("/chat", json={"query": "I was banned for no reason unban me"})
        assert response.status_code == 200
        data = response.json()
        assert data["should_escalate"] is True
        assert data["reply_mode"] == "ESCALATE"
        
        # Check if BAN_APPEAL is in risk flags
        flags = [f["risk_flag"] for f in data.get("risk_flags", [])]
        assert "BAN_APPEAL" in flags

def test_technical_query_intent_correction():
    with TestClient(app) as client:
        response = client.post("/chat", json={"query": "My game keeps crashing when I launch it."})
        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "CONNECTIVITY_AND_ERRORS"
        assert data["reply_mode"] == "GROUNDED_REPLY"

def test_evidence_formatter():
    from src.ui.evidence_formatter import format_evidence_text
    raw = "@619546 Please restart the game. ^RK"
    assert format_evidence_text(raw) == "Please restart the game."
    assert format_evidence_text("@123 Hello") == "Hello"
    assert format_evidence_text("Hi ^A") == "Hi"
    assert format_evidence_text("Nothing to format") == "Nothing to format"

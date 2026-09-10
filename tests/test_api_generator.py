import pytest
import os
from unittest.mock import MagicMock
from src.agent.support_agent import SupportAgent
from src.generation.api_generator import APIGenerator

@pytest.fixture
def empty_env(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
def test_no_api_key_fallback(empty_env):
    # Without an API key, APIGenerator raises ValueError which SupportAgent catches
    agent = SupportAgent(use_mock_generator=False)
    # The normal query shouldn't hit escalate or abstain, so it will attempt API generation
    res = agent.respond("I keep getting dev error 6068 when I launch the game.")
    
    assert res["fallback_used"] == True
    assert res["generation_source"] == "TEMPLATE"
    assert res["generation_model"] is None

def test_mock_api_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    
    agent = SupportAgent(use_mock_generator=False)
    
    # Mock the response
    mock_response = MagicMock()
    mock_response.text = "This is a grounded response."
    
    mock_generate = MagicMock(return_value=mock_response)
    agent.primary_generator.client.models.generate_content = mock_generate
    
    res = agent.respond("I keep getting dev error 6068 when I launch the game.")
    
    # Since it's safe (no hallucinated URLs or banned words)
    assert res["fallback_used"] == False
    assert res["generation_source"] == "API"
    assert res["reply_text"] == "This is a grounded response."

def test_api_exception_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    
    agent = SupportAgent(use_mock_generator=False)
    
    # Mock the response to raise an exception
    mock_generate = MagicMock(side_effect=Exception("API Timeout"))
    agent.primary_generator.client.models.generate_content = mock_generate
    
    res = agent.respond("I keep getting dev error 6068 when I launch the game.")
    
    assert res["fallback_used"] == True
    assert res["generation_source"] == "TEMPLATE"

def test_api_empty_response_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    
    agent = SupportAgent(use_mock_generator=False)
    
    # Mock the response to return empty text
    mock_response = MagicMock()
    mock_response.text = ""
    
    mock_generate = MagicMock(return_value=mock_response)
    agent.primary_generator.client.models.generate_content = mock_generate
    
    res = agent.respond("I keep getting dev error 6068 when I launch the game.")
    
    assert res["fallback_used"] == True
    assert res["generation_source"] == "TEMPLATE"

def test_api_safety_hallucination_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    
    agent = SupportAgent(use_mock_generator=False)
    
    # Mock the response to return a hallucinated URL
    mock_response = MagicMock()
    mock_response.text = "Check out this link: https://scam-site.com/free-points"
    
    mock_generate = MagicMock(return_value=mock_response)
    agent.primary_generator.client.models.generate_content = mock_generate
    
    res = agent.respond("I keep getting dev error 6068 when I launch the game.")
    
    assert res["fallback_used"] == True
    assert res["safety_validation"]["passed"] == False
    assert res["generation_source"] == "TEMPLATE"

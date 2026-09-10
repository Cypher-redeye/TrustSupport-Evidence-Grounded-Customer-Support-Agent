import pytest
from src.agent.support_agent import SupportAgent

@pytest.fixture(scope="module")
def agent():
    return SupportAgent(use_mock_generator=True)
    
def test_agent_ban_appeal(agent):
    res = agent.respond("I got banned for no reason unban me")
    assert res["reply_mode"] == "ESCALATE"
    assert res["should_escalate"] == True
    assert "We cannot discuss enforcement actions" in res["reply_text"]
    assert res["generation_source"] == "TEMPLATE"
    
def test_agent_ood(agent):
    res = agent.respond("How do I cook pasta?")
    assert res["reply_mode"] == "ABSTAIN"
    assert "I don't have enough specific information" in res["reply_text"]
    assert res["generation_source"] == "TEMPLATE"

def test_agent_normal_query(agent):
    # This query should reliably hit a Grounded or Cautious reply since it's highly relevant to the dataset
    res = agent.respond("I keep getting dev error 6068 when I launch the game. Help.")
    assert res["reply_mode"] in ["GROUNDED_REPLY", "CAUTIOUS_REPLY", "CLARIFY"]
    assert res["should_escalate"] == False
    
def test_agent_game_integrity(agent):
    res = agent.respond("This guy is a hacker check his profile")
    # Game Integrity is cautious reply, which goes to API generation.
    assert res["reply_mode"] in ["CAUTIOUS_REPLY", "CLARIFY", "ABSTAIN"]
    if res["reply_mode"] == "CAUTIOUS_REPLY":
        assert res["generation_source"] == "MOCK"

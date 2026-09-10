import pytest
from src.generation.reply_router import ReplyRouter

def test_escalate_severe_risk():
    mode = ReplyRouter.determine_mode(
        intent="UNKNOWN",
        confidence_level="UNKNOWN",
        risk_flags=["BAN_APPEAL"],
        retrieval_status="SUCCESS",
        max_similarity=0.99
    )
    assert mode == "ESCALATE"
    
def test_abstain_no_evidence():
    mode = ReplyRouter.determine_mode(
        intent="PURCHASE_AND_BILLING",
        confidence_level="HIGH",
        risk_flags=[],
        retrieval_status="NO_RELIABLE_EVIDENCE",
        max_similarity=0.0
    )
    assert mode == "ABSTAIN"
    
def test_abstain_low_similarity():
    mode = ReplyRouter.determine_mode(
        intent="PURCHASE_AND_BILLING",
        confidence_level="HIGH",
        risk_flags=[],
        retrieval_status="SUCCESS",
        max_similarity=0.35  # < 0.40
    )
    assert mode == "ABSTAIN"

def test_clarify_ambiguous():
    mode = ReplyRouter.determine_mode(
        intent="ACCOUNT_AND_REWARDS",
        confidence_level="LOW",
        risk_flags=[],
        retrieval_status="SUCCESS",
        max_similarity=0.45  # < 0.50 and LOW confidence
    )
    assert mode == "CLARIFY"
    
def test_cautious_game_integrity():
    mode = ReplyRouter.determine_mode(
        intent="EXPLOIT_AND_HACKER_REPORT",
        confidence_level="HIGH",
        risk_flags=["GAME_INTEGRITY"],
        retrieval_status="SUCCESS",
        max_similarity=0.80
    )
    assert mode == "CAUTIOUS_REPLY"
    
def test_cautious_low_confidence():
    mode = ReplyRouter.determine_mode(
        intent="DIGITAL_ACCESS_AND_DOWNLOAD",
        confidence_level="LOW",
        risk_flags=[],
        retrieval_status="SUCCESS",
        max_similarity=0.75  # > 0.50 but LOW confidence
    )
    assert mode == "CAUTIOUS_REPLY"
    
def test_grounded_reply():
    mode = ReplyRouter.determine_mode(
        intent="DIGITAL_ACCESS_AND_DOWNLOAD",
        confidence_level="HIGH",
        risk_flags=[],
        retrieval_status="SUCCESS",
        max_similarity=0.85
    )
    assert mode == "GROUNDED_REPLY"

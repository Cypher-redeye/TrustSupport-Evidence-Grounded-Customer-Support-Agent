import pytest
from src.generation.safety import SafetyValidator

def test_safety_banned_terms():
    evidence = [{"historical_brand_response": "We can help you."}]
    
    assert SafetyValidator.validate("I can process a refund for you.", evidence) == False
    assert SafetyValidator.validate("I will unban your account.", evidence) == False
    assert SafetyValidator.validate("I guarantee it will work.", evidence) == False
    assert SafetyValidator.validate("Please restart your console.", evidence) == True

def test_safety_url_filtering():
    evidence = [{"historical_brand_response": "Check out this link: https://support.activision.com/articles/clear-cache"}]
    
    # Generated URL matches exactly what's in evidence
    assert SafetyValidator.validate("Go here: https://support.activision.com/articles/clear-cache", evidence) == True
    
    # Generated URL is slightly off / invented
    assert SafetyValidator.validate("Go here: https://support.activision.com/articles/fake-link", evidence) == False
    
    # Generated a random domain
    assert SafetyValidator.validate("Check out http://scamsite.com", evidence) == False

def test_safety_support_domain_without_http():
    evidence = [{"historical_brand_response": "Visit support.activision.com"}]
    
    assert SafetyValidator.validate("Go to support.activision.com", evidence) == True
    assert SafetyValidator.validate("Go to support.activision.com/fake", evidence) == False

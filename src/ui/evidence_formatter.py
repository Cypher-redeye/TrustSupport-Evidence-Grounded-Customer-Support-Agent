import re

def format_evidence_text(text: str) -> str:
    """
    Cleans raw ATVIAssist responses for frontend presentation.
    Removes @mention IDs at the start and ^XX signatures at the end.
    Example: '@619546 Please restart the game. ^RK' -> 'Please restart the game.'
    """
    if not text:
        return ""
    
    # Remove leading @ID tags (e.g., @123456)
    text = re.sub(r'^@\d+\s+', '', text)
    
    # Remove trailing ^XX signatures (e.g., ^RK, ^J, ^ABC)
    text = re.sub(r'\s*\^[A-Za-z0-9]+$', '', text)
    
    return text.strip()

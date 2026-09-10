from src.config import settings
import os

def test_directories_created():
    assert os.path.exists(settings.raw_data_dir)
    assert os.path.exists(settings.processed_data_dir)
    assert os.path.exists(settings.golden_data_dir)

def test_default_values():
    assert settings.llm_provider == "gemini"
    assert settings.random_seed == 42

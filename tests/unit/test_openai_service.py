import pytest
from unittest.mock import patch
from openai_service import OpenAIService
from config import config
from utils import handle_api_error

@patch('openai_service.openai.Completion.create')
def test_translate_text_success(mock_openai_create):
    """Tests successful text translation."""
    mock_openai_create.return_value = {
        "choices": [
            {"text": "This is a translation."}
        ]
    }
    ai_service = OpenAIService()
    translation = ai_service.translate_text(text="Hello world", target_language="fr")
    assert translation == "This is a translation."

@patch('openai_service.openai.Completion.create', side_effect=openai.error.OpenAIError("API Error"))
def test_translate_text_failure(mock_openai_create):
    """Tests handling OpenAI API errors during translation."""
    ai_service = OpenAIService()
    with pytest.raises(Exception):
        ai_service.translate_text(text="Hello world", target_language="fr")

@patch('openai_service.openai.Completion.create')
def test_generate_text_success(mock_openai_create):
    """Tests successful text generation."""
    mock_openai_create.return_value = {
        "choices": [
            {"text": "This is generated text."}
        ]
    }
    ai_service = OpenAIService()
    generated_text = ai_service.generate_text(prompt="Write a short story.")
    assert generated_text == "This is generated text."

@patch('openai_service.openai.Completion.create', side_effect=openai.error.OpenAIError("API Error"))
def test_generate_text_failure(mock_openai_create):
    """Tests handling OpenAI API errors during text generation."""
    ai_service = OpenAIService()
    with pytest.raises(Exception):
        ai_service.generate_text(prompt="Write a short story.")
from typing import Optional
import openai
from .config import config
from .utils import handle_api_error

class OpenAIService:
    """
    A service class for interacting with the OpenAI API.

    This class handles API requests, processes responses, and provides 
    a simplified interface to the OpenAI API.

    Attributes:
        api_key (str): The OpenAI API key.
    """

    def __init__(self):
        self.api_key = config.get_openai_api_key()

    def translate_text(self, text: str, target_language: str, model: Optional[str] = "text-davinci-003") -> str:
        """
        Translates text using the OpenAI API.

        Args:
            text (str): The text to translate.
            target_language (str): The target language code (e.g., "fr" for French, "es" for Spanish).
            model (str, optional): The OpenAI model to use for translation. Defaults to "text-davinci-003".

        Returns:
            str: The translated text.

        Raises:
            Exception: If an error occurs during API communication or response processing.
        """
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=f"Translate this text into {target_language}: {text}",
            )
            return response.choices[0].text
        except Exception as e:
            handle_api_error(e)

    def generate_text(self, prompt: str, model: Optional[str] = "text-davinci-003", max_tokens: Optional[int] = 1000) -> str:
        """
        Generates text using the OpenAI API.

        Args:
            prompt (str): The prompt for text generation.
            model (str, optional): The OpenAI model to use for text generation. Defaults to "text-davinci-003".
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1000.

        Returns:
            str: The generated text.

        Raises:
            Exception: If an error occurs during API communication or response processing.
        """
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
            )
            return response.choices[0].text
        except Exception as e:
            handle_api_error(e)
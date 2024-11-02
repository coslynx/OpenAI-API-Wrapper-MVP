from pydantic import BaseModel

from .openai_service import OpenAIService

class TextRequest(BaseModel):
    text: str
    task: str = "translate"
    model: str = "text-davinci-003"

class TranslationResponse(BaseModel):
    translation: str

class SummarizationRequest(BaseModel):
    text: str
    model: str = "text-davinci-003"
    max_tokens: int = 1000

class SummarizationResponse(BaseModel):
    summary: str

class CodeGenerationRequest(BaseModel):
    prompt: str
    model: str = "code-davinci-002"
    language: str = "python"

class CodeGenerationResponse(BaseModel):
    code: str

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"

class ChatResponse(BaseModel):
    response: str
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import openai
from sqlalchemy.orm import Session
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import RequestModel, ResponseModel, ErrorLog
from .config import config
from .utils import generate_jwt, validate_jwt
from .openai_service import OpenAIService
from .schemas import TextRequest, TranslationResponse
from .db import get_db

app = FastAPI()

openai.api_key = config.get_openai_api_key()

oauth2_scheme = HTTPBearer()

@app.on_event("startup")
async def startup_event():
    openai.api_key = config.get_openai_api_key()

@app.post("/ai")
async def process_ai_request(request: TextRequest, db: Session = Depends(get_db)):
    try:
        # Authentication (Optional)
        # user = validate_jwt(token) # if JWT authentication is implemented
        
        ai_service = OpenAIService()
        
        # Map user request to AI task
        if request.task == "translate":
            response = ai_service.translate_text(text=request.text, target_language=request.target_language)
            
            # Store request and response in the database
            db_request = RequestModel(task=request.task, input_text=request.text, user_id=user.id)  # Add user_id if JWT is used
            db_response = ResponseModel(request_id=db_request.id, response_text=response)
            db.add(db_request)
            db.add(db_response)
            db.commit()
            
            return {"translation": response}
        
        # Implement other AI tasks similarly
        
        else:
            raise HTTPException(status_code=400, detail="Invalid task")
            
    except Exception as e:
        # Log error
        error_log = ErrorLog(message=str(e))
        db.add(error_log)
        db.commit()
        raise HTTPException(status_code=500, detail="Internal server error")
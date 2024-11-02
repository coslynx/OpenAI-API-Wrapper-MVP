import os
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

class Config:
    """
    Configuration class for the AI Wrapper application.

    Loads environment variables from the .env file and provides methods for
    accessing configuration settings.
    """
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.database_uri = self.get_database_uri()
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY", None) 
        self.server_port = int(os.getenv("PORT", 8000))  

    def get_database_uri(self):
        """
        Constructs the PostgreSQL database connection string using environment variables.

        Returns:
            str: The database connection URI.
        """
        return f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

    def get_openai_api_key(self):
        """
        Returns the OpenAI API key from the environment variable.

        Returns:
            str: The OpenAI API key.
        """
        return self.openai_api_key 

    def get_database_uri(self):
        """
        Returns the PostgreSQL database connection URI.

        Returns:
            str: The database connection URI.
        """
        return self.database_uri

    def get_jwt_secret_key(self):
        """
        Returns the JWT secret key from the environment variable.

        Returns:
            str: The JWT secret key.
        """
        return self.jwt_secret_key

    def get_server_port(self):
        """
        Returns the port number for the FastAPI application.

        Returns:
            int: The server port.
        """
        return self.server_port

# Create the FastAPI app instance
app = FastAPI()

# Inject the configuration into the application
config = Config()

# Example usage in main.py
@app.on_event("startup")
async def startup_event():
    # Access configuration values from Config
    openai.api_key = config.get_openai_api_key()  
    # ... other setup tasks using configuration values

# ... rest of the application code
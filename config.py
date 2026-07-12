import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key-12345')
    
    # Check fallback option
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
    # Fix for Render/Heroku style URLs
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f"sqlite:///{os.path.join(BASE_DIR, 'prep_ai.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Gemini API Key Config
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "ranchanadevi07@gmail.com"
    MAIL_PASSWORD = "buik jesc aveq rrwy"
    MAIL_DEFAULT_SENDER = "ranchanadevi07@gmail.com"

# Create uploads directory if not exists
os.makedirs(os.path.join(BASE_DIR, 'uploads'), exist_ok=True)

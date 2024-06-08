import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG", False)
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")
    MODEL = os.getenv("MODEL", "gpt-3.5-turbo")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    EMBEDDING_DIM = os.getenv("EMBEDDING_DIM", "1536")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1024"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "20"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
    POSTGRES_DB_HOST = os.getenv("POSTGRES_DB_HOST")
    POSTGRES_DB_PORT = int(os.getenv("POSTGRES_DB_PORT", 5432))
    SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}"


config = Config

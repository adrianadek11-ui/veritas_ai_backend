import os

class Settings:
    PROJECT_NAME: str = "Veritas Media C2"
    VERSION: str = "3.0.0-Standalone"
    USE_REDIS_CACHE: bool = False  # Wymuszamy lokalny bufor pamięci, zero błędów sieciowych
    STORAGE_MODE: str = "GHOST_CLOUD_STANDALONE"

settings = Settings()

import os

class Config:
    DB_NAME = os.getenv("DB_NAME", "urbannexus")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Meet2701")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "aeb8cb774b160764b4aaa2015c0e3a9b")
    
    # Path settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data_sources")

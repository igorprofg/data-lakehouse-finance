import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # CoinGecko
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

    # PostgreSQL
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_LOCAL_PORT = os.getenv("POSTGRES_LOCAL_PORT")

    # Data Lake
    RAW_DATA_PATH = "data/raw/coingecko"
    TRUSTED_DATA_PATH = "data/trusted/market"
    REFINED_DATA_PATH = "data/refined/analytics"

    # Logs
    LOG_LEVEL = "INFO"
    LOG_PATH = "airflow/logs"
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    RAW_DATA_PATH = "data/raw/coingecko"
    TRUSTED_DATA_PATH = "data/trusted/market"
    REFINED_DATA_PATH = "data/refined/analytics"
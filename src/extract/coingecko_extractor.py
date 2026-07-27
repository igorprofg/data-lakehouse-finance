import json
from datetime import datetime
from pathlib import Path

import requests

from src.utils.config import Config
from src.utils.logger import Logger


class CoinGeckoExtractor:

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self.api_key = Config.COINGECKO_API_KEY
        self.raw_path = Path(Config.RAW_DATA_PATH)

        self.raw_path.mkdir(parents=True, exist_ok=True)

        self.logger = Logger.get_logger(self.__class__.__name__)

    def extract_market_data(self):
        self.logger.info("Starting market data extraction.")

        endpoint = f"{self.BASE_URL}/coins/markets"

        headers = {
            "x-cg-demo-api-key": self.api_key
        }

        params = {
            "vs_currency": "usd",
            "ids": "bitcoin,ethereum,solana,xrp,cardano"
        }

        self.logger.info("Sending request to CoinGecko API.")

        response = requests.get(
            endpoint,
            headers=headers,
            params=params
        )

        response.raise_for_status()

        self.logger.info("Market data extracted successfully.")

        return response.json()

    def save_raw_data(self, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_name = f"{timestamp}.json"
        file_path = self.raw_path / file_name

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        self.logger.info(f"Raw data saved at: {file_path}")

    def run(self):
        self.logger.info("Starting CoinGecko extraction pipeline.")

        data = self.extract_market_data()
        self.save_raw_data(data)

        self.logger.info("CoinGecko extraction pipeline finished successfully.")


if __name__ == "__main__":
    extractor = CoinGeckoExtractor()
    extractor.run()
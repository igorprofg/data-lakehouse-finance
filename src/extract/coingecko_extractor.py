import requests
import json
from pathlib import Path
from datetime import datetime 

from src.utils.config import Config

class CoinGeckoExtractor:
    BASE_URL = "https://api.coingecko.com/api/v3"
    def __init__(self): 
        self.api_key = Config.COINGECKO_API_KEY
        self.raw_path = Path(Config.RAW_DATA_PATH)

        # cria diretório caso não exista
        self.raw_path.mkdir(parents=True, exist_ok=True)   

    def extract_market_data(self):
             endpoint = f"{self.BASE_URL}/coins/markets"

             headers = {
                   "x-cg-demo-api-key": self.api_key
             }

             params = {
                   "vs_currency":"usd", 
                   "ids":"bitcoin,etherum,solana,xrp,cardano"

             }

             response = requests.get(
                  endpoint,
                  headers = headers,
                  params = params
             )

             response.raise_for_status()

             return response.json()
    
    def save_raw_data(self, data): 
          timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
          file_name = f"{timestamp}.json"
          file_path = self.raw_path / file_name

          with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

          print(f"Raw data saved at: {file_path}") 

    def run(self):
          data = self.extract_market_data()
          self.save_raw_data(data)

if __name__ == "__main__":
    extractor = CoinGeckoExtractor()
    extractor.run()
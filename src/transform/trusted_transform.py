from pathlib import Path

import polars as pl

from src.utils.config import Config
from src.utils.logger import Logger


class TrustedTransformer:

    def __init__(self):
        self.raw_path = Path(Config.RAW_DATA_PATH)
        self.trusted_path = Path(Config.TRUSTED_DATA_PATH)

        self.trusted_path.mkdir(parents=True, exist_ok=True)

        self.logger = Logger.get_logger(self.__class__.__name__)

    def get_latest_raw_file(self):
        files = list(self.raw_path.glob("*.json"))

        if not files:
            raise FileNotFoundError("No raw data files found.")

        latest_file = max(files, key=lambda file: file.stat().st_mtime)

        self.logger.info(f"Latest raw file found: {latest_file.name}")

        return latest_file

    def transform_to_trusted(self):
        self.logger.info("Starting trusted transformation.")

        latest_file = self.get_latest_raw_file()

        df = pl.read_json(latest_file)

        df = df.select([
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_24h",
            "last_updated"
        ])

        df = df.with_columns([
            pl.col("current_price").cast(pl.Float64),
            pl.col("market_cap").cast(pl.Float64),
            pl.col("total_volume").cast(pl.Float64),
            pl.col("price_change_percentage_24h").cast(pl.Float64),
            pl.col("last_updated").cast(pl.String)
        ])

        df = df.drop_nulls()

        self.logger.info("Trusted transformation completed successfully.")

        return df

    def save_trusted_data(self, df):
        file_path = self.trusted_path / "market_trusted.parquet"

        df.write_parquet(file_path)

        self.logger.info(f"Trusted data saved at: {file_path}")

    def run(self):
        self.logger.info("Starting Trusted pipeline.")

        df = self.transform_to_trusted()
        self.save_trusted_data(df)

        self.logger.info("Trusted pipeline finished successfully.")


if __name__ == "__main__":
    transformer = TrustedTransformer()
    transformer.run()
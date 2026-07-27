from pathlib import Path

import polars as pl
import psycopg

from src.utils.config import Config
from src.utils.logger import Logger


class PostgresLoader:

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)

        self.trusted_file = (
            Path(Config.TRUSTED_DATA_PATH)
            / "market_trusted.parquet"
        )

        self.connection = None

    def connect(self):
        self.logger.info("Connecting to PostgreSQL...")

        self.connection = psycopg.connect(
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            dbname=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD
        )

        self.logger.info("Connection established successfully.")

    def read_trusted_data(self):
        self.logger.info("Reading trusted parquet file...")

        df = pl.read_parquet(self.trusted_file)

        self.logger.info(f"{df.height} records loaded from Trusted Layer.")

        return df

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Connection closed.")

    def run(self):

        self.connect()

        df = self.read_trusted_data()

        self.logger.info("Infrastructure validation completed successfully.")

        self.close_connection()


if __name__ == "__main__":
    loader = PostgresLoader()
    loader.run()
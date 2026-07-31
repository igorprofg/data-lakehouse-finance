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
            port=Config.POSTGRES_LOCAL_PORT,
            dbname=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD
        )

        self.logger.info("Connection established successfully.")

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    current_database(),
                    current_user,
                    inet_server_addr(),
                    inet_server_port(),
                    current_setting('data_directory'),
                    pg_postmaster_start_time();
            """)

            connection_info = cursor.fetchone()

        self.logger.info(
            f"Database: {connection_info[0]}"
        )

        self.logger.info(
            f"User: {connection_info[1]}"
        )

        self.logger.info(
            f"Server address: {connection_info[2]}"
        )

        self.logger.info(
            f"Server port: {connection_info[3]}"
        )

        self.logger.info(
            f"Data directory: {connection_info[4]}"
        )

        self.logger.info(
            f"Server start time: {connection_info[5]}"
        )

    def read_trusted_data(self):
        self.logger.info("Reading trusted parquet file...")

        df = pl.read_parquet(self.trusted_file)

        self.logger.info(
            f"{df.height} records loaded from Trusted Layer."
        )

        return df

    def load_assets(self, df):
        self.logger.info("Starting assets loading...")

        assets = df.select([
            "id",
            "symbol",
            "name"
        ])

        asset_ids = {}

        with self.connection.cursor() as cursor:

            for row in assets.iter_rows(named=True):

                cursor.execute(
                    """
                    INSERT INTO assets (
                        coingecko_id,
                        symbol,
                        name
                    )
                    VALUES (%s, %s, %s)
                    ON CONFLICT (coingecko_id)
                    DO UPDATE SET
                        symbol = EXCLUDED.symbol,
                        name = EXCLUDED.name
                    RETURNING asset_id;
                    """,
                    (
                        row["id"],
                        row["symbol"],
                        row["name"]
                    )
                )

                asset_id = cursor.fetchone()[0]

                asset_ids[row["id"]] = asset_id

        self.connection.commit()

        self.logger.info(
            f"{len(asset_ids)} assets loaded successfully."
        )

        return asset_ids

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Connection closed.")

    def run(self):

        self.connect()

        try:
            df = self.read_trusted_data()

            self.load_assets(df)

            self.logger.info(
                "Assets loading completed successfully."
            )

        except Exception:
            if self.connection:
                self.connection.rollback()

            self.logger.exception(
                "An error occurred during assets loading."
            )

            raise

        finally:
            self.close_connection()


if __name__ == "__main__":
    loader = PostgresLoader()
    loader.run()
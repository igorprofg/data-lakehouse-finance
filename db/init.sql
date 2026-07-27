-- =====================================================
-- Lakehouse Finance
-- Database Initialization Script
-- =====================================================

-- Remove tabelas existentes (caso existam)
DROP TABLE IF EXISTS market_snapshots CASCADE;
DROP TABLE IF EXISTS assets CASCADE;

-- =====================================================
-- Tabela: assets
-- Armazena informações estáticas das criptomoedas.
-- =====================================================

CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    coingecko_id VARCHAR(100) NOT NULL UNIQUE,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- =====================================================
-- Tabela: market_snapshots
-- Armazena os dados coletados a cada execução do pipeline.
-- =====================================================

CREATE TABLE market_snapshots (
    snapshot_id BIGSERIAL PRIMARY KEY,

    asset_id INTEGER NOT NULL,

    current_price NUMERIC(20,8) NOT NULL,
    market_cap NUMERIC(30,2) NOT NULL,
    total_volume NUMERIC(30,2) NOT NULL,
    price_change_percentage_24h NUMERIC(10,4),

    market_last_updated TIMESTAMP NOT NULL,

    ingestion_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_market_asset
        FOREIGN KEY(asset_id)
        REFERENCES assets(asset_id)
);
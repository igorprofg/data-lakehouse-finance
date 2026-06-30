<strong><h1>Arquitetura do projeto</h1></strong>
    
    lakehouse_finance/
    │── README.md
    │── .env
    │── .gitignore
    │── requirements.txt
    │── docker-compose.yml
    │
    ├── airflow/
    │   ├── dags/
    │   │   └── coingecko_pipeline.py
    │   │
    │   ├── logs/
    │   │
    │   ├── plugins/
    │   │
    │   └── config/
    │
    ├── src/
    │   ├── extract/
    │   │   └── coingecko_extractor.py
    │   │
    │   ├── transform/
    │   │   ├── trusted_transform.py
    │   │   └── refined_transform.py
    │   │
    │   ├── load/
    │   │   └── postgres_loader.py
    │   │
    │   ├── utils/
    │   │   ├── config.py
    │   │   ├── logger.py
    │   │   └── helpers.py
    │   │
    │   └── models/
    │       └── schemas.py
    │
    ├── data/
    │   ├── raw/
    │   │   └── coingecko/
    │   │
    │   ├── trusted/
    │   │   └── market/
    │   │
    │   └── refined/
    │       └── analytics/
    │
    ├── db/
    │   ├── init.sql
    │   └── migrations/
    │
    ├── dbt/
    │   ├── models/
    │   │   ├── staging/
    │   │   └── marts/
    │   │
    │   ├── seeds/
    │   └── dbt_project.yml
    │
    ├── tests/
    │   ├── test_extract.py
    │   ├── test_transform.py
    │   └── test_load.py
    │
    └── docs/
        └── architecture.md
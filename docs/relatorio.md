<h1>Dia 01:</h1> 
<strong>feat: setup initial project architecture, directory structure and documentation.
Inicialmente foi criada a arquitetura do projeto, documentação inicial, database no postgreSQL e conteúdos nos arquivos:</strong>

<br>

1 - .env 

2 - requirements.txt 

3 - .gitignore 

4 - docker-compose.yml

<br>

<h1>Dificuldades</h1>

Nenhuma

<br>

<h1>Próximos passos:</h1>

- subir containers
- testar Airflow
- criar config.py
- criar extractor da API
- salvar primeiro JSON em raw

<br>

<h1>Dia 02:</h1> 
<strong>feat: inicialização da infraestrutura com Docker e validação do Airflow</strong>

<br>

Fluxo:

docker compose up -d

↓

Container inicia

↓

    Airflow Webserver sobe

    ↓

    Porta 8080 é exposta

    ↓

    Interface disponível no navegador

<br>

Disponível em: localhost:8080

<br>

<h3>arquivo: src/utils/config.py</h3>

Esse arquivo vai centralizar toda leitura de configuração do projeto.

Em vez de ficar espalhando:

    os.getenv(...)

em vários arquivos, ele vai concentrar tudo.

Então ele carrega automaticamente o arquivo:

    .env

Estrutura lógica

    .env

    ↓

    config.py

    ↓

    extractor.py

    ↓

    Airflow DAG

    ↓

    transform.py

    ↓

    load.py

<br>

# Documentação Técnica: Ingestão de Dados com CoinGeckoExtractor

Abaixo detalho o funcionamento das principais funções que desenvolvi para o processo de ingestão de dados brutos na camada **Raw** do meu Data Lakehouse.

---

## Função: `save_raw_data(self, data)`

Esta função é a responsável por salvar os dados brutos que extraio da API diretamente na camada **Raw** do meu Data Lakehouse.

### Fluxo de Execução

- Dados extraídos da API
- ↓
- Geração de um timestamp único
- ↓
- Criação do nome do arquivo
- ↓
- Salvamento do JSON bruto
- ↓
- Persistência concluída na camada Raw

### Objetivo Principal

Garantir o armazenamento dos dados exatamente como foram recebidos da API, mantendo a integridade da informação sem aplicar nenhuma transformação nesta etapa.

### Etapas de Execução

**1. Geração do timestamp**

```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

- Crio um identificador único baseado na data e hora exatas da execução.
- Exemplo: `20260701_154512`
- Isso impede que execuções futuras sobrescrevam os arquivos já existentes.

**2. Criação do nome do arquivo**

```python
file_name = f"{timestamp}.json"
```

- Exemplo: `20260701_154512.json`

**3. Montagem do caminho (Path)**

```python
file_path = self.raw_path / file_name
```

- Resultado esperado: `data/raw/coingecko/20260701_154512.json`

**4. Escrita do arquivo JSON**

```python
json.dump(data, file, indent=4)
```

- Salvo o conteúdo bruto mantendo uma indentação legível para auditoria.

### Conceito no Lakehouse

Esta função representa a base da minha Raw Layer (Camada Bruta). Nela, garanto que os dados permaneçam:

- Totalmente brutos
- Sem processos de limpeza
- Sem qualquer tipo de transformação
- 100% auditáveis para o caso de reprocessamentos futuros

---

## Função: `run(self)`

Esta função atua como o ponto principal e o motor de execução do meu extrator. Desenvolvi essa rotina para orquestrar de forma simplificada todo o fluxo de ingestão.

### Fluxo de Execução

- `extract_market_data()`
- ↓
- `save_raw_data()`

### Etapas de Orquestração

**Etapa 1: Extração**

```python
data = self.extract_market_data()
```

O meu script é responsável por:

- Chamar a API externa do CoinGecko.
- Buscar as cotações atuais e dados financeiros das moedas selecionadas.
- Retornar a resposta completa em formato JSON.

**Etapa 2: Persistência**

```python
self.save_raw_data(data)
```

- Eu envio o JSON retornado diretamente para a minha função de salvamento, persistindo os dados na camada Raw sem intermediários.

<br>

<h1>Dificuldades</h1>

* Durante a execução inicial do extractor, ocorreu o erro `No module named src`, causado pelo contexto de execução do Python e resolução de imports absolutos.
* A correção foi ajustar a forma de execução do módulo a partir da raiz do projeto, garantindo que a estrutura de pacotes fosse corretamente reconhecida.

<br>

<h1>Próximos passos:</h1>

* criar transformação da camada Trusted com Polars
* padronizar schema dos dados extraídos
* tratar tipos de dados
* validar campos nulos
* salvar arquivos em formato Parquet
* iniciar modelagem das tabelas no PostgreSQL
* preparar integração com Airflow DAG

<br>

<h1>Dia 03:</h1> 
<strong>feat:</strong>

<br>

* padronizar schema
* corrigir tipos
* remover inconsistências
* validar nulos
* persistir em formato analítico

<br>

# Documentação Técnica: Camada Trusted

Nesta etapa foi implementada a primeira versão da **Trusted Layer** do Data Lakehouse.

## Objetivo

A camada Trusted é responsável por transformar os dados brutos (Raw) em dados padronizados e confiáveis para as próximas etapas do pipeline.

## Fluxo

CoinGecko API

↓

Raw Layer (JSON)

↓

Trusted Transformer

↓

Seleção de colunas

↓

Padronização dos tipos de dados

↓

Remoção de registros nulos

↓

Persistência em Parquet

## O que foi implementado

- Leitura automática do arquivo JSON mais recente da camada Raw.
- Seleção apenas das colunas relevantes para análise.
- Conversão dos tipos de dados utilizando Polars.
- Remoção de registros contendo valores nulos.
- Persistência dos dados na camada Trusted em formato **Parquet**.

## Resultado

Arquivo gerado em:

`data/trusted/market/market_trusted.parquet`

## Observação

Para executar o módulo foi utilizado:

```bash
python -m src.transform.trusted_transform
```

A execução como módulo garante que o pacote `src` seja reconhecido corretamente pelo Python.

<br>

No arquivo:

```bash
db\init.sql
```

Ao invés de FLOAT, usei:

**NUMERIC(20,8)**

Porque valores financeiros exigem precisão. Isso evita problemas de arredondamento.

**BIGSERIAL**

Na tabela de snapshots. Porque ela vai crescer bastante.Cada execução do pipeline gera novos registros.

**SERIAL**

Na tabela de assets. Ela praticamente não cresce.

**Hoje temos:**

- Bitcoin
- Ethereum
- Solana
- XRP
- Cardano

# Documentação Técnica: PostgreSQL Loader (Etapa 1)

Nesta etapa foi criada a infraestrutura inicial da camada **Load** do pipeline ETL.

## Objetivo

Preparar o projeto para carregar os dados da camada Trusted para o PostgreSQL.

Nesta primeira versão, o foco não foi inserir dados no banco, mas validar toda a infraestrutura necessária para essa operação.

## Fluxo

Trusted Layer (Parquet)

↓

PostgresLoader

↓

Conexão com PostgreSQL

↓

Leitura do arquivo Parquet

↓

Validação da infraestrutura

↓

Encerramento da conexão

## O que foi implementado

- Criação da classe `PostgresLoader`.
- Configuração da conexão utilizando `psycopg`.
- Leitura do arquivo `market_trusted.parquet` utilizando Polars.
- Centralização do logging através do `logger.py`.
- Encerramento seguro da conexão com o banco de dados.

## Arquitetura

O módulo foi dividido em pequenas responsabilidades, facilitando manutenção e testes.

- `connect()` → estabelece conexão com o PostgreSQL.
- `read_trusted_data()` → lê os dados da camada Trusted.
- `close_connection()` → encerra a conexão.
- `run()` → orquestra toda a execução do loader.

## Resultado

Ao final desta etapa, o pipeline já consegue:

- conectar ao PostgreSQL;
- ler corretamente o arquivo Parquet da camada Trusted;
- validar que toda a infraestrutura da camada Load está operacional.

A inserção dos dados nas tabelas será implementada na próxima etapa.

<h1>Dificuldades</h1>

Até o momento, nenhuma dificuldade técnica relevante foi encontrada nesta etapa. Todos os componentes da camada Trusted e da infraestrutura inicial da camada Load foram implementados e validados com sucesso.

<br>

<h1>Próximos passos:</h1>

Implementar a 2 etapa do PostgreSQL Loader.

<br>

# Dia 04:

<strong>feat: implementação da carga inicial de ativos no PostgreSQL</strong>

<br>

## Objetivo

Implementar a **Etapa 2 do PostgreSQL Loader**, realizando a primeira carga efetiva de dados da camada **Trusted** para o banco PostgreSQL.

Nesta etapa foi utilizada a tabela `assets`, responsável por armazenar as informações básicas das criptomoedas.

<br>

## Fluxo

Trusted Layer (Parquet)

↓

PostgresLoader

↓

Leitura dos dados com Polars

↓

Conexão com PostgreSQL

↓

Carga da tabela `assets`

↓

Validação dos registros

<br>

## O que foi implementado

* Implementação da função `load_assets()`.
* Leitura das colunas `id`, `symbol` e `name` da camada Trusted.
* Inserção dos ativos na tabela `assets`.
* Utilização de `ON CONFLICT` para evitar duplicidade de ativos.
* Captura do `asset_id` gerado pelo PostgreSQL.
* Implementação de tratamento de exceções com `rollback`.
* Validação da carga diretamente no PostgreSQL.

A tabela `assets` foi populada com os dados obtidos da camada Trusted:

* Bitcoin
* Ethereum
* Solana
* Cardano

<br>

## Resultado

Foram carregados **4 registros** na tabela `assets`.

Consulta utilizada para validação:

```sql
SELECT *
FROM public.assets;
```

Resultado:

```text
1 | bitcoin  | btc | Bitcoin
2 | ethereum | eth | Ethereum
3 | solana   | sol | Solana
4 | cardano  | ada | Cardano
```

<br>

## Dificuldades

Durante a implementação foi identificado que existiam **duas instâncias do PostgreSQL** na máquina:

* PostgreSQL instalado diretamente no Windows;
* PostgreSQL executado através do Docker.

Ambas utilizavam a porta `5432`, fazendo com que o `PostgresLoader` se conectasse inicialmente à instância do Windows em vez da instância containerizada onde as tabelas haviam sido criadas.

A situação foi identificada através da verificação do `data_directory` do PostgreSQL.

### Solução

A porta externa do PostgreSQL containerizado foi alterada para `5433`, mantendo a porta interna `5432`.

```text
127.0.0.1:5433
        ↓
Docker PostgreSQL:5432
```

Com isso, o `PostgresLoader` passou a acessar corretamente o PostgreSQL do Docker.

<br>

## Observação

O `PostgresLoader` foi executado através de:

```bash
python -m src.load.postgres_loader
```

A execução foi concluída com sucesso e confirmou:

```text
4 assets loaded successfully.
```

<br>

# Próximos passos:

* Implementar a **Etapa 3 do PostgreSQL Loader**.
* Carregar os dados de mercado na tabela `market_snapshots`.
* Relacionar cada registro ao respectivo `asset_id`.
* Validar os registros inseridos no PostgreSQL.


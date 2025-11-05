import subprocess
import os
from google.cloud import bigquery
import json

# CONFIGURATION
START_BLOCK = 23732687
END_BLOCK = 23732691
PROVIDER_URI = "https://mainnet.infura.io/v3/7aef3f0cd1f64408b163814b22cc643c"
BLOCKS_CSV = "output/blocks.csv"
TXS_CSV = "output/transactions.csv"
BQ_TABLE = "nansen-technical-test.crypto_ethereum.transactions"
SCHEMA_PATH = "assets/transactions_schema.json"


# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("gcp-key.json")

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# 1. Export blocks and transactions using ethereum-etl
print("Exporting blocks and transactions...")
subprocess.run(
    [
        "ethereumetl",
        "export_blocks_and_transactions",
        "--start-block",
        str(START_BLOCK),
        "--end-block",
        str(END_BLOCK),
        "--provider-uri",
        PROVIDER_URI,
        "--blocks-output",
        BLOCKS_CSV,
        "--transactions-output",
        TXS_CSV,
    ],
    check=True,
)

# 2. Load transactions into BigQuery with explicit schema
print("Loading transactions into BigQuery...")

# Load schema from JSON
with open(SCHEMA_PATH, "r") as schema_file:
    schema_json = json.load(schema_file)
bq_schema = [
    bigquery.SchemaField(
        name=field["name"],
        field_type=field["type"],
        mode=field.get("mode", "NULLABLE"),
    )
    for field in schema_json
]

client = bigquery.Client()
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    schema=bq_schema,
    autodetect=False,
)

with open(TXS_CSV, "rb") as source_file:
    job = client.load_table_from_file(source_file, BQ_TABLE, job_config=job_config)
job.result()
print(f"Loaded {job.output_rows} rows into {BQ_TABLE}.")

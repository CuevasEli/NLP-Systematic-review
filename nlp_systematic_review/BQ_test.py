import pandas as pd

from google.cloud import bigquery
#from colorama import Fore, Style
from pathlib import Path

# Variable
GCP_PROJECT_SEBT84='useful-proposal-392710'
GCP_REGION='europe-west1'

# BigQuery
BQ_REGION='EU'
BQ_DATASET='enhancing_systemic_reviews_nlp'
TABLE = 'pubmed'

# Cloud Storage
BUCKET_NAME='enhancing_systemic_reviews_nlp'

full_table_name = f"{GCP_PROJECT_SEBT84}.{BQ_DATASET}.raw_{TABLE}"
print("before query")
client = bigquery.Client(project=GCP_PROJECT_SEBT84)

query = f"""
        SELECT
          *
        FROM {GCP_PROJECT_SEBT84}.{BQ_DATASET}.raw_{TABLE}
        LIMIT 10"""
print(query)
query_job = client.query(query)
print('query done\n')
results = query_job.result()  # Waits for job to complete.

print(results.to_dataframe())

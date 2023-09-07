import pandas as pd

from google.cloud import bigquery
#from colorama import Fore, Style
from pathlib import Path

from nlp_systematic_review.params import *

def get_data_from_bq(query):
    #full_table_name = f"{GCP_PROJECT_SEBT84}.{BQ_DATASET}.raw_{TABLE}"

    client = bigquery.Client(project=GCP_PROJECT_SEBT84)

    query_job = client.query(query)
    results = query_job.result()  # Waits for job to complete.
    df = results.to_dataframe()

    print(f"✅ Data loaded, with shape {df.shape}")

    return df

def load_data_bq(df: pd.DataFrame
                 , replace: bool):
    full_table_name = f"{GCP_PROJECT_SEBT84}.{BQ_DATASET}.concat_{TABLE}"

    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" if replace else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(df, full_table_name, job_config=job_config)
    result = job.result()

    print(f"✅ Data saved to bigquery, with shape {df.shape}")

def get_data_row_count(table='concat_pubmed'):
    full_table_name = f"{GCP_PROJECT_SEBT84}.{BQ_DATASET}.{TABLE}"

    client = bigquery.Client(project=GCP_PROJECT_SEBT84)
    query = f"""
        SELECT
          count(*)
        FROM {full_table_name}
        """
    query_job = client.query(query)

    results = query_job.result()  # Waits for job to complete.

    df = results.to_dataframe()
    count = int(df.values)

    return count

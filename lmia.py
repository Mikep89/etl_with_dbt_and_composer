import pandas as pd
import pendulum

from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from airflow import DAG
from airflow.decorators import task, dag
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.docker.operators.docker import DockerOperator

DBT_PROJECT_PATH = Variable.get('dbt-lmia-path')
DBT_PROFILE_PATH = Variable.get('dbt-profile-path')
GCP_CREDENTIAL = Variable.get('gcp-credential-location')

@dag(dag_id = 'process_lmia',
start_date = pendulum.datetime(2025,1,12,tz='UTC'),
schedule = "@once")
def load_files():
    @task(task_id = 'get_raw_file')
    def get_raw_file(quarter: int) -> None:
        bucket = "gs://" + Variable.get('test_gs_bucket') + '/'
        (pd.read_excel(bucket + f'raw_excel_lmia/tfwp_2024q{quarter}_pos_en.xlsx', skipfooter=8, skiprows=1)
         .rename(columns = {'Province/Territory' : 'province',
                            'Program Stream': 'program_stream',
                            'Employer': 'employer',
                            'Address': 'address',
                            'Occupation': 'occupation',
                            'Incorporate Status': 'incoperation_status',
                            'Approved LMIAs': 'approved_lmia_count',
                            'Approved Positions': 'approved_positions'})
        .assign(period = "2024-Q"+ str(quarter))
                .to_csv(bucket + f'transformed_csv/lmia_q{quarter}.csv', index = False))

    def load_data_tg():
        with TaskGroup('load_data') as raw:
            for quarter in range(1,4):
                get_raw = get_raw_file.override(task_id = f'get_raw_q{quarter}')(quarter)
                load_csv_to_bq = GCSToBigQueryOperator(
                    task_id = f"load_csv_to_bq_q{quarter}",
                    bucket = Variable.get('test_gs_bucket'),
                    source_objects = f'transformed_csv/lmia_q{quarter}.csv',
                    destination_project_dataset_table = 'lmia.lmia_applications_raw',
                    source_format = 'csv',
                    write_disposition = 'WRITE_APPEND',
                    autodetect = True # being explicit here although this is true by default as per docs
                )
                get_raw  >> load_csv_to_bq

    dbt = DockerOperator(
        task_id = 'run_dbt',
        image = "mikepineau89/dbt-run",
        envionment = {'PROJECT_DIR':DBT_PROJECT_PATH}
    )
        
    load_data_tg >> dbt

load_files()
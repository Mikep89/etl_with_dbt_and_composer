import pandas as pd
import datetime

from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from airflow import DAG
from airflow.decorators import task, dag
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

@dag(dag_id = 'load_lmia_file',
start_date = datetime.date(2025,1,11),
schedule = "@once")
def load_files():
    @task(task_id = 'get_raw_file')
    def get_raw_file(quarter: int) -> pd.DataFrame:
        return pd.read_excel(Variable('test_gs_bucket') + f'raw_excel_lmia/tfwp_2024q{quarter}_pos_en.xlsx', sheet_name='2024_POS_EN', skipfooter=8)

    @task(task_id = 'save_lmia_df_as_csv')
    def save_lmia_df_as_csv(df, quarter: int) -> None:
        df.to_csv(Variable('test_gs_bucket') + f'transformed_csv/lmia_q{quarter}.csv', index = False)


    with TaskGroup('load_data') as raw:
        for quarter in range(1,4):
            get_raw = get_raw_file.override(task_id = f'get_raw_q{quarter}')(quarter)
            load_raw_to_csv = save_lmia_df_as_csv.override(task_id = f'save_lmia_df_as_csv_q{quarter}')("{{ti.xcomm_pull('raw_data.get_raw_q{quarter})}}")
            load_csv_to_bq = gcs_to_bigquery(
                bucket = Variable('test_gs_bucket'),
                source_object = '/transformed_csv/lmia_q{quarter}.csv',
                destination_project_database_table = 'lmia.lmia_applications_raw',
                source_format = 'csv',
                write_disposition = 'WRITE_APPEND',
                autodetect = True # being explicit here although this is true by default as per docs
            )
            get_raw >> load_raw_to_csv >> load_csv_to_bq
    
load_files()
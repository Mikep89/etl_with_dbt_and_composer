from airflow import DAG
import datetime
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import pandas as pd

def get_raw_file(quarter: int) -> pd.DataFrame:
    return pd.read_excel(Variable('test_gs_bucket') + f'raw_excel_lmia/tfwp_2024q{quarter}_pos_en.xlsx', sheet_name='2024_POS_EN', skipfooter=8)

def save_df_as_csv(df, quarter: int) -> None:
    df.to_csv(Variable('test_gs_bucket') + f'transformed_csv/lmia_q{quarter}.csv', index = False)




with DAG(dag_id = 'load_lmia_file',
start_date = datetime.date(2025,1,11),
schedule = "@once"
):
    for i in range(1,4):
        get_raw = PythonOperator(python_callable=get_raw_file)
        load_raw = PythonOperator(python_callable=save_df_as_csv,)
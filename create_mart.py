import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(dag_id = 'dbt-transforms',
         start_date = pendulum.datetime(2025,1,12,tz='UTC'),
         schedule = "@once") as dag:
    dbt = BashOperator(
        task_id = 'dbt-run',
        cwd = "us-east1-composer-a5b62adb-bucket/dags/etl_with_dbt_and_composer/lmia",
        bash_command="dbt run"
    )
    dbt
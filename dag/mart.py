from airflow.providers.google.cloud.operators.cloud_run import CloudRunExecuteJobOperator
from airflow import DAG

with DAG(dag_id='update_mart') as dag:
    run_dbt = CloudRunExecuteJobOperator(
            task_id = "run-dbt",
            project_id = "durable-bond-447600-a5",
            region = "us-central1",
            job_name = "dbt-run"
        )
    run_dbt
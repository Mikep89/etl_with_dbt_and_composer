FROM python:3.11-slim

RUN apt-get update & apt install --yes --no-install-recommends git & pip install dbt-core dbt-bigquery

COPY gs://us-east1-composer-a5b62adb-bucket/dags/.dbt /.dbt
COPY gs://us-east1-composer-a5b62adb-bucket/dags/etl_with_dbt_and_composer/lmia /app
WORKDIR /app
ENTRYPOINT [ "dbt", "run" ]
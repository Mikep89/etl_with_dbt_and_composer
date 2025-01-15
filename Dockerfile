FROM  python:3.12.1-slim

RUN apt-get update && apt-get install --yes git
RUN pip install dbt-core dbt-bigquery
RUN cd /root/app
ENTRYPOINT ['dbt','run']
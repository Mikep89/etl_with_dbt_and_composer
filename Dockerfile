FROM  python:3.12.1-slim

COPY ./lmia /root/lmia
COPY ./.dbt /root/.dbt
COPY ../dbt_project.yml /dbt_project.yml

RUN apt-get update && apt-get install --yes git
RUN pip install dbt-core dbt-bigquery
RUN cd /root/lmia
RUN dbt debug && dbt run && dbt test

FROM python:3.11-slim

RUN apt-get update & apt install --yes --no-install-recommends git & pip install dbt-core dbt-bigquery

COPY ./lmia /app
COPY .dbt /root/.dbt

WORKDIR /app
ENTRYPOINT [ "dbt", "run" ]
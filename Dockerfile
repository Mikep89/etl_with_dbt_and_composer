FROM python:3.11-slim

RUN apt-get update & apt install --yes --no-install-recommends git & pip install dbt-core dbt-bigquery

COPY .dbt /root/.dbt
COPY ./lmia /app
WORKDIR /app
ENTRYPOINT [ "dbt", "run" ]
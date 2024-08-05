FROM apache/airflow:2.9.3

COPY ./dags /opt/airflow/dags
COPY ./handlers /opt/airflow/handlers

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

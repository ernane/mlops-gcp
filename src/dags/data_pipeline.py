from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from tasks.data_tasks import extract_data, load_data, transform_data
from tasks.ml_tasks import (
    deploy_model,
    evaluate_model,
    preprocess_data,
    register_model,
    train_model,
)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
}

with DAG("main_pipeline", default_args=default_args, schedule_interval=None) as dag:
    # Task Group para o Pipeline de Dados
    with TaskGroup(group_id="data_pipeline") as data_pipeline:
        extract_task = PythonOperator(
            task_id="extract_data",
            python_callable=extract_data,
        )

        transform_task = PythonOperator(
            task_id="transform_data",
            python_callable=transform_data,
        )

        load_task = PythonOperator(
            task_id="load_data",
            python_callable=load_data,
        )

        extract_task >> transform_task >> load_task

    # Task Group para o Pipeline de ML
    with TaskGroup(group_id="ml_pipeline") as ml_pipeline:
        preprocess_task = PythonOperator(
            task_id="preprocess_data",
            python_callable=preprocess_data,
        )

        train_task = PythonOperator(
            task_id="train_model",
            python_callable=train_model,
        )

        evaluate_task = PythonOperator(
            task_id="evaluate_model",
            python_callable=evaluate_model,
        )

        register_task = PythonOperator(
            task_id="register_model",
            python_callable=register_model,
        )

        deploy_task = PythonOperator(
            task_id="deploy_model",
            python_callable=deploy_model,
        )

        preprocess_task >> train_task >> evaluate_task >> register_task >> deploy_task

    data_pipeline >> ml_pipeline

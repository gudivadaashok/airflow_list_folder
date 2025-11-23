from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import logging
from pathlib import Path

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'list_folders_dag',
    default_args=default_args,
    description='A DAG to list folders in a directory',
    schedule_interval=timedelta(days=1),  # Run daily
    catchup=False,
)

def list_folders_task(directory_path):
    """
    Function to list folders in a directory
    """
    directory = Path(directory_path)
    
    logging.info(f"Current time: {datetime.now()}")
    
    if not directory.exists():
        logging.error(f"Directory does not exist: {directory}")
        raise FileNotFoundError(f"Directory does not exist: {directory}")
    
    logging.info(f"Scanning directory: {directory}")
    
    folders = [p.name for p in directory.iterdir() if p.is_dir()]
    folders.sort()
    
    logging.info("Folders found:")
    for name in folders:
        logging.info(f"  - {name}")
    
    return folders

# Create the task
list_folders = PythonOperator(
    task_id='list_folders',
    python_callable=list_folders_task,
    op_kwargs={'directory_path': '/mnt/target_directory'},  # Mounted Windows directory
    dag=dag,
)

list_folders

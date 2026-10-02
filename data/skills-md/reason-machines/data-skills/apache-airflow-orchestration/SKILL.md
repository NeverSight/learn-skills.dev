---
name: apache-airflow-orchestration
description: Expert knowledge of Apache Airflow for building, scheduling, and monitoring data pipelines and workflows
triggers:
  - how do I create an Airflow DAG
  - help me schedule a workflow in Airflow
  - how to set up Apache Airflow
  - create an Airflow pipeline
  - how do I use Airflow operators
  - troubleshoot Airflow task failures
  - configure Airflow connections
  - how to use XCom in Airflow
---

# Apache Airflow Orchestration

> Skill by [ara.so](https://ara.so) — Data Skills collection.

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows. It allows you to define workflows as Directed Acyclic Graphs (DAGs) in Python code, making them maintainable, versionable, testable, and collaborative.

## Installation

### Using pip

```bash
# Install Airflow with constraints for your Python version
AIRFLOW_VERSION=3.2.0
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### Using Docker (Recommended for Development)

```bash
# Download docker-compose.yaml
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Create required directories
mkdir -p ./dags ./logs ./plugins ./config

# Set the Airflow user
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize the database
docker compose up airflow-init

# Start Airflow
docker compose up
```

Access the web UI at `http://localhost:8080` (default credentials: `airflow`/`airflow`).

### Standalone Quick Start

```bash
# Initialize database and create admin user
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start the web server (default port 8080)
airflow webserver --port 8080

# Start the scheduler (in another terminal)
airflow scheduler
```

## Core Concepts

### DAG (Directed Acyclic Graph)

A DAG defines a workflow with tasks and their dependencies. Tasks must not create cycles.

### Basic DAG Structure

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Default arguments applied to all tasks
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_data_pipeline',
    default_args=default_args,
    description='A simple data pipeline',
    schedule='0 0 * * *',  # Run daily at midnight (cron expression)
    start_date=datetime(2024, 1, 1),
    catchup=False,  # Don't run for past dates
    tags=['example', 'data-engineering'],
)

def extract_data(**context):
    """Extract data from source"""
    print("Extracting data...")
    # Your extraction logic here
    return {'records': 1000}

def transform_data(**context):
    """Transform extracted data"""
    # Access data from previous task via XCom
    ti = context['ti']
    extracted = ti.xcom_pull(task_ids='extract')
    print(f"Transforming {extracted['records']} records...")
    return {'transformed_records': extracted['records']}

def load_data(**context):
    """Load data to destination"""
    ti = context['ti']
    transformed = ti.xcom_pull(task_ids='transform')
    print(f"Loading {transformed['transformed_records']} records...")

# Define tasks
extract = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

load = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag,
)

# Set task dependencies
extract >> transform >> load
```

### TaskFlow API (Recommended for Airflow 2.0+)

Modern, cleaner syntax using decorators:

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['taskflow', 'etl'],
)
def taskflow_etl_pipeline():
    """
    ETL pipeline using TaskFlow API
    """
    
    @task()
    def extract():
        """Extract data from API"""
        import requests
        # Using environment variable for API key
        import os
        api_key = os.getenv('DATA_API_KEY')
        
        # Simulated extraction
        data = {'records': [1, 2, 3, 4, 5]}
        return data
    
    @task()
    def transform(data: dict):
        """Transform the data"""
        records = data['records']
        transformed = [r * 2 for r in records]
        return {'transformed': transformed}
    
    @task()
    def load(data: dict):
        """Load data to warehouse"""
        print(f"Loading {len(data['transformed'])} records")
        # Your loading logic here
        return True
    
    # Define pipeline
    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

# Instantiate the DAG
taskflow_etl_pipeline()
```

## Common Operators

### BashOperator

```python
from airflow.operators.bash import BashOperator

run_script = BashOperator(
    task_id='run_data_script',
    bash_command='python /opt/scripts/process_data.py --date {{ ds }}',
    dag=dag,
)
```

### PythonOperator

```python
from airflow.operators.python import PythonOperator

def my_function(param1, param2, **context):
    execution_date = context['execution_date']
    print(f"Processing for {execution_date}")
    # Your logic here

python_task = PythonOperator(
    task_id='python_task',
    python_callable=my_function,
    op_kwargs={'param1': 'value1', 'param2': 'value2'},
    dag=dag,
)
```

### BranchPythonOperator

```python
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator

def choose_branch(**context):
    """Decide which branch to execute"""
    execution_date = context['execution_date']
    if execution_date.day % 2 == 0:
        return 'even_day_task'
    else:
        return 'odd_day_task'

branch = BranchPythonOperator(
    task_id='branch_task',
    python_callable=choose_branch,
    dag=dag,
)

even_task = EmptyOperator(task_id='even_day_task', dag=dag)
odd_task = EmptyOperator(task_id='odd_day_task', dag=dag)

branch >> [even_task, odd_task]
```

### EmailOperator

```python
from airflow.operators.email import EmailOperator

send_email = EmailOperator(
    task_id='send_notification',
    to='team@example.com',
    subject='Pipeline {{ ds }} completed',
    html_content='<p>The pipeline for {{ ds }} has completed successfully.</p>',
    dag=dag,
)
```

## Sensors

Sensors wait for a condition to be met before proceeding.

### FileSensor

```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id='wait_for_data_file',
    filepath='/data/input/file_{{ ds }}.csv',
    poke_interval=30,  # Check every 30 seconds
    timeout=3600,  # Timeout after 1 hour
    mode='poke',  # 'poke' or 'reschedule'
    dag=dag,
)
```

### TimeDeltaSensor

```python
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import timedelta

wait_sensor = TimeDeltaSensor(
    task_id='wait_10_minutes',
    delta=timedelta(minutes=10),
    dag=dag,
)
```

### Custom Sensor

```python
from airflow.sensors.base import BaseSensorOperator

class CustomDataSensor(BaseSensorOperator):
    def __init__(self, endpoint, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = endpoint
    
    def poke(self, context):
        """Check if data is available"""
        import requests
        import os
        
        api_key = os.getenv('API_KEY')
        response = requests.get(
            self.endpoint,
            headers={'Authorization': f'Bearer {api_key}'}
        )
        return response.status_code == 200 and response.json().get('ready', False)

check_data = CustomDataSensor(
    task_id='check_data_ready',
    endpoint='https://api.example.com/status',
    poke_interval=60,
    timeout=3600,
    dag=dag,
)
```

## Connections and Hooks

### Setting Up Connections

Connections store credentials and connection details.

#### Via CLI

```bash
# Add a Postgres connection
airflow connections add 'postgres_default' \
    --conn-type 'postgres' \
    --conn-host 'localhost' \
    --conn-schema 'mydb' \
    --conn-login 'user' \
    --conn-password 'password' \
    --conn-port 5432

# Add an HTTP connection
airflow connections add 'http_api' \
    --conn-type 'http' \
    --conn-host 'https://api.example.com' \
    --conn-extra '{"api_key": "from_env_var"}'
```

#### Via Environment Variables

```bash
export AIRFLOW_CONN_POSTGRES_DEFAULT='postgresql://user:password@localhost:5432/mydb'
export AIRFLOW_CONN_HTTP_API='http://api.example.com'
```

### Using Hooks

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task

@task()
def query_database():
    """Query PostgreSQL database"""
    hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Execute query and fetch results
    results = hook.get_records(
        sql="SELECT * FROM users WHERE created_date = %s",
        parameters=['2024-01-01']
    )
    
    # Or use pandas
    df = hook.get_pandas_df(sql="SELECT * FROM transactions")
    
    return len(results)

@task()
def insert_data():
    """Insert data into database"""
    hook = PostgresHook(postgres_conn_id='postgres_default')
    
    hook.run(
        sql="INSERT INTO logs (message, timestamp) VALUES (%s, %s)",
        parameters=[('Pipeline completed', datetime.now())]
    )
```

### HTTP Hook Example

```python
from airflow.providers.http.hooks.http import HttpHook
from airflow.decorators import task

@task()
def call_api():
    """Make HTTP API call"""
    hook = HttpHook(http_conn_id='http_api', method='GET')
    
    response = hook.run(
        endpoint='/v1/data',
        headers={'Content-Type': 'application/json'},
        extra_options={'timeout': 30}
    )
    
    data = response.json()
    return data
```

## XCom (Cross-Communication)

XCom allows tasks to exchange small amounts of data.

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2024, 1, 1), schedule=None, catchup=False)
def xcom_example():
    
    @task()
    def push_data():
        """Push data to XCom"""
        return {
            'total_records': 1000,
            'processing_time': 45.2,
            'status': 'success'
        }
    
    @task()
    def pull_data(data: dict):
        """Receive data from previous task"""
        print(f"Received {data['total_records']} records")
        print(f"Processing took {data['processing_time']} seconds")
        
        # Can also use task instance to pull from specific task
        from airflow.operators.python import get_current_context
        context = get_current_context()
        ti = context['ti']
        
        # Pull from specific task
        specific_data = ti.xcom_pull(task_ids='push_data')
        return specific_data['status']
    
    result = push_data()
    pull_data(result)

xcom_example()
```

### XCom with Multiple Return Values

```python
@task()
def process_multiple():
    """Return multiple values"""
    return {'key1': 'value1', 'key2': 'value2'}

@task()
def use_multiple(data: dict):
    """Use multiple values"""
    print(data['key1'], data['key2'])

data = process_multiple()
use_multiple(data)
```

## Task Dependencies

### Linear Dependencies

```python
task1 >> task2 >> task3
# Or
task1.set_downstream(task2)
task2.set_downstream(task3)
```

### Parallel Dependencies

```python
# Fan-out
task1 >> [task2, task3, task4]

# Fan-in
[task2, task3, task4] >> task5
```

### Complex Dependencies

```python
# Multiple dependencies
task1 >> task2
task1 >> task3
[task2, task3] >> task4

# Or using chain
from airflow.models.baseoperator import chain

chain(task1, [task2, task3], task4)
```

### Cross-DAG Dependencies

```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_for_other_dag = ExternalTaskSensor(
    task_id='wait_for_upstream_dag',
    external_dag_id='upstream_dag',
    external_task_id='final_task',
    timeout=3600,
    dag=dag,
)
```

## Dynamic Task Generation

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2024, 1, 1), schedule=None, catchup=False)
def dynamic_tasks_example():
    
    @task()
    def get_sources():
        """Get list of data sources to process"""
        return ['source_1', 'source_2', 'source_3', 'source_4']
    
    @task()
    def process_source(source: str):
        """Process a single source"""
        print(f"Processing {source}")
        # Your processing logic
        return f"{source}_processed"
    
    @task()
    def combine_results(results: list):
        """Combine all processed results"""
        print(f"Combining {len(results)} results")
        return results
    
    sources = get_sources()
    processed = process_source.expand(source=sources)
    combine_results(processed)

dynamic_tasks_example()
```

### Dynamic Task Mapping (Airflow 2.3+)

```python
@dag(start_date=datetime(2024, 1, 1), schedule=None, catchup=False)
def task_mapping_example():
    
    @task()
    def extract_files():
        """Return list of files to process"""
        return [
            {'file': 'data1.csv', 'format': 'csv'},
            {'file': 'data2.json', 'format': 'json'},
            {'file': 'data3.parquet', 'format': 'parquet'},
        ]
    
    @task()
    def process_file(file_info: dict):
        """Process a single file"""
        filename = file_info['file']
        format = file_info['format']
        print(f"Processing {filename} as {format}")
        return f"Processed {filename}"
    
    files = extract_files()
    process_file.expand(file_info=files)

task_mapping_example()
```

## Configuration

### airflow.cfg

Key configuration options:

```ini
[core]
# DAGs folder
dags_folder = /opt/airflow/dags

# Executor (LocalExecutor, CeleryExecutor, KubernetesExecutor)
executor = LocalExecutor

# Parallelism
parallelism = 32
dag_concurrency = 16
max_active_runs_per_dag = 16

[database]
# Database connection
sql_alchemy_conn = postgresql+psycopg2://airflow:password@localhost/airflow

[scheduler]
# How often to scan for new DAGs
dag_dir_list_interval = 300

# Number of scheduler processes
scheduler_zombie_task_threshold = 300

[webserver]
# Web server host and port
web_server_host = 0.0.0.0
web_server_port = 8080

# Secret key for session
secret_key = your_secret_key_here

[email]
# Email backend
email_backend = airflow.utils.email.send_email_smtp

[smtp]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = your_email@gmail.com
smtp_password = your_app_password
smtp_mail_from = airflow@example.com
```

### Environment Variables

```bash
# Override any config
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://user:pass@localhost/airflow
export AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
export AIRFLOW__WEBSERVER__SECRET_KEY=your_secret_key

# Set Airflow home
export AIRFLOW_HOME=~/airflow
```

## Variables

Store global configuration values.

### Set Variables

```bash
# Via CLI
airflow variables set my_key my_value
airflow variables set api_endpoint "https://api.example.com/v1"

# Import from JSON file
airflow variables import variables.json
```

### Use Variables in DAGs

```python
from airflow.models import Variable

# Get variable
api_endpoint = Variable.get("api_endpoint")

# Get with default value
timeout = Variable.get("timeout", default_var=30)

# Get as JSON
config = Variable.get("config_json", deserialize_json=True)

# In a task
@task()
def use_variable():
    endpoint = Variable.get("api_endpoint")
    print(f"Using endpoint: {endpoint}")
```

### Variables in Templates

```python
bash_task = BashOperator(
    task_id='use_variable',
    bash_command='echo "API: {{ var.value.api_endpoint }}"',
    dag=dag,
)
```

## Templating with Jinja

Airflow uses Jinja templating for many fields.

### Common Template Variables

```python
from airflow.operators.bash import BashOperator

templated_command = """
    # Execution date
    echo "Execution date: {{ ds }}"  # YYYY-MM-DD
    echo "Execution date no dash: {{ ds_nodash }}"  # YYYYMMDD
    
    # Date components
    echo "Year: {{ macros.ds_format(ds, '%Y-%m-%d', '%Y') }}"
    echo "Previous day: {{ macros.ds_add(ds, -1) }}"
    
    # Task instance
    echo "Task ID: {{ task.task_id }}"
    echo "DAG ID: {{ dag.dag_id }}"
    echo "Run ID: {{ run_id }}"
    
    # Parameters
    echo "Param: {{ params.my_param }}"
"""

task = BashOperator(
    task_id='templated_task',
    bash_command=templated_command,
    params={'my_param': 'value'},
    dag=dag,
)
```

### Custom Macros

```python
def custom_macro(value):
    """Custom Jinja macro"""
    return value.upper()

dag = DAG(
    'dag_with_macros',
    user_defined_macros={
        'custom_upper': custom_macro
    },
    start_date=datetime(2024, 1, 1),
)

task = BashOperator(
    task_id='use_macro',
    bash_command='echo "{{ custom_upper(params.name) }}"',
    params={'name': 'airflow'},
    dag=dag,
)
```

## CLI Commands

### DAG Management

```bash
# List all DAGs
airflow dags list

# List tasks in a DAG
airflow tasks list my_dag

# Show DAG structure
airflow dags show my_dag

# Trigger a DAG run
airflow dags trigger my_dag

# Trigger with config
airflow dags trigger my_dag --conf '{"key": "value"}'

# Pause/Unpause DAG
airflow dags pause my_dag
airflow dags unpause my_dag

# Delete DAG (from metadata, not file)
airflow dags delete my_dag
```

### Task Management

```bash
# Test a task (doesn't save state)
airflow tasks test my_dag my_task 2024-01-01

# Run a task (saves state)
airflow tasks run my_dag my_task 2024-01-01

# Clear task state
airflow tasks clear my_dag --task-regex my_task

# Clear all tasks in DAG
airflow tasks clear my_dag --start-date 2024-01-01 --end-date 2024-01-31
```

### Database

```bash
# Initialize database
airflow db init

# Upgrade database
airflow db upgrade

# Reset database (WARNING: deletes all data)
airflow db reset

# Check database
airflow db check
```

### Users

```bash
# Create user
airflow users create \
    --username john \
    --firstname John \
    --lastname Doe \
    --role Admin \
    --email john@example.com

# List users
airflow users list

# Delete user
airflow users delete --username john
```

### Connections

```bash
# List connections
airflow connections list

# Get connection details
airflow connections get postgres_default

# Export connections
airflow connections export connections.json

# Import connections
airflow connections import connections.json
```

### Variables

```bash
# Set variable
airflow variables set my_var my_value

# Get variable
airflow variables get my_var

# Delete variable
airflow variables delete my_var

# List all variables
airflow variables list

# Export variables to JSON
airflow variables export variables.json

# Import variables from JSON
airflow variables import variables.json
```

## Working with Providers

Providers extend Airflow with additional operators, hooks, and sensors.

### Install Providers

```bash
# Install specific providers
pip install apache-airflow-providers-amazon
pip install apache-airflow-providers-google
pip install apache-airflow-providers-postgres
pip install apache-airflow-providers-http
pip install apache-airflow-providers-docker
```

### AWS S3 Example

```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2024, 1, 1), schedule=None, catchup=False)
def s3_example():
    
    list_files = S3ListOperator(
        task_id='list_s3_files',
        bucket='my-bucket',
        prefix='data/',
        aws_conn_id='aws_default',
    )
    
    @task()
    def download_from_s3():
        """Download file from S3"""
        hook = S3Hook(aws_conn_id='aws_default')
        
        # Download file
        content = hook.read_key(
            key='data/file.csv',
            bucket_name='my-bucket'
        )
        
        return len(content)
    
    @task()
    def upload_to_s3():
        """Upload file to S3"""
        hook = S3Hook(aws_conn_id='aws_default')
        
        # Upload file
        hook.load_string(
            string_data='Hello, S3!',
            key='output/result.txt',
            bucket_name='my-bucket'
        )
    
    list_files >> download_from_s3() >> upload_to_s3()

s3_example()
```

### Google Cloud Storage Example

```python
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

load_to_bigquery = GCSToBigQueryOperator(
    task_id='load_to_bq',
    bucket='my-gcs-bucket',
    source_objects=['data/*.csv'],
    destination_project_dataset_table='project.dataset.table',
    source_format='CSV',
    skip_leading_rows=1,
    write_disposition='WRITE_TRUNCATE',
    gcp_conn_id='google_cloud_default',
    dag=dag,
)
```

### Docker Operator Example

```python
from airflow.providers.docker.operators.docker import DockerOperator

run_container = DockerOperator(
    task_id='run_docker_container',
    image='python:3.10',
    command='python -c "print(\'Hello from Docker\')"',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    dag=dag,
)
```

## Error Handling and Retries

### Task-level Configuration

```python
@task(
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    max_retry_delay=timedelta(hours=1),
)
def task_with_retries():
    """Task with custom retry logic"""
    # Your code
    pass
```

### Failure Callbacks

```python
def on_failure_callback(context):
    """Called when task fails"""
    ti = context['task_instance']
    print(f"Task {ti.task_id} failed!")
    # Send alert, create ticket, etc.

def on_success_callback(context):
    """Called when task succeeds"""
    print("Task succeeded!")

@task(
    on_failure_callback=on_failure_callback,
    on_success_callback=on_success_callback,
)
def monitored_task():
    """Task with callbacks"""
    # Your code
    pass
```

### Try/Except in Tasks

```python
from airflow.exceptions import AirflowException

@task()
def safe_task():
    """Task with error handling"""
    try:
        # Your code that might fail
        result = risky_operation()
        return result
    except SpecificException as e:
        # Log error but don't fail task
        print(f"Warning: {e}")
        return None
    except Exception as e:
        # Fail task with custom message
        raise AirflowException(f"Critical error: {e}")
```

## Testing DAGs

### Unit Testing

```python
# test_dag.py
import pytest
from datetime import datetime
from airflow.models import DagBag

def test_dag_loaded():
    """Test that DAG is loaded correctly"""
    dagbag = DagBag(dag_folder='dags/', include_examples=False)
    assert 'my_dag' in dagbag.dags
    assert len(dagbag.import_errors) == 0

def test_dag_structure():
    """Test DAG structure"""
    dagbag = DagBag(dag_folder='dags/', include_examples=False)
    dag = dagbag.get_dag('my_dag')
    
    # Check task count
    assert len(dag.tasks) == 5
    
    # Check specific task exists
    assert 'extract' in dag.task_ids
    
    # Check dependencies
    extract_task = dag.get_task('extract')
    downstream = extract_task.downstream_task_ids
    assert 'transform' in downstream

def test_task_execution():
    """Test task execution"""
    from airflow.models import TaskInstance
    from airflow import settings
    
    dagbag = DagBag(dag_folder='dags/')
    dag = dagbag.get_dag('my_dag')
    task = dag.get_task('extract')
    
    # Create task instance
    ti = TaskInstance(task=task, execution_date=datetime(2024, 1, 1))
    
    # Test execution
    ti.run(ignore_ti_state=True)
    
    # Check result
    assert ti.state == 'success'
```

### Integration Testing

```python
# test_integration.py
from airflow.models import DagBag
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType

def test_dag_run():
    """Test complete DAG run"""
    dagbag = DagBag(dag_folder='dags/')
    dag = dagbag.get_dag('my_dag')
    
    # Trigger DAG
    dag.test()
```

## Best Practices

### 1. Idempotent Tasks

```python
@task()
def idempotent_load(execution_date):
    """
    Task that can be run multiple times safely
    """
    # Delete existing data for this date first
    delete_query = "DELETE FROM table WHERE date = %s"
    hook.run(delete_query, parameters=[execution_date])
    
    # Then insert new data
    insert_query = "INSERT INTO table ..."
    hook.run(insert_query)
```

### 2. Use Connections for Credentials

```python
# Good: Use connections
@task()
def good_practice():
    hook = PostgresHook(postgres_conn_id='postgres_default')
    # Use hook

# Bad: Hardcode credentials
@task()
def bad_practice():
    import psycopg2
    conn = psycopg2.connect(
        host='localhost',
        user='user',  # Don't do this!
        password='password'  # Never do this!
    )
```

### 3. Don't Pass Large Data Between Tasks

```python
# Good: Pass references
@task()
def process_data():
    # Process and save to database/storage
    data_id = save_to_database(large_data)
    return data_id  # Return only ID

@task()

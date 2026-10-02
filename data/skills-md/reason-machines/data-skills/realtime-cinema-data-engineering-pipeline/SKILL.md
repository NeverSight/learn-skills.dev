---
name: realtime-cinema-data-engineering-pipeline
description: Build end-to-end real-time data pipelines with Kafka, PostgreSQL, Airflow, and Streamlit using Medallion Architecture for streaming analytics.
triggers:
  - set up a real-time data pipeline with kafka and airflow
  - build a streaming etl pipeline with medallion architecture
  - create a cinema analytics dashboard with streamlit
  - implement bronze silver gold data layers
  - stream events through kafka to postgresql
  - orchestrate elt pipelines with apache airflow
  - visualize real-time analytics with plotly
  - configure kafka producers and consumers for data ingestion
---

# CinéWorld Real-Time Data Engineering Pipeline Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project implements an end-to-end real-time data engineering pipeline using Apache Kafka for event streaming, PostgreSQL for data warehousing with Medallion Architecture (Bronze/Silver/Gold layers), Apache Airflow for ELT orchestration, and Streamlit for live visualization. Perfect for learning how to build production-grade streaming data pipelines that process 1M+ events.

## Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Virtual environment (recommended)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/BaidaneAyoub/realtime-cinema-data-engineering.git
cd realtime-cinema-data-engineering

# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start infrastructure (Kafka, PostgreSQL, Airflow)
docker-compose up -d
```

**Important**: Wait 2-3 minutes for Airflow to fully initialize before proceeding.

## Architecture Components

### 1. Medallion Architecture Layers

**Bronze Layer**: Raw JSON event data ingested from Kafka
```sql
-- Bronze table stores raw events
CREATE TABLE bronze_transactions (
    id SERIAL PRIMARY KEY,
    raw_data JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Silver Layer**: Normalized 3NF tables (Customers, Movies, Showtimes, Transactions)
```sql
-- Normalized dimension and fact tables
CREATE TABLE silver_customers (...);
CREATE TABLE silver_movies (...);
CREATE TABLE silver_showtimes (...);
CREATE TABLE silver_transactions (...);
```

**Gold Layer**: Materialized views for analytics
```sql
-- Business-ready aggregated data
CREATE MATERIALIZED VIEW gold_cinema_analytics AS
SELECT ...
```

### 2. Kafka Event Producer

Generate and stream synthetic cinema transaction events:

```python
# producer/main_producer.py
from kafka import KafkaProducer
from faker import Faker
import json
import time
import os

fake = Faker()

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_ticket_sale():
    """Generate a synthetic ticket sale event"""
    return {
        "transaction_id": fake.uuid4(),
        "customer": {
            "customer_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number()
        },
        "movie": {
            "movie_id": fake.uuid4(),
            "title": fake.catch_phrase(),
            "genre": fake.random_element(['Action', 'Comedy', 'Drama', 'Horror']),
            "duration_minutes": fake.random_int(90, 180)
        },
        "showtime": {
            "showtime_id": fake.uuid4(),
            "cinema_location": fake.city(),
            "screen_number": fake.random_int(1, 10),
            "showtime": fake.date_time_this_month().isoformat()
        },
        "payment": {
            "amount": round(fake.random.uniform(8.0, 25.0), 2),
            "payment_method": fake.random_element(['Credit Card', 'Cash', 'Gift Card']),
            "currency": "USD"
        },
        "seats": [f"{fake.random_element(['A','B','C','D'])}{fake.random_int(1,20)}"],
        "timestamp": fake.date_time_this_month().isoformat()
    }

# Stream events continuously
def start_streaming(topic='cinema_transactions', interval=0.5):
    """Start producing events to Kafka topic"""
    print(f"🎬 Starting producer on topic: {topic}")
    
    try:
        while True:
            event = generate_ticket_sale()
            producer.send(topic, value=event)
            print(f"✅ Sent: {event['transaction_id']}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Stopping producer...")
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    start_streaming()
```

### 3. Kafka Consumer (Bronze Layer Ingestion)

Consume events from Kafka and insert into PostgreSQL Bronze layer:

```python
# consumer/main_consumer.py
from kafka import KafkaConsumer
import psycopg2
from psycopg2.extras import Json
import json
import os

# Kafka consumer configuration
consumer = KafkaConsumer(
    'cinema_transactions',
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='cinema-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        database=os.getenv('POSTGRES_DB', 'cinema_dw'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres')
    )

def insert_bronze(connection, event_data):
    """Insert raw event into bronze layer"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO bronze_transactions (raw_data)
            VALUES (%s)
            """,
            (Json(event_data),)
        )
        connection.commit()

# Start consuming
def start_consuming():
    print("🎧 Starting consumer...")
    conn = get_db_connection()
    
    try:
        for message in consumer:
            event = message.value
            insert_bronze(conn, event)
            print(f"✅ Inserted: {event.get('transaction_id', 'unknown')}")
    except KeyboardInterrupt:
        print("\n🛑 Stopping consumer...")
    finally:
        conn.close()
        consumer.close()

if __name__ == "__main__":
    start_consuming()
```

### 4. Airflow ELT DAG (Bronze → Silver → Gold)

Orchestrate data transformation pipeline:

```python
# dags/bronze_to_silver_and_gold_elt.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def bronze_to_silver():
    """Extract from Bronze, transform, and load into Silver layer"""
    pg_hook = PostgresHook(postgres_conn_id='postgres_cinema_dw')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # Fetch unprocessed bronze records (limit 50k per run)
    cursor.execute("""
        SELECT id, raw_data 
        FROM bronze_transactions 
        WHERE processed = FALSE 
        LIMIT 50000
    """)
    
    records = cursor.fetchall()
    
    for record_id, raw_data in records:
        # Extract nested fields
        customer = raw_data['customer']
        movie = raw_data['movie']
        showtime = raw_data['showtime']
        payment = raw_data['payment']
        
        # Insert into silver_customers (upsert)
        cursor.execute("""
            INSERT INTO silver_customers (customer_id, name, email, phone)
            VALUES (%(customer_id)s, %(name)s, %(email)s, %(phone)s)
            ON CONFLICT (customer_id) DO NOTHING
        """, customer)
        
        # Insert into silver_movies (upsert)
        cursor.execute("""
            INSERT INTO silver_movies (movie_id, title, genre, duration_minutes)
            VALUES (%(movie_id)s, %(title)s, %(genre)s, %(duration_minutes)s)
            ON CONFLICT (movie_id) DO NOTHING
        """, movie)
        
        # Insert into silver_showtimes (upsert)
        cursor.execute("""
            INSERT INTO silver_showtimes (showtime_id, cinema_location, screen_number, showtime)
            VALUES (%(showtime_id)s, %(cinema_location)s, %(screen_number)s, %(showtime)s)
            ON CONFLICT (showtime_id) DO NOTHING
        """, showtime)
        
        # Insert into silver_transactions (fact table)
        cursor.execute("""
            INSERT INTO silver_transactions 
            (transaction_id, customer_id, movie_id, showtime_id, amount, payment_method, seats, transaction_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
        """, (
            raw_data['transaction_id'],
            customer['customer_id'],
            movie['movie_id'],
            showtime['showtime_id'],
            payment['amount'],
            payment['payment_method'],
            raw_data['seats'],
            raw_data['timestamp']
        ))
        
        # Mark as processed
        cursor.execute("""
            UPDATE bronze_transactions SET processed = TRUE WHERE id = %s
        """, (record_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Processed {len(records)} records from Bronze to Silver")

def refresh_gold_layer():
    """Refresh materialized view in Gold layer"""
    pg_hook = PostgresHook(postgres_conn_id='postgres_cinema_dw')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    cursor.execute("REFRESH MATERIALIZED VIEW gold_cinema_analytics")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Refreshed Gold layer materialized view")

# Define DAG
with DAG(
    'bronze_to_silver_and_gold_elt',
    default_args=default_args,
    description='ELT pipeline: Bronze → Silver → Gold',
    schedule_interval=timedelta(minutes=5),
    catchup=False,
) as dag:
    
    task_bronze_to_silver = PythonOperator(
        task_id='bronze_to_silver',
        python_callable=bronze_to_silver,
    )
    
    task_refresh_gold = PythonOperator(
        task_id='refresh_gold_layer',
        python_callable=refresh_gold_layer,
    )
    
    task_bronze_to_silver >> task_refresh_gold
```

### 5. Streamlit Dashboard

Real-time analytics visualization:

```python
# dashboard/app.py
import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import os
from time import sleep

st.set_page_config(page_title="CinéWorld Executive Dashboard", layout="wide")

@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        database=os.getenv('POSTGRES_DB', 'cinema_dw'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres')
    )

def fetch_gold_data():
    """Fetch aggregated analytics from Gold layer"""
    conn = get_db_connection()
    query = """
        SELECT 
            cinema_location,
            genre,
            payment_method,
            total_revenue,
            ticket_count,
            avg_ticket_price
        FROM gold_cinema_analytics
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Dashboard header
st.title("🎬 CinéWorld Real-Time Analytics Dashboard")
st.markdown("**Live metrics from Gold layer** | Updates every 30 seconds")

# Auto-refresh
if 'refresh_counter' not in st.session_state:
    st.session_state.refresh_counter = 0

placeholder = st.empty()

while True:
    with placeholder.container():
        # Fetch fresh data
        df = fetch_gold_data()
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Revenue", f"${df['total_revenue'].sum():,.2f}")
        with col2:
            st.metric("Total Tickets Sold", f"{df['ticket_count'].sum():,.0f}")
        with col3:
            st.metric("Avg Ticket Price", f"${df['avg_ticket_price'].mean():.2f}")
        with col4:
            st.metric("Active Locations", df['cinema_location'].nunique())
        
        # Visualizations
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Revenue by Location
            location_revenue = df.groupby('cinema_location')['total_revenue'].sum().reset_index()
            fig1 = px.bar(
                location_revenue,
                x='cinema_location',
                y='total_revenue',
                title='Revenue by Cinema Location',
                labels={'total_revenue': 'Revenue ($)', 'cinema_location': 'Location'}
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Tickets by Payment Method
            payment_tickets = df.groupby('payment_method')['ticket_count'].sum().reset_index()
            fig3 = px.pie(
                payment_tickets,
                values='ticket_count',
                names='payment_method',
                title='Tickets by Payment Method'
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_right:
            # Revenue by Genre (Treemap)
            genre_revenue = df.groupby('genre')['total_revenue'].sum().reset_index()
            fig2 = px.treemap(
                genre_revenue,
                path=['genre'],
                values='total_revenue',
                title='Revenue by Movie Genre'
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Top performing locations table
            st.subheader("Top 5 Locations by Revenue")
            top_locations = df.groupby('cinema_location').agg({
                'total_revenue': 'sum',
                'ticket_count': 'sum'
            }).sort_values('total_revenue', ascending=False).head(5)
            st.dataframe(top_locations, use_container_width=True)
    
    sleep(30)
    st.session_state.refresh_counter += 1
    st.rerun()
```

## Configuration

### Environment Variables

Create a `.env` file for configuration:

```bash
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=cinema_transactions

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cinema_dw
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Airflow Configuration
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW_CONN_POSTGRES_CINEMA_DW=postgresql://postgres:postgres@postgres:5432/cinema_dw
```

### Docker Compose Services

```yaml
# docker-compose.yml (key services)
services:
  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: cinema_dw
    ports:
      - "5432:5432"
  
  airflow-webserver:
    image: apache/airflow:2.7.0
    ports:
      - "8080:8080"
```

## Common Workflows

### Starting the Complete Pipeline

```bash
# Terminal 1: Start infrastructure
docker-compose up -d
sleep 180  # Wait for Airflow initialization

# Terminal 2: Start producer
source myenv/bin/activate
python producer/main_producer.py

# Terminal 3: Start consumer
source myenv/bin/activate
python consumer/main_consumer.py

# Terminal 4: Launch dashboard
source myenv/bin/activate
streamlit run dashboard/app.py

# Browser: Access Airflow at http://localhost:8080
# Enable DAG: bronze_to_silver_and_gold_elt
```

### Manual DAG Trigger

```bash
# Via Airflow CLI inside container
docker exec -it <airflow-container-id> airflow dags trigger bronze_to_silver_and_gold_elt
```

### Query Gold Layer Directly

```python
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="cinema_dw",
    user="postgres",
    password="postgres"
)

# Get top revenue-generating genres
query = """
    SELECT genre, SUM(total_revenue) as revenue
    FROM gold_cinema_analytics
    GROUP BY genre
    ORDER BY revenue DESC
    LIMIT 5
"""

df = pd.read_sql(query, conn)
print(df)
conn.close()
```

## Troubleshooting

### Kafka Consumer Not Receiving Messages

```bash
# Check if topic exists
docker exec -it <kafka-container> kafka-topics --list --bootstrap-server localhost:9092

# Check consumer group lag
docker exec -it <kafka-container> kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group cinema-consumer-group \
  --describe
```

### Airflow DAG Not Running

```python
# Check DAG status
from airflow.models import DagBag

dagbag = DagBag()
dag = dagbag.get_dag('bronze_to_silver_and_gold_elt')
print(f"DAG errors: {dagbag.import_errors}")
```

### PostgreSQL Connection Issues

```bash
# Test connection
docker exec -it <postgres-container> psql -U postgres -d cinema_dw -c "\dt"

# Check if tables exist
docker exec -it <postgres-container> psql -U postgres -d cinema_dw -c "
SELECT schemaname, tablename 
FROM pg_tables 
WHERE schemaname = 'public';
"
```

### Streamlit Dashboard Not Updating

```python
# Check if materialized view is populated
conn = psycopg2.connect(...)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM gold_cinema_analytics")
count = cursor.fetchone()[0]
print(f"Gold layer records: {count}")
```

## Performance Optimization

### Batch Processing Size

Adjust batch size in Airflow DAG:

```python
# In bronze_to_silver() function
cursor.execute("""
    SELECT id, raw_data 
    FROM bronze_transactions 
    WHERE processed = FALSE 
    LIMIT 100000  -- Increase for better throughput
""")
```

### Kafka Consumer Parallelization

```python
# Run multiple consumer instances with same group_id
# Each will process different partitions

# consumer/main_consumer.py
consumer = KafkaConsumer(
    'cinema_transactions',
    bootstrap_servers='localhost:9092',
    group_id='cinema-consumer-group',  # Same group ID
    max_poll_records=500,  # Process more records per poll
    session_timeout_ms=30000
)
```

### Materialized View Incremental Refresh

```sql
-- Replace full refresh with incremental updates
CREATE MATERIALIZED VIEW gold_cinema_analytics AS
SELECT ...
WITH DATA;

CREATE UNIQUE INDEX ON gold_cinema_analytics (cinema_location, genre, payment_method);

-- Use REFRESH MATERIALIZED VIEW CONCURRENTLY
REFRESH MATERIALIZED VIEW CONCURRENTLY gold_cinema_analytics;
```

This skill enables AI agents to help developers build production-grade real-time streaming data pipelines with proper architecture patterns, orchestration, and visualization.

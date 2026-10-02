---
name: harvard-art-museums-data-engineering-app
description: End-to-end data engineering and analytics application for Harvard Art Museums API with ETL pipelines, SQL analytics, and Streamlit visualization
triggers:
  - build an ETL pipeline for museum artifact data
  - create a data engineering app with Harvard Art Museums API
  - set up SQL analytics for art collection data
  - implement artifact data collection and visualization
  - build a Streamlit dashboard for museum artifacts
  - analyze Harvard Art Museums collection with SQL queries
  - create an end-to-end data pipeline for art metadata
  - visualize museum artifact data with interactive charts
---

# Harvard Art Museums Data Engineering App

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides an end-to-end data engineering and analytics application built on the Harvard Art Museums API. It demonstrates real-world ETL pipelines, SQL database design, analytical queries, and interactive visualization using Streamlit.

## What This Project Does

The application follows a complete data pipeline: **API → ETL → SQL → Analytics → Visualization**

- **Collects** artifact data from Harvard Art Museums API with pagination and rate limiting
- **Transforms** nested JSON into normalized relational tables
- **Loads** data into MySQL/TiDB Cloud databases
- **Analyzes** with 20+ predefined SQL queries
- **Visualizes** results through interactive Plotly dashboards in Streamlit

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export HARVARD_API_KEY="your_api_key_here"
export DB_HOST="your_database_host"
export DB_USER="your_database_user"
export DB_PASSWORD="your_database_password"
export DB_NAME="harvard_artifacts"
```

**Required dependencies:**
```
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### API Key Setup

Get a free API key from [Harvard Art Museums API](https://www.harvardartmuseums.org/collections/api):

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"
```

### Database Connection

```python
import mysql.connector
import os

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
```

## Database Schema

The application uses three normalized tables:

```sql
-- Artifact metadata table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    classification VARCHAR(200),
    department VARCHAR(200),
    dated VARCHAR(200),
    medium VARCHAR(500),
    technique VARCHAR(500),
    period VARCHAR(200),
    primaryimageurl TEXT,
    verificationlevel INT,
    accesslevel INT
);

-- Artifact media table
CREATE TABLE artifactmedia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    baseimageurl TEXT,
    format VARCHAR(50),
    height INT,
    width INT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact colors table
CREATE TABLE artifactcolors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    percentage FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## ETL Pipeline

### Extract: Fetch Data from API

```python
import requests
import time

def fetch_artifacts(api_key, num_records=100, page_size=100):
    """
    Fetch artifacts from Harvard Art Museums API with pagination
    """
    artifacts = []
    url = f"{BASE_URL}?apikey={api_key}&size={page_size}"
    
    pages_needed = (num_records + page_size - 1) // page_size
    
    for page in range(1, pages_needed + 1):
        try:
            response = requests.get(f"{url}&page={page}")
            response.raise_for_status()
            data = response.json()
            
            artifacts.extend(data.get('records', []))
            
            # Rate limiting
            time.sleep(0.5)
            
            if len(artifacts) >= num_records:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    return artifacts[:num_records]
```

### Transform: Normalize JSON Data

```python
import pandas as pd

def transform_artifact_data(artifacts):
    """
    Transform nested JSON into normalized dataframes
    """
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in artifacts:
        # Extract metadata
        metadata = {
            'id': artifact.get('id'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'medium': artifact.get('medium'),
            'technique': artifact.get('technique'),
            'period': artifact.get('period'),
            'primaryimageurl': artifact.get('primaryimageurl'),
            'verificationlevel': artifact.get('verificationlevel'),
            'accesslevel': artifact.get('accesslevel')
        }
        metadata_list.append(metadata)
        
        # Extract images/media
        images = artifact.get('images', [])
        for img in images:
            media = {
                'artifact_id': artifact.get('id'),
                'baseimageurl': img.get('baseimageurl'),
                'format': img.get('format'),
                'height': img.get('height'),
                'width': img.get('width')
            }
            media_list.append(media)
        
        # Extract colors
        colors = artifact.get('colors', [])
        for color in colors:
            color_entry = {
                'artifact_id': artifact.get('id'),
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'percentage': color.get('percent')
            }
            colors_list.append(color_entry)
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### Load: Insert into Database

```python
def load_to_database(metadata_df, media_df, colors_df, connection):
    """
    Load dataframes into SQL database with batch inserts
    """
    cursor = connection.cursor()
    
    # Insert metadata
    metadata_query = """
    INSERT INTO artifactmetadata 
    (id, title, culture, century, classification, department, dated, 
     medium, technique, period, primaryimageurl, verificationlevel, accesslevel)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE title=VALUES(title)
    """
    
    metadata_values = metadata_df.values.tolist()
    cursor.executemany(metadata_query, metadata_values)
    
    # Insert media
    media_query = """
    INSERT INTO artifactmedia (artifact_id, baseimageurl, format, height, width)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    media_values = media_df.values.tolist()
    cursor.executemany(media_query, media_values)
    
    # Insert colors
    colors_query = """
    INSERT INTO artifactcolors (artifact_id, color, spectrum, percentage)
    VALUES (%s, %s, %s, %s)
    """
    
    colors_values = colors_df.values.tolist()
    cursor.executemany(colors_query, colors_values)
    
    connection.commit()
    cursor.close()
```

## Streamlit Application

### Main App Structure

```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Harvard Art Analytics", layout="wide")

# Sidebar for data collection
with st.sidebar:
    st.header("Data Collection")
    num_records = st.slider("Number of records", 10, 500, 100)
    
    if st.button("Fetch & Load Data"):
        with st.spinner("Fetching artifacts..."):
            artifacts = fetch_artifacts(API_KEY, num_records)
            metadata_df, media_df, colors_df = transform_artifact_data(artifacts)
            load_to_database(metadata_df, media_df, colors_df, connection)
            st.success(f"Loaded {len(metadata_df)} artifacts!")

# Main dashboard
st.title("🎨 Harvard Art Museums Analytics Dashboard")

# Analytics section
st.header("SQL Analytics")

# Sample queries
queries = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as count 
        FROM artifactmetadata 
        WHERE culture IS NOT NULL 
        GROUP BY culture 
        ORDER BY count DESC 
        LIMIT 10
    """,
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count 
        FROM artifactmetadata 
        WHERE century IS NOT NULL 
        GROUP BY century 
        ORDER BY count DESC
    """,
    "Media Availability": """
        SELECT 
            CASE WHEN primaryimageurl IS NOT NULL THEN 'Has Image' ELSE 'No Image' END as status,
            COUNT(*) as count
        FROM artifactmetadata
        GROUP BY status
    """,
    "Top Colors Used": """
        SELECT color, COUNT(*) as count, AVG(percentage) as avg_percentage
        FROM artifactcolors
        GROUP BY color
        ORDER BY count DESC
        LIMIT 10
    """,
    "Artifacts by Department": """
        SELECT department, COUNT(*) as count
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY count DESC
    """
}

selected_query = st.selectbox("Select Analysis", list(queries.keys()))

if st.button("Run Analysis"):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(queries[selected_query])
    results = cursor.fetchall()
    cursor.close()
    
    df_results = pd.DataFrame(results)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.dataframe(df_results, use_container_width=True)
    
    with col2:
        if len(df_results.columns) >= 2:
            fig = px.bar(
                df_results, 
                x=df_results.columns[0], 
                y=df_results.columns[1],
                title=selected_query
            )
            st.plotly_chart(fig, use_container_width=True)
```

## Common Patterns

### Running the Complete ETL Pipeline

```python
def run_etl_pipeline(api_key, db_config, num_records=100):
    """
    Execute complete ETL pipeline
    """
    # Extract
    print("Extracting data from API...")
    artifacts = fetch_artifacts(api_key, num_records)
    
    # Transform
    print("Transforming data...")
    metadata_df, media_df, colors_df = transform_artifact_data(artifacts)
    
    # Load
    print("Loading to database...")
    connection = mysql.connector.connect(**db_config)
    load_to_database(metadata_df, media_df, colors_df, connection)
    connection.close()
    
    print(f"ETL pipeline complete: {len(metadata_df)} artifacts processed")
    return metadata_df, media_df, colors_df
```

### Incremental Data Loading

```python
def get_latest_artifact_id(connection):
    """
    Get the highest artifact ID in database
    """
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM artifactmetadata")
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] else 0

def incremental_load(api_key, db_config):
    """
    Load only new artifacts
    """
    connection = mysql.connector.connect(**db_config)
    last_id = get_latest_artifact_id(connection)
    
    # Fetch artifacts with ID filter
    url = f"{BASE_URL}?apikey={api_key}&after={last_id}"
    # Continue with ETL...
```

## Key Commands

### Run Streamlit App

```bash
streamlit run app.py
```

### Database Setup

```bash
# Create database
mysql -u $DB_USER -p -e "CREATE DATABASE harvard_artifacts;"

# Run schema creation
mysql -u $DB_USER -p harvard_artifacts < schema.sql
```

## Troubleshooting

### API Rate Limiting

If you hit rate limits, increase the delay:

```python
time.sleep(1)  # Increase from 0.5 to 1 second
```

### Database Connection Issues

```python
# Test connection
try:
    connection = mysql.connector.connect(**db_config)
    print("Connection successful!")
    connection.close()
except mysql.connector.Error as e:
    print(f"Error: {e}")
```

### Missing Data Handling

```python
# Handle None values before inserting
def safe_value(val, default=''):
    return val if val is not None else default

metadata = {
    'title': safe_value(artifact.get('title')),
    'culture': safe_value(artifact.get('culture'))
}
```

### Memory Issues with Large Datasets

```python
# Process in chunks
chunk_size = 100
for i in range(0, total_records, chunk_size):
    chunk = artifacts[i:i+chunk_size]
    process_chunk(chunk)
```

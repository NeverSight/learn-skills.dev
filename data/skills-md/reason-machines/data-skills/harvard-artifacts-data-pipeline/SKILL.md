---
name: harvard-artifacts-data-pipeline
description: Build end-to-end data engineering pipelines using Harvard Art Museums API with ETL, SQL analytics, and Streamlit visualization
triggers:
  - how do I fetch data from Harvard Art Museums API
  - build an ETL pipeline for museum artifact data
  - create a Streamlit analytics dashboard for Harvard artifacts
  - query Harvard museum collection data with SQL
  - visualize art museum data using plotly and streamlit
  - set up a data engineering project with Harvard API
  - analyze artifact metadata from Harvard Art Museums
  - implement pagination for Harvard API data collection
---

# Harvard Artifacts Data Pipeline

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## What This Project Does

The Harvard Artifacts Collection Data Engineering & Analytics App is an end-to-end data pipeline that demonstrates professional ETL workflows. It fetches artifact data from the Harvard Art Museums API, transforms it into structured relational tables, stores it in MySQL/TiDB Cloud, and provides interactive analytics through a Streamlit dashboard with Plotly visualizations.

**Key capabilities:**
- API data extraction with pagination and rate limiting
- ETL transformations for nested JSON to relational schema
- SQL database design with proper foreign keys
- 20+ predefined analytical queries
- Interactive visualization dashboards

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

**Required packages:**
```
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### API Setup

Get your Harvard Art Museums API key from: https://docs.harvardartmuseums.org/

```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"
```

### Database Schema

The project uses three main tables:

```sql
-- Artifact metadata table
CREATE TABLE artifactmetadata (
    objectid INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    division VARCHAR(200),
    classification VARCHAR(200),
    dated VARCHAR(200),
    accessionyear INT,
    peoplecount INT,
    totalpageviews INT
);

-- Artifact media table
CREATE TABLE artifactmedia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    objectid INT,
    imagecount INT,
    videocount INT,
    hasimage BOOLEAN,
    primaryimageurl TEXT,
    FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
);

-- Artifact colors table
CREATE TABLE artifactcolors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    objectid INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    hue VARCHAR(50),
    percent FLOAT,
    FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
);
```

## Key API Patterns

### Fetching Artifacts with Pagination

```python
import requests
import pandas as pd

def fetch_artifacts(api_key, num_records=100, page_size=100):
    """
    Fetch artifacts from Harvard Art Museums API with pagination
    """
    url = f"https://api.harvardartmuseums.org/object"
    params = {
        'apikey': api_key,
        'size': page_size,
        'page': 1
    }
    
    all_records = []
    
    while len(all_records) < num_records:
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
            
        data = response.json()
        records = data.get('records', [])
        
        if not records:
            break
            
        all_records.extend(records)
        params['page'] += 1
        
        # Rate limiting
        import time
        time.sleep(0.5)
    
    return all_records[:num_records]
```

### ETL Transformation

```python
def transform_artifacts(raw_data):
    """
    Transform raw API data into structured DataFrames
    """
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_data:
        # Extract metadata
        metadata = {
            'objectid': artifact.get('objectid'),
            'title': artifact.get('title'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'division': artifact.get('division'),
            'classification': artifact.get('classification'),
            'dated': artifact.get('dated'),
            'accessionyear': artifact.get('accessionyear'),
            'peoplecount': artifact.get('peoplecount', 0),
            'totalpageviews': artifact.get('totalpageviews', 0)
        }
        metadata_list.append(metadata)
        
        # Extract media info
        media = {
            'objectid': artifact.get('objectid'),
            'imagecount': artifact.get('imagecount', 0),
            'videocount': artifact.get('videocount', 0),
            'hasimage': artifact.get('primaryimageurl') is not None,
            'primaryimageurl': artifact.get('primaryimageurl')
        }
        media_list.append(media)
        
        # Extract colors
        colors = artifact.get('colors', [])
        for color in colors:
            color_data = {
                'objectid': artifact.get('objectid'),
                'color': color.get('color'),
                'spectrum': color.get('spectrum'),
                'hue': color.get('hue'),
                'percent': color.get('percent')
            }
            colors_list.append(color_data)
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

## Database Operations

### Loading Data into MySQL

```python
import mysql.connector
from mysql.connector import Error

def create_database_connection():
    """
    Create MySQL database connection
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def batch_insert_metadata(df_metadata, connection):
    """
    Batch insert artifact metadata
    """
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO artifactmetadata 
    (objectid, title, culture, century, division, classification, 
     dated, accessionyear, peoplecount, totalpageviews)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    title=VALUES(title), culture=VALUES(culture)
    """
    
    data_tuples = [tuple(row) for row in df_metadata.values]
    
    try:
        cursor.executemany(insert_query, data_tuples)
        connection.commit()
        print(f"Inserted {cursor.rowcount} records into artifactmetadata")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
```

## Analytical SQL Queries

### Example Queries

```python
ANALYTICAL_QUERIES = {
    "Top 10 Cultures by Artifact Count": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 10
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "Image Availability Analysis": """
        SELECT 
            hasimage,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM artifactmedia), 2) as percentage
        FROM artifactmedia
        GROUP BY hasimage
    """,
    
    "Top Colors Used": """
        SELECT color, COUNT(*) as usage_count, AVG(percent) as avg_percentage
        FROM artifactcolors
        WHERE color IS NOT NULL
        GROUP BY color
        ORDER BY usage_count DESC
        LIMIT 10
    """,
    
    "Most Viewed Artifacts": """
        SELECT title, culture, totalpageviews
        FROM artifactmetadata
        WHERE totalpageviews > 0
        ORDER BY totalpageviews DESC
        LIMIT 10
    """
}
```

## Streamlit Dashboard

### Basic App Structure

```python
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")
    
    st.title("🏛️ Harvard Art Museums - Data Analytics Dashboard")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # API Data Collection
    if st.sidebar.button("Fetch New Data"):
        with st.spinner("Fetching artifacts..."):
            raw_data = fetch_artifacts(API_KEY, num_records=500)
            df_meta, df_media, df_colors = transform_artifacts(raw_data)
            
            # Load to database
            conn = create_database_connection()
            if conn:
                batch_insert_metadata(df_meta, conn)
                # ... insert other tables
                st.success("Data loaded successfully!")
    
    # Analytics Section
    st.header("📊 SQL Analytics")
    
    query_name = st.selectbox("Select Analysis", list(ANALYTICAL_QUERIES.keys()))
    
    if st.button("Run Query"):
        conn = create_database_connection()
        if conn:
            df_result = pd.read_sql(ANALYTICAL_QUERIES[query_name], conn)
            
            st.subheader("Query Results")
            st.dataframe(df_result)
            
            # Auto-generate visualization
            if len(df_result.columns) >= 2:
                fig = px.bar(
                    df_result,
                    x=df_result.columns[0],
                    y=df_result.columns[1],
                    title=query_name
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

## Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# The app will be available at http://localhost:8501
```

## Common Patterns

### Error Handling for API Calls

```python
def safe_api_fetch(url, params, max_retries=3):
    """
    Fetch data with retry logic
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

### Data Validation

```python
def validate_artifact_data(df):
    """
    Validate DataFrame before database insertion
    """
    # Remove duplicates
    df = df.drop_duplicates(subset=['objectid'])
    
    # Handle null values
    df['culture'] = df['culture'].fillna('Unknown')
    df['century'] = df['century'].fillna('Unknown')
    
    # Validate data types
    df['accessionyear'] = pd.to_numeric(df['accessionyear'], errors='coerce')
    
    return df
```

## Troubleshooting

**API Rate Limiting:**
```python
# Add delays between requests
import time
time.sleep(0.5)  # 500ms delay

# Use session for connection pooling
session = requests.Session()
response = session.get(url, params=params)
```

**Database Connection Issues:**
```python
# Test connection
def test_db_connection():
    try:
        conn = create_database_connection()
        if conn and conn.is_connected():
            print("Database connection successful")
            conn.close()
            return True
    except Error as e:
        print(f"Connection failed: {e}")
        return False
```

**Memory Management for Large Datasets:**
```python
# Process in chunks
def fetch_in_batches(total_records, batch_size=100):
    for start in range(0, total_records, batch_size):
        batch = fetch_artifacts(API_KEY, num_records=batch_size)
        yield batch
```

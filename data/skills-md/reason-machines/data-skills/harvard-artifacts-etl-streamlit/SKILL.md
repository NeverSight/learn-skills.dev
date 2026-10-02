---
name: harvard-artifacts-etl-streamlit
description: ETL pipeline and analytics app for Harvard Art Museums API with SQL storage and Streamlit visualization
triggers:
  - build an ETL pipeline for museum artifacts
  - connect to Harvard Art Museums API
  - create a streamlit dashboard for art data
  - extract and transform API data to SQL
  - analyze museum collection with SQL queries
  - visualize art museum data with plotly
  - build a data engineering pipeline for artifacts
  - create analytics app for Harvard art collection
---

# Harvard Artifacts ETL & Analytics Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This skill enables AI agents to build and work with end-to-end data engineering pipelines using the Harvard Art Museums API. It demonstrates ETL workflows, SQL database design, analytics queries, and interactive Streamlit dashboards with Plotly visualizations.

## What This Project Does

The Harvard Artifacts Collection Data Engineering & Analytics App provides:

- **API Integration**: Fetch artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extract, transform, and load museum artifact data into relational SQL databases
- **SQL Database**: Store artifacts metadata, media details, and color information with proper relationships
- **Analytics Queries**: 20+ predefined SQL queries for insights on culture, century, media, colors, and departments
- **Interactive Dashboard**: Streamlit-based UI with Plotly visualizations for real-time analytics

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

### Required Dependencies

```txt
streamlit
pandas
requests
mysql-connector-python
plotly
python-dotenv
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Harvard Art Museums API
HARVARD_API_KEY=your_api_key_here

# MySQL/TiDB Configuration
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=harvard_artifacts
```

### API Key Setup

Get your free API key from [Harvard Art Museums API](https://harvardartmuseums.org/collections/api):

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('HARVARD_API_KEY')
```

## Database Schema

### Tables Structure

```sql
-- Artifact Metadata
CREATE TABLE artifactmetadata (
    artifact_id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    department VARCHAR(255),
    dated VARCHAR(255),
    description TEXT,
    accession_number VARCHAR(100),
    primary_image_url TEXT
);

-- Artifact Media
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    media_type VARCHAR(50),
    media_url TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
);

-- Artifact Colors
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color_hex VARCHAR(10),
    color_name VARCHAR(100),
    percentage FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
);
```

## ETL Pipeline Implementation

### 1. Extract Data from API

```python
import requests
import pandas as pd

def fetch_artifacts(api_key, page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API"""
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data['records'], data['info']

# Paginated extraction
def extract_all_artifacts(api_key, max_pages=10):
    """Extract artifacts with pagination"""
    all_artifacts = []
    
    for page in range(1, max_pages + 1):
        records, info = fetch_artifacts(api_key, page=page)
        all_artifacts.extend(records)
        
        if page >= info['pages']:
            break
    
    return all_artifacts
```

### 2. Transform Data

```python
def transform_artifacts(raw_artifacts):
    """Transform nested JSON to relational format"""
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_artifacts:
        # Metadata extraction
        metadata = {
            'artifact_id': artifact.get('id'),
            'title': artifact.get('title', 'Unknown'),
            'culture': artifact.get('culture'),
            'century': artifact.get('century'),
            'classification': artifact.get('classification'),
            'department': artifact.get('department'),
            'dated': artifact.get('dated'),
            'description': artifact.get('description'),
            'accession_number': artifact.get('accessionNumber'),
            'primary_image_url': artifact.get('primaryimageurl')
        }
        metadata_list.append(metadata)
        
        # Media extraction
        if 'images' in artifact and artifact['images']:
            for img in artifact['images']:
                media = {
                    'artifact_id': artifact.get('id'),
                    'media_type': 'image',
                    'media_url': img.get('baseimageurl')
                }
                media_list.append(media)
        
        # Colors extraction
        if 'colors' in artifact and artifact['colors']:
            for color in artifact['colors']:
                color_data = {
                    'artifact_id': artifact.get('id'),
                    'color_hex': color.get('hex'),
                    'color_name': color.get('color'),
                    'percentage': color.get('percent')
                }
                colors_list.append(color_data)
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### 3. Load to SQL Database

```python
import mysql.connector
from mysql.connector import Error

def create_connection(host, port, user, password, database):
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def load_to_database(df_metadata, df_media, df_colors, connection):
    """Batch insert data into SQL database"""
    cursor = connection.cursor()
    
    # Load metadata
    for _, row in df_metadata.iterrows():
        query = """
        INSERT INTO artifactmetadata 
        (artifact_id, title, culture, century, classification, department, 
         dated, description, accession_number, primary_image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
        """
        cursor.execute(query, tuple(row))
    
    # Load media
    for _, row in df_media.iterrows():
        query = """
        INSERT INTO artifactmedia (artifact_id, media_type, media_url)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, tuple(row))
    
    # Load colors
    for _, row in df_colors.iterrows():
        query = """
        INSERT INTO artifactcolors (artifact_id, color_hex, color_name, percentage)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, tuple(row))
    
    connection.commit()
    cursor.close()
```

## Analytics Queries

### Sample SQL Analytics

```python
ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY count DESC
        LIMIT 15
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "Top Colors in Collection": """
        SELECT color_name, COUNT(*) as frequency, AVG(percentage) as avg_percentage
        FROM artifactcolors
        GROUP BY color_name
        ORDER BY frequency DESC
        LIMIT 20
    """,
    
    "Department Distribution": """
        SELECT department, COUNT(*) as artifact_count
        FROM artifactmetadata
        GROUP BY department
        ORDER BY artifact_count DESC
    """,
    
    "Media Availability": """
        SELECT 
            COUNT(DISTINCT am.artifact_id) as total_artifacts,
            COUNT(DISTINCT m.artifact_id) as artifacts_with_media,
            ROUND(COUNT(DISTINCT m.artifact_id) * 100.0 / COUNT(DISTINCT am.artifact_id), 2) as coverage_percentage
        FROM artifactmetadata am
        LEFT JOIN artifactmedia m ON am.artifact_id = m.artifact_id
    """
}

def execute_query(connection, query):
    """Execute SQL query and return results as DataFrame"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(results)
```

## Streamlit Dashboard

### Main Application Structure

```python
import streamlit as st
import plotly.express as px
import os

st.set_page_config(page_title="Harvard Artifacts Analytics", layout="wide")

# Sidebar configuration
st.sidebar.title("🎨 Harvard Art Analytics")
st.sidebar.markdown("---")

# Database connection
@st.cache_resource
def get_db_connection():
    return create_connection(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Main app
def main():
    st.title("📊 Harvard Artifacts Collection Analytics")
    
    conn = get_db_connection()
    
    # Query selector
    query_name = st.selectbox(
        "Select Analytics Query:",
        list(ANALYTICS_QUERIES.keys())
    )
    
    if st.button("Run Query"):
        with st.spinner("Executing query..."):
            df_results = execute_query(conn, ANALYTICS_QUERIES[query_name])
            
            # Display results
            st.subheader("Query Results")
            st.dataframe(df_results)
            
            # Visualization
            if len(df_results.columns) >= 2:
                st.subheader("Visualization")
                fig = px.bar(
                    df_results,
                    x=df_results.columns[0],
                    y=df_results.columns[1],
                    title=query_name
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
```

## Running the Application

```bash
# Start Streamlit app
streamlit run app.py

# Access dashboard at http://localhost:8501
```

## Common Patterns

### Complete ETL Workflow

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv('HARVARD_API_KEY')
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Execute ETL
def run_etl_pipeline():
    # Extract
    print("Extracting data from API...")
    raw_artifacts = extract_all_artifacts(API_KEY, max_pages=5)
    
    # Transform
    print("Transforming data...")
    df_metadata, df_media, df_colors = transform_artifacts(raw_artifacts)
    
    # Load
    print("Loading to database...")
    conn = create_connection(**DB_CONFIG)
    load_to_database(df_metadata, df_media, df_colors, conn)
    conn.close()
    
    print(f"ETL Complete: {len(df_metadata)} artifacts processed")

if __name__ == "__main__":
    run_etl_pipeline()
```

## Troubleshooting

### API Rate Limiting

```python
import time

def fetch_with_retry(api_key, page, max_retries=3):
    """Fetch with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return fetch_artifacts(api_key, page)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too many requests
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Database Connection Issues

```python
def verify_connection(connection):
    """Test database connection"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return True
    except Error as e:
        print(f"Connection failed: {e}")
        return False
```

### Handling Missing Data

```python
def safe_get(dictionary, key, default='Unknown'):
    """Safely extract values from nested JSON"""
    value = dictionary.get(key, default)
    return value if value else default
```

This skill provides complete ETL pipeline implementation for museum artifact data with SQL analytics and interactive visualization capabilities.

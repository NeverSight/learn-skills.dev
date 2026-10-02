---
name: harvard-artifacts-collection-data-engineering
description: End-to-end data engineering and analytics application for Harvard Art Museums API with ETL pipelines, SQL analytics, and Streamlit visualization
triggers:
  - build an ETL pipeline for museum artifact data
  - connect to Harvard Art Museums API
  - create a data engineering pipeline with Streamlit
  - analyze Harvard museum collection with SQL
  - set up artifact collection data warehouse
  - visualize museum data with interactive dashboards
  - implement batch data loading from Harvard API
  - query and analyze art museum metadata
---

# Harvard Artifacts Collection Data Engineering

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project provides an end-to-end data engineering and analytics application built on the Harvard Art Museums API. It demonstrates real-world ETL pipelines, SQL database design, analytical queries, and interactive visualization using Streamlit. The architecture follows: API → ETL → SQL → Analytics → Visualization.

## What This Project Does

- **API Integration**: Fetches artifact data from Harvard Art Museums API with pagination and rate limiting
- **ETL Pipeline**: Extracts, transforms, and loads nested JSON into relational database tables
- **SQL Database**: Stores structured data across `artifactmetadata`, `artifactmedia`, and `artifactcolors` tables
- **Analytics**: Executes 20+ predefined SQL queries for insights
- **Visualization**: Interactive dashboards using Plotly and Streamlit

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

**Required packages:**
```txt
streamlit
pandas
requests
mysql-connector-python
plotly
```

## Configuration

### Environment Variables

Set up your configuration before running:

```bash
# Harvard Art Museums API Key (get from https://www.harvardartmuseums.org/collections/api)
export HARVARD_API_KEY="your_api_key_here"

# Database credentials
export DB_HOST="your_database_host"
export DB_PORT="3306"
export DB_USER="your_database_user"
export DB_PASSWORD="your_database_password"
export DB_NAME="harvard_artifacts"
```

### Database Setup

Create the required tables:

```sql
CREATE DATABASE harvard_artifacts;
USE harvard_artifacts;

CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(100),
    classification VARCHAR(255),
    division VARCHAR(255),
    department VARCHAR(255),
    technique VARCHAR(500),
    period VARCHAR(255),
    dated VARCHAR(255),
    url TEXT,
    lastupdate DATETIME
);

CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    baseimageurl TEXT,
    iiifbaseuri TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    spectrum VARCHAR(50),
    percentage FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Key Components and Usage

### 1. API Data Extraction

```python
import requests
import os

class HarvardAPIClient:
    def __init__(self):
        self.api_key = os.getenv('HARVARD_API_KEY')
        self.base_url = "https://api.harvardartmuseums.org/object"
    
    def fetch_artifacts(self, page=1, size=100):
        """Fetch artifacts with pagination"""
        params = {
            'apikey': self.api_key,
            'page': page,
            'size': size,
            'hasimage': 1  # Only artifacts with images
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    def fetch_multiple_pages(self, num_pages=10):
        """Fetch multiple pages of artifacts"""
        all_artifacts = []
        for page in range(1, num_pages + 1):
            data = self.fetch_artifacts(page=page)
            all_artifacts.extend(data.get('records', []))
        return all_artifacts
```

### 2. ETL Pipeline Implementation

```python
import pandas as pd
import mysql.connector
from typing import List, Dict

class ArtifactETL:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        
    def connect_db(self):
        """Establish database connection"""
        self.conn = mysql.connector.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
        return self.conn
    
    def transform_artifacts(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Transform raw JSON to structured DataFrame"""
        artifacts = []
        for item in raw_data:
            artifact = {
                'id': item.get('id'),
                'title': item.get('title', '')[:500],
                'culture': item.get('culture', ''),
                'century': item.get('century', ''),
                'classification': item.get('classification', ''),
                'division': item.get('division', ''),
                'department': item.get('department', ''),
                'technique': item.get('technique', ''),
                'period': item.get('period', ''),
                'dated': item.get('dated', ''),
                'url': item.get('url', ''),
                'lastupdate': item.get('lastupdate', '')
            }
            artifacts.append(artifact)
        return pd.DataFrame(artifacts)
    
    def transform_media(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Extract media information"""
        media_records = []
        for item in raw_data:
            artifact_id = item.get('id')
            if 'primaryimageurl' in item:
                media_records.append({
                    'artifact_id': artifact_id,
                    'baseimageurl': item.get('primaryimageurl', ''),
                    'iiifbaseuri': item.get('iiifbaseuri', '')
                })
        return pd.DataFrame(media_records)
    
    def transform_colors(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Extract color information"""
        color_records = []
        for item in raw_data:
            artifact_id = item.get('id')
            colors = item.get('colors', [])
            for color in colors:
                color_records.append({
                    'artifact_id': artifact_id,
                    'color': color.get('color', ''),
                    'spectrum': color.get('spectrum', ''),
                    'percentage': color.get('percent', 0)
                })
        return pd.DataFrame(color_records)
    
    def load_data(self, df: pd.DataFrame, table_name: str):
        """Batch insert data into SQL table"""
        cursor = self.conn.cursor()
        
        # Prepare column names and placeholders
        cols = ','.join(df.columns)
        placeholders = ','.join(['%s'] * len(df.columns))
        
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        
        # Convert DataFrame to list of tuples
        data = [tuple(row) for row in df.values]
        
        # Execute batch insert
        cursor.executemany(sql, data)
        self.conn.commit()
        cursor.close()
        
        return len(data)
```

### 3. Complete ETL Workflow

```python
def run_etl_pipeline():
    """Execute complete ETL pipeline"""
    # Configuration
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    
    # Initialize clients
    api_client = HarvardAPIClient()
    etl = ArtifactETL(db_config)
    etl.connect_db()
    
    # Extract
    print("Extracting data from API...")
    raw_artifacts = api_client.fetch_multiple_pages(num_pages=5)
    print(f"Extracted {len(raw_artifacts)} artifacts")
    
    # Transform
    print("Transforming data...")
    df_artifacts = etl.transform_artifacts(raw_artifacts)
    df_media = etl.transform_media(raw_artifacts)
    df_colors = etl.transform_colors(raw_artifacts)
    
    # Load
    print("Loading data to database...")
    etl.load_data(df_artifacts, 'artifactmetadata')
    etl.load_data(df_media, 'artifactmedia')
    etl.load_data(df_colors, 'artifactcolors')
    
    print("ETL pipeline completed successfully!")
    etl.conn.close()
```

### 4. SQL Analytics Queries

```python
class ArtifactAnalytics:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return DataFrame"""
        conn = mysql.connector.connect(**self.db_config)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    def get_artifacts_by_culture(self):
        """Get artifact distribution by culture"""
        query = """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL AND culture != ''
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 20;
        """
        return self.execute_query(query)
    
    def get_artifacts_by_century(self):
        """Get artifact distribution by century"""
        query = """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL AND century != ''
        GROUP BY century
        ORDER BY count DESC;
        """
        return self.execute_query(query)
    
    def get_color_distribution(self):
        """Get color usage across artifacts"""
        query = """
        SELECT color, COUNT(*) as frequency, AVG(percentage) as avg_percentage
        FROM artifactcolors
        GROUP BY color
        ORDER BY frequency DESC
        LIMIT 15;
        """
        return self.execute_query(query)
    
    def get_artifacts_with_media(self):
        """Get artifacts with and without media"""
        query = """
        SELECT 
            CASE WHEN m.artifact_id IS NOT NULL THEN 'With Media' ELSE 'Without Media' END as media_status,
            COUNT(*) as count
        FROM artifactmetadata a
        LEFT JOIN artifactmedia m ON a.id = m.artifact_id
        GROUP BY media_status;
        """
        return self.execute_query(query)
```

### 5. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def create_dashboard():
    st.title("Harvard Art Museums Analytics Dashboard")
    
    # Sidebar for navigation
    st.sidebar.header("Navigation")
    option = st.sidebar.selectbox(
        "Choose Analysis",
        ["Overview", "Culture Analysis", "Century Distribution", "Color Patterns", "Media Analysis"]
    )
    
    # Initialize analytics
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    analytics = ArtifactAnalytics(db_config)
    
    if option == "Culture Analysis":
        st.header("Artifacts by Culture")
        df = analytics.get_artifacts_by_culture()
        
        # Display data table
        st.dataframe(df)
        
        # Create visualization
        fig = px.bar(df, x='culture', y='artifact_count', 
                     title='Top 20 Cultures by Artifact Count')
        st.plotly_chart(fig)
    
    elif option == "Century Distribution":
        st.header("Artifacts by Century")
        df = analytics.get_artifacts_by_century()
        
        st.dataframe(df)
        
        fig = px.bar(df, x='century', y='count',
                     title='Artifact Distribution Across Centuries')
        st.plotly_chart(fig)
    
    elif option == "Color Patterns":
        st.header("Color Usage Analysis")
        df = analytics.get_color_distribution()
        
        st.dataframe(df)
        
        fig = px.bar(df, x='color', y='frequency',
                     title='Most Common Colors in Artifacts')
        st.plotly_chart(fig)

if __name__ == "__main__":
    create_dashboard()
```

## Running the Application

```bash
# Start the Streamlit dashboard
streamlit run app.py

# Run ETL pipeline separately (if needed)
python etl_pipeline.py
```

## Common Patterns

### Incremental Data Loading

```python
def incremental_load(last_update_date):
    """Load only new or updated artifacts"""
    query = f"""
    SELECT id FROM artifactmetadata 
    WHERE lastupdate > '{last_update_date}'
    """
    # Fetch only updated records from API
    # Update existing records in database
```

### Error Handling in ETL

```python
def safe_etl_run():
    try:
        run_etl_pipeline()
    except requests.HTTPError as e:
        print(f"API Error: {e}")
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
```

## Troubleshooting

**API Rate Limiting**: Add delays between requests
```python
import time
time.sleep(0.5)  # 500ms delay between API calls
```

**Database Connection Issues**: Verify credentials and network access
```python
# Test connection
try:
    conn = mysql.connector.connect(**db_config)
    print("Database connection successful")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

**Missing Data Fields**: Handle null values during transformation
```python
artifact = {
    'title': item.get('title', 'Unknown')[:500],
    'culture': item.get('culture') or 'Not Specified'
}
```

**Memory Issues with Large Datasets**: Use chunking
```python
chunk_size = 1000
for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    etl.load_data(pd.DataFrame(chunk), 'artifactmetadata')
```

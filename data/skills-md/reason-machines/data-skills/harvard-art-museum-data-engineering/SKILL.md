---
name: harvard-art-museum-data-engineering
description: ETL pipeline and analytics app for Harvard Art Museums API using Python, SQL, and Streamlit
triggers:
  - build a data pipeline for Harvard Art Museums
  - create ETL process for museum artifacts
  - analyze Harvard museum collection data
  - build analytics dashboard for art museum data
  - extract and transform Harvard API data
  - query Harvard Art Museums database
  - visualize museum artifact analytics
  - implement art collection data warehouse
---

# Harvard Art Museum Data Engineering Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project provides an end-to-end data engineering solution for the Harvard Art Museums API. It implements a complete ETL pipeline that extracts artifact data, transforms it into relational tables, loads it into SQL databases (MySQL/TiDB), and provides interactive analytics dashboards using Streamlit.

**Architecture Flow**: API → ETL → SQL → Analytics → Visualization

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Required packages
pip install streamlit pandas requests mysql-connector-python plotly python-dotenv
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Harvard API Configuration
HARVARD_API_KEY=your_api_key_here

# Database Configuration
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=harvard_artifacts
```

### Getting Harvard API Key

1. Visit: https://docs.api.harvardartmuseums.org/
2. Register for a free API key
3. Store it in your `.env` file

## Database Schema

The project uses three main tables with relational structure:

```sql
-- Artifact Metadata Table
CREATE TABLE artifactmetadata (
    artifact_id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(200),
    century VARCHAR(100),
    classification VARCHAR(200),
    department VARCHAR(200),
    division VARCHAR(200),
    technique VARCHAR(300),
    period VARCHAR(200),
    people VARCHAR(500),
    url TEXT,
    last_updated DATETIME
);

-- Artifact Media Table
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    image_url TEXT,
    media_type VARCHAR(50),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
);

-- Artifact Colors Table
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color_hex VARCHAR(10),
    color_percent DECIMAL(5,2),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(artifact_id)
);
```

## Core Usage Patterns

### 1. API Data Extraction

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(page=1, size=100):
    """Fetch artifacts from Harvard API with pagination"""
    api_key = os.getenv('HARVARD_API_KEY')
    base_url = "https://api.harvardartmuseums.org/object"
    
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['records'], data['info']
    else:
        raise Exception(f"API Error: {response.status_code}")

# Fetch multiple pages
def collect_artifacts(total_records=500):
    """Collect artifacts with pagination handling"""
    all_artifacts = []
    page = 1
    page_size = 100
    
    while len(all_artifacts) < total_records:
        records, info = fetch_artifacts(page=page, size=page_size)
        all_artifacts.extend(records)
        
        if page >= info['pages']:
            break
        page += 1
    
    return all_artifacts[:total_records]
```

### 2. ETL Pipeline Implementation

```python
import pandas as pd
from datetime import datetime

def transform_artifacts(raw_data):
    """Transform API JSON to relational DataFrames"""
    
    # Metadata transformation
    metadata_list = []
    media_list = []
    colors_list = []
    
    for artifact in raw_data:
        # Extract metadata
        metadata_list.append({
            'artifact_id': artifact.get('id'),
            'title': artifact.get('title', '')[:500],
            'culture': artifact.get('culture', '')[:200],
            'century': artifact.get('century', '')[:100],
            'classification': artifact.get('classification', '')[:200],
            'department': artifact.get('department', '')[:200],
            'division': artifact.get('division', '')[:200],
            'technique': artifact.get('technique', '')[:300],
            'period': artifact.get('period', '')[:200],
            'people': str(artifact.get('people', []))[:500],
            'url': artifact.get('url', ''),
            'last_updated': datetime.now()
        })
        
        # Extract media/images
        if 'images' in artifact and artifact['images']:
            for img in artifact['images']:
                media_list.append({
                    'artifact_id': artifact.get('id'),
                    'image_url': img.get('baseimageurl', ''),
                    'media_type': 'image'
                })
        
        # Extract colors
        if 'colors' in artifact and artifact['colors']:
            for color in artifact['colors']:
                colors_list.append({
                    'artifact_id': artifact.get('id'),
                    'color_hex': color.get('hex', ''),
                    'color_percent': color.get('percent', 0)
                })
    
    return (
        pd.DataFrame(metadata_list),
        pd.DataFrame(media_list),
        pd.DataFrame(colors_list)
    )
```

### 3. Database Loading

```python
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create database connection"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def load_to_database(metadata_df, media_df, colors_df):
    """Batch insert data into SQL database"""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Load metadata (with REPLACE to handle duplicates)
        metadata_query = """
        REPLACE INTO artifactmetadata 
        (artifact_id, title, culture, century, classification, 
         department, division, technique, period, people, url, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(metadata_query, metadata_df.values.tolist())
        
        # Load media
        media_query = """
        INSERT INTO artifactmedia (artifact_id, image_url, media_type)
        VALUES (%s, %s, %s)
        """
        cursor.executemany(media_query, media_df.values.tolist())
        
        # Load colors
        colors_query = """
        INSERT INTO artifactcolors (artifact_id, color_hex, color_percent)
        VALUES (%s, %s, %s)
        """
        cursor.executemany(colors_query, colors_df.values.tolist())
        
        conn.commit()
        print(f"Loaded {len(metadata_df)} artifacts successfully")
        
    except Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
```

### 4. Analytics Queries

```python
def execute_analytics_query(query):
    """Execute analytical SQL query and return DataFrame"""
    conn = get_db_connection()
    
    try:
        df = pd.read_sql(query, conn)
        return df
    except Error as e:
        print(f"Query error: {e}")
        return None
    finally:
        conn.close()

# Example analytics queries
ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL AND culture != ''
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 15
    """,
    
    "Artifacts by Century": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL AND century != ''
        GROUP BY century
        ORDER BY count DESC
        LIMIT 20
    """,
    
    "Department Distribution": """
        SELECT department, COUNT(*) as total_artifacts
        FROM artifactmetadata
        GROUP BY department
        ORDER BY total_artifacts DESC
    """,
    
    "Most Common Colors": """
        SELECT color_hex, COUNT(*) as usage_count,
               AVG(color_percent) as avg_percent
        FROM artifactcolors
        GROUP BY color_hex
        ORDER BY usage_count DESC
        LIMIT 20
    """,
    
    "Artifacts with Multiple Images": """
        SELECT m.title, m.culture, COUNT(media.media_id) as image_count
        FROM artifactmetadata m
        JOIN artifactmedia media ON m.artifact_id = media.artifact_id
        GROUP BY m.artifact_id, m.title, m.culture
        HAVING image_count > 1
        ORDER BY image_count DESC
        LIMIT 20
    """
}
```

### 5. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def create_dashboard():
    """Main Streamlit dashboard application"""
    
    st.title("🏛️ Harvard Art Museums Analytics Dashboard")
    st.markdown("End-to-end data engineering and analytics application")
    
    # Sidebar for query selection
    st.sidebar.header("Analytics Options")
    query_name = st.sidebar.selectbox(
        "Select Analysis",
        list(ANALYTICS_QUERIES.keys())
    )
    
    # Execute query
    if st.sidebar.button("Run Analysis"):
        with st.spinner("Executing query..."):
            query = ANALYTICS_QUERIES[query_name]
            df = execute_analytics_query(query)
            
            if df is not None and not df.empty:
                st.success(f"Retrieved {len(df)} records")
                
                # Display table
                st.subheader("Query Results")
                st.dataframe(df)
                
                # Auto-generate visualization
                if len(df.columns) >= 2:
                    st.subheader("Visualization")
                    fig = px.bar(
                        df.head(20), 
                        x=df.columns[0], 
                        y=df.columns[1],
                        title=query_name
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{query_name.replace(' ', '_')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    create_dashboard()
```

## Running the Application

```bash
# Start the Streamlit dashboard
streamlit run app.py

# Access at http://localhost:8501
```

## Complete ETL Workflow

```python
def run_complete_etl(num_artifacts=500):
    """Execute full ETL pipeline"""
    
    print("Step 1: Extracting data from Harvard API...")
    raw_data = collect_artifacts(total_records=num_artifacts)
    
    print("Step 2: Transforming data...")
    metadata_df, media_df, colors_df = transform_artifacts(raw_data)
    
    print("Step 3: Loading to database...")
    load_to_database(metadata_df, media_df, colors_df)
    
    print("ETL Pipeline completed successfully!")
    print(f"Loaded {len(metadata_df)} artifacts")
    print(f"Loaded {len(media_df)} media records")
    print(f"Loaded {len(colors_df)} color records")

# Run the pipeline
if __name__ == "__main__":
    run_complete_etl(num_artifacts=1000)
```

## Common Troubleshooting

### API Rate Limiting
```python
import time

def fetch_with_retry(page, max_retries=3):
    """Fetch with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return fetch_artifacts(page=page)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retry {attempt + 1} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e
```

### Database Connection Issues
```python
def test_db_connection():
    """Test database connectivity"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✓ Database connection successful")
        conn.close()
        return True
    except Error as e:
        print(f"✗ Database connection failed: {e}")
        return False
```

### Handling Missing Data
```python
def safe_extract(artifact, field, default=''):
    """Safely extract nested fields"""
    try:
        value = artifact.get(field, default)
        return value if value is not None else default
    except (AttributeError, TypeError):
        return default
```

## Best Practices

1. **Always use environment variables** for sensitive credentials
2. **Implement pagination** when fetching large datasets
3. **Use batch inserts** for better database performance
4. **Handle API rate limits** with retry logic
5. **Validate data** before loading to database
6. **Create indexes** on frequently queried columns
7. **Log ETL operations** for debugging and monitoring

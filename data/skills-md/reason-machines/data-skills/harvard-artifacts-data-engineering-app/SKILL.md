---
name: harvard-artifacts-data-engineering-app
description: Build ETL pipelines and analytics dashboards using the Harvard Art Museums API with SQL storage and Streamlit visualization
triggers:
  - build a data pipeline for museum artifacts
  - create an ETL workflow with Harvard Art Museums API
  - analyze art collection data with SQL
  - visualize museum artifacts data in Streamlit
  - extract and transform API data into relational database
  - build analytics dashboard for art museum collections
  - create data engineering pipeline for cultural artifacts
  - query and visualize Harvard museum data
---

# Harvard Artifacts Data Engineering App

> Skill by [ara.so](https://ara.so) — Data Skills collection.

This project demonstrates end-to-end data engineering using the Harvard Art Museums API. It extracts artifact data, transforms it into relational tables, loads it into SQL databases (MySQL/TiDB), and provides interactive analytics through Streamlit dashboards with Plotly visualizations.

## What It Does

- **API Integration**: Fetches paginated artifact data from Harvard Art Museums API
- **ETL Pipeline**: Transforms nested JSON into normalized relational tables
- **SQL Storage**: Creates and populates `artifactmetadata`, `artifactmedia`, and `artifactcolors` tables
- **Analytics Queries**: 20+ predefined SQL queries for artifact insights
- **Interactive Visualization**: Streamlit dashboard with Plotly charts

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

### Requirements

```txt
streamlit
pandas
requests
pymysql
plotly
python-dotenv
```

## Configuration

### Database Setup

The application expects a MySQL/TiDB database with three main tables:

```python
import pymysql
import os

# Database connection
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

# Create tables
def create_tables(connection):
    with connection.cursor() as cursor:
        # Artifact Metadata table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            id INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(255),
            period VARCHAR(255),
            century VARCHAR(100),
            classification VARCHAR(255),
            department VARCHAR(255),
            technique VARCHAR(500),
            dated VARCHAR(255)
        )
        """)
        
        # Artifact Media table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            media_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            baseimageurl VARCHAR(1000),
            primaryimageurl VARCHAR(1000),
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
        """)
        
        # Artifact Colors table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            color_id INT AUTO_INCREMENT PRIMARY KEY,
            artifact_id INT,
            color VARCHAR(50),
            spectrum VARCHAR(50),
            percentage FLOAT,
            FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
        )
        """)
        
    connection.commit()
```

### API Configuration

```python
import requests
import os

API_KEY = os.getenv('HARVARD_API_KEY')
BASE_URL = "https://api.harvardartmuseums.org/object"

def fetch_artifacts(page=1, size=100):
    """Fetch artifacts from Harvard Art Museums API"""
    params = {
        'apikey': API_KEY,
        'page': page,
        'size': size
    }
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
```

## Key Components

### 1. ETL Pipeline

```python
import pandas as pd

def extract_artifacts(num_pages=5):
    """Extract artifacts from API"""
    all_records = []
    
    for page in range(1, num_pages + 1):
        data = fetch_artifacts(page=page, size=100)
        records = data.get('records', [])
        all_records.extend(records)
        
        # Respect rate limits
        if not data.get('info', {}).get('next'):
            break
    
    return all_records

def transform_artifacts(records):
    """Transform nested JSON to relational format"""
    metadata = []
    media = []
    colors = []
    
    for record in records:
        artifact_id = record.get('id')
        
        # Extract metadata
        metadata.append({
            'id': artifact_id,
            'title': record.get('title'),
            'culture': record.get('culture'),
            'period': record.get('period'),
            'century': record.get('century'),
            'classification': record.get('classification'),
            'department': record.get('department'),
            'technique': record.get('technique'),
            'dated': record.get('dated')
        })
        
        # Extract media
        media.append({
            'artifact_id': artifact_id,
            'baseimageurl': record.get('baseimageurl'),
            'primaryimageurl': record.get('primaryimageurl')
        })
        
        # Extract colors
        for color_data in record.get('colors', []):
            colors.append({
                'artifact_id': artifact_id,
                'color': color_data.get('color'),
                'spectrum': color_data.get('spectrum'),
                'percentage': color_data.get('percent')
            })
    
    return (
        pd.DataFrame(metadata),
        pd.DataFrame(media),
        pd.DataFrame(colors)
    )

def load_to_database(df_metadata, df_media, df_colors):
    """Load dataframes to SQL database"""
    connection = get_db_connection()
    
    try:
        # Load metadata
        for _, row in df_metadata.iterrows():
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO artifactmetadata 
                (id, title, culture, period, century, classification, department, technique, dated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE title=VALUES(title)
                """, tuple(row))
        
        # Load media
        for _, row in df_media.iterrows():
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO artifactmedia (artifact_id, baseimageurl, primaryimageurl)
                VALUES (%s, %s, %s)
                """, tuple(row))
        
        # Load colors
        for _, row in df_colors.iterrows():
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO artifactcolors (artifact_id, color, spectrum, percentage)
                VALUES (%s, %s, %s, %s)
                """, tuple(row))
        
        connection.commit()
    finally:
        connection.close()
```

### 2. SQL Analytics Queries

```python
# Sample analytical queries
ANALYTICS_QUERIES = {
    "Artifacts by Culture": """
        SELECT culture, COUNT(*) as artifact_count
        FROM artifactmetadata
        WHERE culture IS NOT NULL
        GROUP BY culture
        ORDER BY artifact_count DESC
        LIMIT 10
    """,
    
    "Century Distribution": """
        SELECT century, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL
        GROUP BY century
        ORDER BY count DESC
    """,
    
    "Department Statistics": """
        SELECT department, 
               COUNT(*) as total_artifacts,
               COUNT(DISTINCT culture) as cultures_represented
        FROM artifactmetadata
        WHERE department IS NOT NULL
        GROUP BY department
        ORDER BY total_artifacts DESC
    """,
    
    "Media Availability": """
        SELECT 
            SUM(CASE WHEN primaryimageurl IS NOT NULL THEN 1 ELSE 0 END) as with_image,
            SUM(CASE WHEN primaryimageurl IS NULL THEN 1 ELSE 0 END) as without_image
        FROM artifactmedia
    """,
    
    "Top Colors": """
        SELECT color, spectrum, 
               COUNT(*) as occurrences,
               AVG(percentage) as avg_percentage
        FROM artifactcolors
        GROUP BY color, spectrum
        ORDER BY occurrences DESC
        LIMIT 15
    """,
    
    "Classification by Century": """
        SELECT century, classification, COUNT(*) as count
        FROM artifactmetadata
        WHERE century IS NOT NULL AND classification IS NOT NULL
        GROUP BY century, classification
        ORDER BY century, count DESC
    """
}

def execute_query(query_name):
    """Execute analytical query and return results"""
    connection = get_db_connection()
    
    try:
        df = pd.read_sql(ANALYTICS_QUERIES[query_name], connection)
        return df
    finally:
        connection.close()
```

### 3. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.title("Harvard Art Museums Analytics Dashboard")
    
    # Sidebar for ETL controls
    st.sidebar.header("Data Collection")
    num_pages = st.sidebar.slider("Number of pages to fetch", 1, 10, 5)
    
    if st.sidebar.button("Run ETL Pipeline"):
        with st.spinner("Extracting data from API..."):
            records = extract_artifacts(num_pages)
            st.success(f"Extracted {len(records)} artifacts")
        
        with st.spinner("Transforming data..."):
            df_metadata, df_media, df_colors = transform_artifacts(records)
            st.success("Data transformed")
        
        with st.spinner("Loading to database..."):
            load_to_database(df_metadata, df_media, df_colors)
            st.success("Data loaded successfully")
    
    # Analytics section
    st.header("Analytics Queries")
    
    query_name = st.selectbox("Select Query", list(ANALYTICS_QUERIES.keys()))
    
    if st.button("Execute Query"):
        df_result = execute_query(query_name)
        
        # Display table
        st.dataframe(df_result)
        
        # Auto-generate visualization
        if len(df_result.columns) >= 2:
            fig = px.bar(
                df_result,
                x=df_result.columns[0],
                y=df_result.columns[1],
                title=query_name
            )
            st.plotly_chart(fig)
        
        # Download option
        csv = df_result.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{query_name.replace(' ', '_')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
```

## Running the Application

```bash
# Start the Streamlit dashboard
streamlit run app.py

# The app will be available at http://localhost:8501
```

## Common Patterns

### Batch Processing

```python
def batch_insert(connection, table, data, batch_size=1000):
    """Insert data in batches for better performance"""
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        # Insert batch logic here
        connection.commit()
```

### Error Handling for API Calls

```python
import time

def fetch_with_retry(url, params, max_retries=3):
    """Fetch data with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Data Quality Checks

```python
def validate_artifacts(df):
    """Validate artifact data quality"""
    checks = {
        'missing_ids': df['id'].isna().sum(),
        'duplicate_ids': df['id'].duplicated().sum(),
        'missing_titles': df['title'].isna().sum(),
        'total_records': len(df)
    }
    return checks
```

## Troubleshooting

### API Rate Limits
If you encounter rate limit errors:
```python
import time

# Add delay between requests
time.sleep(0.5)  # 500ms delay

# Or implement exponential backoff
```

### Database Connection Issues
```python
# Test connection
try:
    connection = get_db_connection()
    connection.ping(reconnect=True)
    print("Database connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
```

### Memory Issues with Large Datasets
```python
# Process in chunks
chunk_size = 100
for i in range(0, total_records, chunk_size):
    chunk = records[i:i + chunk_size]
    process_chunk(chunk)
```

### Streamlit Caching
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_query(query_name):
    return execute_query(query_name)
```

## Advanced Usage

### Custom Query Builder

```python
def build_custom_query(filters):
    """Build dynamic SQL query from user filters"""
    base_query = "SELECT * FROM artifactmetadata WHERE 1=1"
    
    if filters.get('culture'):
        base_query += f" AND culture = '{filters['culture']}'"
    
    if filters.get('century'):
        base_query += f" AND century = '{filters['century']}'"
    
    if filters.get('department'):
        base_query += f" AND department = '{filters['department']}'"
    
    return base_query
```

### Export to Multiple Formats

```python
def export_results(df, format='csv'):
    """Export query results to various formats"""
    if format == 'csv':
        return df.to_csv(index=False)
    elif format == 'json':
        return df.to_json(orient='records')
    elif format == 'excel':
        return df.to_excel('results.xlsx', index=False)
```

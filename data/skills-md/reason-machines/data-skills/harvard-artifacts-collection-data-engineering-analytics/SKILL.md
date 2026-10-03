---
name: harvard-artifacts-collection-data-engineering-analytics
description: End-to-end data engineering and analytics application using Harvard Art Museums API with ETL pipelines, SQL analytics, and Streamlit visualization
triggers:
  - build ETL pipeline for Harvard Art Museums data
  - create analytics dashboard with museum artifacts
  - set up Harvard Art Museums API data collection
  - analyze museum collection data with SQL
  - visualize art museum artifact data
  - implement data engineering pipeline for museum API
  - query Harvard Art Museums collection database
  - build Streamlit app for museum data analytics
---

# Harvard Artifacts Collection Data Engineering Analytics

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project demonstrates a complete data engineering workflow: extracting artifact data from the Harvard Art Museums API, transforming it into structured relational tables, loading it into SQL databases (MySQL/TiDB Cloud), and building interactive analytics dashboards with Streamlit and Plotly.

The application handles:
- API pagination and rate limiting
- ETL pipeline for nested JSON to relational data
- SQL database design with proper relationships
- 20+ analytical SQL queries
- Interactive visualizations

## Installation

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt
```

**Required dependencies:**
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

Create a `.env` file in the project root:

```env
HARVARD_API_KEY=your_api_key_here
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=harvard_artifacts
```

### Database Setup

```python
import mysql.connector
from mysql.connector import Error

def create_database_schema():
    """Initialize the database schema for Harvard artifacts"""
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cursor = connection.cursor()
    
    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
    cursor.execute(f"USE {os.getenv('DB_NAME')}")
    
    # Create artifact metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmetadata (
            objectid INT PRIMARY KEY,
            title VARCHAR(500),
            culture VARCHAR(200),
            century VARCHAR(100),
            classification VARCHAR(200),
            department VARCHAR(200),
            dated VARCHAR(200),
            medium VARCHAR(500),
            technique VARCHAR(500),
            division VARCHAR(200),
            accessionyear INT,
            period VARCHAR(200)
        )
    """)
    
    # Create artifact media table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactmedia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            objectid INT,
            media_count INT,
            has_images BOOLEAN,
            primary_image_url VARCHAR(1000),
            FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
        )
    """)
    
    # Create artifact colors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artifactcolors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            objectid INT,
            color_hex VARCHAR(10),
            color_percent FLOAT,
            FOREIGN KEY (objectid) REFERENCES artifactmetadata(objectid)
        )
    """)
    
    connection.commit()
    cursor.close()
    connection.close()
```

## ETL Pipeline Implementation

### Extract: Fetch Data from API

```python
import requests
import time

def fetch_artifacts_from_api(api_key, num_pages=10, page_size=100):
    """
    Extract artifact data from Harvard Art Museums API
    
    Args:
        api_key: Harvard API key
        num_pages: Number of pages to fetch
        page_size: Records per page (max 100)
    
    Returns:
        List of artifact records
    """
    base_url = "https://api.harvardartmuseums.org/object"
    all_artifacts = []
    
    for page in range(1, num_pages + 1):
        params = {
            'apikey': api_key,
            'size': page_size,
            'page': page
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            all_artifacts.extend(data.get('records', []))
            print(f"Fetched page {page}/{num_pages}")
            time.sleep(0.5)  # Rate limiting
        else:
            print(f"Error on page {page}: {response.status_code}")
            break
    
    return all_artifacts
```

### Transform: Clean and Structure Data

```python
import pandas as pd

def transform_artifacts_to_dataframes(artifacts):
    """
    Transform raw API data into structured DataFrames
    
    Returns:
        tuple: (metadata_df, media_df, colors_df)
    """
    metadata_records = []
    media_records = []
    color_records = []
    
    for artifact in artifacts:
        # Extract metadata
        metadata_records.append({
            'objectid': artifact.get('objectid'),
            'title': artifact.get('title', '')[:500],
            'culture': artifact.get('culture', '')[:200],
            'century': artifact.get('century', '')[:100],
            'classification': artifact.get('classification', '')[:200],
            'department': artifact.get('department', '')[:200],
            'dated': artifact.get('dated', '')[:200],
            'medium': artifact.get('medium', '')[:500],
            'technique': artifact.get('technique', '')[:500],
            'division': artifact.get('division', '')[:200],
            'accessionyear': artifact.get('accessionyear'),
            'period': artifact.get('period', '')[:200]
        })
        
        # Extract media information
        images = artifact.get('images', [])
        primary_image = artifact.get('primaryimageurl', '')
        
        media_records.append({
            'objectid': artifact.get('objectid'),
            'media_count': len(images),
            'has_images': len(images) > 0,
            'primary_image_url': primary_image[:1000] if primary_image else None
        })
        
        # Extract color data
        colors = artifact.get('colors', [])
        for color in colors:
            color_records.append({
                'objectid': artifact.get('objectid'),
                'color_hex': color.get('hex'),
                'color_percent': color.get('percent')
            })
    
    metadata_df = pd.DataFrame(metadata_records)
    media_df = pd.DataFrame(media_records)
    colors_df = pd.DataFrame(color_records)
    
    return metadata_df, media_df, colors_df
```

### Load: Insert Data into Database

```python
def load_data_to_database(metadata_df, media_df, colors_df):
    """
    Load transformed DataFrames into MySQL database
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
    cursor = connection.cursor()
    
    # Insert metadata (batch insert for performance)
    metadata_query = """
        INSERT INTO artifactmetadata 
        (objectid, title, culture, century, classification, department, 
         dated, medium, technique, division, accessionyear, period)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title)
    """
    
    metadata_values = metadata_df.values.tolist()
    cursor.executemany(metadata_query, metadata_values)
    
    # Insert media data
    media_query = """
        INSERT INTO artifactmedia 
        (objectid, media_count, has_images, primary_image_url)
        VALUES (%s, %s, %s, %s)
    """
    
    media_values = media_df.values.tolist()
    cursor.executemany(media_query, media_values)
    
    # Insert color data
    if not colors_df.empty:
        colors_query = """
            INSERT INTO artifactcolors 
            (objectid, color_hex, color_percent)
            VALUES (%s, %s, %s)
        """
        
        colors_values = colors_df.values.tolist()
        cursor.executemany(colors_query, colors_values)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"Loaded {len(metadata_df)} artifacts to database")
```

## Streamlit Analytics Dashboard

### Main Application Structure

```python
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

def main():
    st.set_page_config(
        page_title="Harvard Artifacts Analytics",
        page_icon="🏛️",
        layout="wide"
    )
    
    st.title("🏛️ Harvard Art Museums Collection Analytics")
    st.markdown("---")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Data Collection", "SQL Analytics", "Visualizations"]
    )
    
    if page == "Data Collection":
        show_data_collection_page()
    elif page == "SQL Analytics":
        show_sql_analytics_page()
    elif page == "Visualizations":
        show_visualizations_page()

if __name__ == "__main__":
    main()
```

### Data Collection Page

```python
def show_data_collection_page():
    st.header("📥 Data Collection from API")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_pages = st.number_input("Number of pages", min_value=1, max_value=100, value=10)
    
    with col2:
        page_size = st.number_input("Page size", min_value=1, max_value=100, value=100)
    
    if st.button("Start ETL Pipeline"):
        with st.spinner("Extracting data from API..."):
            api_key = os.getenv('HARVARD_API_KEY')
            artifacts = fetch_artifacts_from_api(api_key, num_pages, page_size)
            st.success(f"✅ Extracted {len(artifacts)} artifacts")
        
        with st.spinner("Transforming data..."):
            metadata_df, media_df, colors_df = transform_artifacts_to_dataframes(artifacts)
            st.success(f"✅ Transformed into {len(metadata_df)} records")
        
        with st.spinner("Loading to database..."):
            load_data_to_database(metadata_df, media_df, colors_df)
            st.success("✅ Data loaded successfully!")
        
        # Show sample data
        st.subheader("Sample Metadata")
        st.dataframe(metadata_df.head())
```

### SQL Analytics Page

```python
def show_sql_analytics_page():
    st.header("📊 SQL Analytics Dashboard")
    
    # Predefined analytical queries
    queries = {
        "Artifacts by Culture": """
            SELECT culture, COUNT(*) as artifact_count
            FROM artifactmetadata
            WHERE culture IS NOT NULL AND culture != ''
            GROUP BY culture
            ORDER BY artifact_count DESC
            LIMIT 15
        """,
        
        "Artifacts by Century": """
            SELECT century, COUNT(*) as artifact_count
            FROM artifactmetadata
            WHERE century IS NOT NULL AND century != ''
            GROUP BY century
            ORDER BY artifact_count DESC
        """,
        
        "Artifacts with Images": """
            SELECT 
                CASE WHEN has_images THEN 'Has Images' ELSE 'No Images' END as image_status,
                COUNT(*) as count
            FROM artifactmedia
            GROUP BY has_images
        """,
        
        "Top Departments": """
            SELECT department, COUNT(*) as artifact_count
            FROM artifactmetadata
            WHERE department IS NOT NULL
            GROUP BY department
            ORDER BY artifact_count DESC
            LIMIT 10
        """,
        
        "Most Common Colors": """
            SELECT color_hex, COUNT(*) as usage_count
            FROM artifactcolors
            WHERE color_hex IS NOT NULL
            GROUP BY color_hex
            ORDER BY usage_count DESC
            LIMIT 20
        """,
        
        "Artifacts by Accession Year": """
            SELECT accessionyear, COUNT(*) as count
            FROM artifactmetadata
            WHERE accessionyear IS NOT NULL
            GROUP BY accessionyear
            ORDER BY accessionyear DESC
            LIMIT 20
        """
    }
    
    selected_query = st.selectbox("Select Analysis", list(queries.keys()))
    
    if st.button("Run Query"):
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        df = pd.read_sql(queries[selected_query], connection)
        connection.close()
        
        # Display results
        st.subheader("Query Results")
        st.dataframe(df)
        
        # Auto-generate visualization
        if len(df.columns) == 2 and len(df) > 0:
            fig = px.bar(
                df,
                x=df.columns[0],
                y=df.columns[1],
                title=selected_query
            )
            st.plotly_chart(fig, use_container_width=True)
```

## Common Analytics Patterns

### Complex Join Query

```python
def get_artifacts_with_complete_metadata():
    """Join all three tables for comprehensive analysis"""
    query = """
        SELECT 
            m.objectid,
            m.title,
            m.culture,
            m.century,
            m.department,
            med.media_count,
            med.has_images,
            COUNT(DISTINCT c.color_hex) as unique_colors
        FROM artifactmetadata m
        LEFT JOIN artifactmedia med ON m.objectid = med.objectid
        LEFT JOIN artifactcolors c ON m.objectid = c.objectid
        GROUP BY m.objectid, m.title, m.culture, m.century, 
                 m.department, med.media_count, med.has_images
        HAVING media_count > 0
        LIMIT 100
    """
    
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    df = pd.read_sql(query, connection)
    connection.close()
    
    return df
```

### Color Analysis Visualization

```python
def visualize_color_distribution():
    """Visualize dominant colors across artifacts"""
    query = """
        SELECT color_hex, SUM(color_percent) as total_percent
        FROM artifactcolors
        GROUP BY color_hex
        ORDER BY total_percent DESC
        LIMIT 15
    """
    
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    df = pd.read_sql(query, connection)
    connection.close()
    
    # Create color-coded bar chart
    fig = px.bar(
        df,
        x='color_hex',
        y='total_percent',
        title='Most Dominant Colors in Collection',
        color='color_hex',
        color_discrete_map={row['color_hex']: row['color_hex'] for _, row in df.iterrows()}
    )
    
    return fig
```

## Running the Application

```bash
# Run the Streamlit app
streamlit run app.py

# The app will be available at http://localhost:8501
```

## Troubleshooting

### API Rate Limiting
```python
# Add retry logic with exponential backoff
import time
from requests.exceptions import HTTPError

def fetch_with_retry(url, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            if response.status_code == 429:  # Too many requests
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Database Connection Issues
```python
# Test database connectivity
def test_database_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            connect_timeout=10
        )
        connection.close()
        return True
    except Error as e:
        print(f"Database connection failed: {e}")
        return False
```

### Memory Issues with Large Datasets
```python
# Process data in chunks
def load_data_in_chunks(df, chunk_size=1000):
    """Load large DataFrames in chunks to avoid memory issues"""
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        cursor = connection.cursor()
        # Insert chunk
        cursor.executemany(query, chunk.values.tolist())
        connection.commit()
        cursor.close()
        print(f"Loaded chunk {i//chunk_size + 1}")
    
    connection.close()
```

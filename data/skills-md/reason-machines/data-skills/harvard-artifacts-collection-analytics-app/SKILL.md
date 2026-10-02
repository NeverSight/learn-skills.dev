---
name: harvard-artifacts-collection-analytics-app
description: Build ETL pipelines and analytics dashboards for the Harvard Art Museums API using Python, SQL, and Streamlit
triggers:
  - how do I build an ETL pipeline for the Harvard Art Museums API
  - create a data engineering project with museum artifact data
  - build a Streamlit dashboard for Harvard Art Museums data
  - set up SQL analytics for artifact collections
  - implement ETL with Harvard Art Museums API
  - create interactive visualizations for museum artifact data
  - build a data pipeline with Harvard API and TiDB
  - analyze Harvard Art Museums data with Python and SQL
---

# Harvard Artifacts Collection Analytics App

> Skill by [ara.so](https://ara.so) — Data Skills collection

## What This Project Does

The Harvard-Artifacts-Collection-Data-Engineering-Analytics-App is an end-to-end data engineering application that demonstrates real-world ETL pipelines, SQL analytics, and interactive visualization. It extracts artifact data from the Harvard Art Museums API, transforms it into relational database structures, and provides interactive analytics dashboards using Streamlit.

**Key capabilities:**
- Extract artifact metadata, media, and color data from Harvard Art Museums API
- Transform nested JSON into normalized relational tables
- Load data into MySQL/TiDB Cloud databases
- Execute analytical SQL queries
- Visualize results with interactive Plotly charts
- Handle API pagination and rate limiting

## Installation

### Prerequisites

```bash
# Python 3.7+
python --version

# Install required packages
pip install streamlit pandas requests mysql-connector-python plotly python-dotenv
```

### Project Setup

```bash
# Clone the repository
git clone https://github.com/Manali0711/Harvard-Artifacts-Collection-Data-Engineering-Analytics-App.git
cd Harvard-Artifacts-Collection-Data-Engineering-Analytics-App

# Install dependencies
pip install -r requirements.txt

# Create .env file for configuration
touch .env
```

### Environment Configuration

Create a `.env` file with the following variables:

```bash
# Harvard Art Museums API
HARVARD_API_KEY=your_api_key_here

# Database Configuration (MySQL/TiDB Cloud)
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=harvard_artifacts
```

To get a Harvard Art Museums API key:
1. Visit https://www.harvardartmuseums.org/collections/api
2. Request an API key (free)
3. Add it to your `.env` file

## Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# The app will open in your browser at http://localhost:8501
```

## Database Schema

The application creates three main tables:

```sql
-- Artifact metadata table
CREATE TABLE artifactmetadata (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    culture VARCHAR(255),
    century VARCHAR(255),
    dated VARCHAR(255),
    classification VARCHAR(255),
    department VARCHAR(255),
    technique VARCHAR(500),
    medium VARCHAR(500),
    dimensions VARCHAR(500),
    creditline TEXT,
    accession_number VARCHAR(255),
    url TEXT
);

-- Artifact media table
CREATE TABLE artifactmedia (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    image_url TEXT,
    media_type VARCHAR(100),
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);

-- Artifact colors table
CREATE TABLE artifactcolors (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id INT,
    color VARCHAR(50),
    percentage FLOAT,
    FOREIGN KEY (artifact_id) REFERENCES artifactmetadata(id)
);
```

## Code Examples

### 1. API Data Extraction

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_artifacts(api_key, page=1, size=100):
    """
    Fetch artifacts from Harvard Art Museums API
    
    Args:
        api_key: Harvard API key
        page: Page number for pagination
        size: Number of records per page (max 100)
    
    Returns:
        JSON response with artifact data
    """
    base_url = "https://api.harvardartmuseums.org/object"
    params = {
        'apikey': api_key,
        'page': page,
        'size': size,
        'hasimage': 1  # Only artifacts with images
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json()

# Usage
api_key = os.getenv('HARVARD_API_KEY')
data = fetch_artifacts(api_key, page=1, size=50)
print(f"Total records: {data['info']['totalrecords']}")
print(f"Fetched: {len(data['records'])} artifacts")
```

### 2. ETL Pipeline - Transform

```python
import pandas as pd

def transform_artifacts(raw_data):
    """
    Transform raw API data into structured DataFrames
    
    Args:
        raw_data: JSON response from API
    
    Returns:
        Dictionary of DataFrames (metadata, media, colors)
    """
    artifacts = []
    media_list = []
    colors_list = []
    
    for record in raw_data['records']:
        # Extract metadata
        artifact = {
            'id': record.get('id'),
            'title': record.get('title', 'Unknown'),
            'culture': record.get('culture'),
            'century': record.get('century'),
            'dated': record.get('dated'),
            'classification': record.get('classification'),
            'department': record.get('department'),
            'technique': record.get('technique'),
            'medium': record.get('medium'),
            'dimensions': record.get('dimensions'),
            'creditline': record.get('creditline'),
            'accession_number': record.get('accessionnumber'),
            'url': record.get('url')
        }
        artifacts.append(artifact)
        
        # Extract media
        if 'images' in record and record['images']:
            for img in record['images']:
                media_list.append({
                    'artifact_id': record['id'],
                    'image_url': img.get('baseimageurl'),
                    'media_type': 'image'
                })
        
        # Extract colors
        if 'colors' in record and record['colors']:
            for color in record['colors']:
                colors_list.append({
                    'artifact_id': record['id'],
                    'color': color.get('color'),
                    'percentage': color.get('percent')
                })
    
    return {
        'metadata': pd.DataFrame(artifacts),
        'media': pd.DataFrame(media_list),
        'colors': pd.DataFrame(colors_list)
    }
```

### 3. Database Loading

```python
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 3306),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def load_artifacts_to_db(dataframes):
    """
    Load transformed data into SQL database
    
    Args:
        dataframes: Dictionary of DataFrames from transform_artifacts()
    """
    connection = get_db_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Insert metadata
        for _, row in dataframes['metadata'].iterrows():
            query = """
            INSERT INTO artifactmetadata 
            (id, title, culture, century, dated, classification, 
             department, technique, medium, dimensions, creditline, 
             accession_number, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title)
            """
            cursor.execute(query, tuple(row))
        
        # Insert media
        for _, row in dataframes['media'].iterrows():
            query = """
            INSERT INTO artifactmedia (artifact_id, image_url, media_type)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, tuple(row))
        
        # Insert colors
        for _, row in dataframes['colors'].iterrows():
            query = """
            INSERT INTO artifactcolors (artifact_id, color, percentage)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, tuple(row))
        
        connection.commit()
        print("Data loaded successfully!")
        
    except Error as e:
        print(f"Error loading data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
```

### 4. Streamlit Dashboard

```python
import streamlit as st
import plotly.express as px

def main():
    st.title("Harvard Art Museums Analytics Dashboard")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("API Key", type="password", 
                                     value=os.getenv('HARVARD_API_KEY', ''))
    
    num_records = st.sidebar.slider("Records to fetch", 10, 500, 100)
    
    # ETL Pipeline Section
    st.header("🔄 ETL Pipeline")
    
    if st.button("Run ETL Pipeline"):
        with st.spinner("Fetching data from API..."):
            raw_data = fetch_artifacts(api_key, page=1, size=num_records)
            st.success(f"Fetched {len(raw_data['records'])} artifacts")
        
        with st.spinner("Transforming data..."):
            transformed = transform_artifacts(raw_data)
            st.success("Data transformed successfully")
        
        with st.spinner("Loading to database..."):
            load_artifacts_to_db(transformed)
            st.success("Data loaded to database")
    
    # Analytics Section
    st.header("📊 Analytics")
    
    query_options = {
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
        "Top Colors Used": """
            SELECT color, SUM(percentage) as total_percentage 
            FROM artifactcolors 
            GROUP BY color 
            ORDER BY total_percentage DESC 
            LIMIT 10
        """
    }
    
    selected_query = st.selectbox("Select Analysis", list(query_options.keys()))
    
    if st.button("Run Query"):
        connection = get_db_connection()
        if connection:
            df = pd.read_sql(query_options[selected_query], connection)
            
            st.dataframe(df)
            
            # Visualization
            if len(df) > 0:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                            title=selected_query)
                st.plotly_chart(fig)
            
            connection.close()

if __name__ == "__main__":
    main()
```

## Common Analytical Queries

```sql
-- 1. Distribution of artifacts by department
SELECT department, COUNT(*) as artifact_count
FROM artifactmetadata
GROUP BY department
ORDER BY artifact_count DESC;

-- 2. Artifacts with media vs without
SELECT 
    CASE WHEN m.artifact_id IS NOT NULL THEN 'Has Media' ELSE 'No Media' END as media_status,
    COUNT(*) as count
FROM artifactmetadata a
LEFT JOIN artifactmedia m ON a.id = m.artifact_id
GROUP BY media_status;

-- 3. Most common artifact classifications
SELECT classification, COUNT(*) as count
FROM artifactmetadata
WHERE classification IS NOT NULL
GROUP BY classification
ORDER BY count DESC
LIMIT 15;

-- 4. Color distribution across all artifacts
SELECT color, ROUND(AVG(percentage), 2) as avg_percentage, COUNT(*) as occurrences
FROM artifactcolors
GROUP BY color
ORDER BY occurrences DESC
LIMIT 20;

-- 5. Artifacts by culture and century
SELECT culture, century, COUNT(*) as count
FROM artifactmetadata
WHERE culture IS NOT NULL AND century IS NOT NULL
GROUP BY culture, century
ORDER BY count DESC
LIMIT 20;
```

## Troubleshooting

### API Rate Limiting

```python
import time

def fetch_with_rate_limit(api_key, total_records=500, batch_size=100):
    """Fetch data with rate limiting"""
    all_data = []
    pages = (total_records // batch_size) + 1
    
    for page in range(1, pages + 1):
        data = fetch_artifacts(api_key, page=page, size=batch_size)
        all_data.extend(data['records'])
        
        # Rate limit: 1 request per second
        time.sleep(1)
    
    return all_data
```

### Database Connection Issues

```python
def verify_db_connection():
    """Test database connectivity"""
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            print("✓ Database connection successful")
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"✓ Connected to database: {db_name}")
            cursor.close()
            conn.close()
            return True
    except Error as e:
        print(f"✗ Connection failed: {e}")
        return False
```

### Handling Missing Data

```python
def safe_extract(record, key, default='Unknown'):
    """Safely extract nested data from API response"""
    try:
        value = record.get(key, default)
        return value if value else default
    except:
        return default

# Usage in transform function
artifact = {
    'title': safe_extract(record, 'title', 'Untitled'),
    'culture': safe_extract(record, 'culture', None),
    'century': safe_extract(record, 'century', None)
}
```

## Best Practices

1. **Batch Processing**: Process API data in batches to avoid memory issues
2. **Error Handling**: Wrap API calls and DB operations in try-except blocks
3. **Environment Variables**: Never hardcode credentials
4. **Data Validation**: Validate data before inserting into database
5. **Logging**: Add logging for ETL pipeline monitoring
6. **Incremental Loading**: Track processed artifacts to avoid duplicates

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def etl_pipeline(api_key, num_records=100):
    """Complete ETL pipeline with logging"""
    try:
        logger.info(f"Starting ETL for {num_records} records")
        
        raw_data = fetch_artifacts(api_key, size=num_records)
        logger.info(f"Extracted {len(raw_data['records'])} records")
        
        transformed = transform_artifacts(raw_data)
        logger.info(f"Transformed into {len(transformed['metadata'])} artifacts")
        
        load_artifacts_to_db(transformed)
        logger.info("Data loaded successfully")
        
        return True
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        return False
```

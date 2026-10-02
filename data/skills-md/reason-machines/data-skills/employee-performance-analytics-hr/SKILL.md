---
name: employee-performance-analytics-hr
description: SQL and Python-based employee performance analytics with KPI aggregation, departmental insights, and HR dashboard generation
triggers:
  - analyze employee performance metrics
  - create hr analytics dashboard
  - calculate departmental kpis
  - visualize productivity trends
  - generate employee performance reports
  - build hr data pipeline
  - assess workforce efficiency metrics
  - aggregate employee performance data
---

# Employee Performance Analytics HR Skill

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

Employee Performance Analytics is a Python and SQL-based HR analytics tool that transforms employee data into actionable insights. It uses SQLite for KPI aggregation and pandas/matplotlib for visualization, generating departmental performance reports, efficiency metrics, and workload analysis.

The project provides an end-to-end analytics pipeline: data loading → SQL feature engineering → Python analysis → visualization exports.

## Installation

```bash
# Clone the repository
git clone https://github.com/AmirhosseinHonardoust/Employee-Performance-Analytics.git
cd Employee-Performance-Analytics

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```txt
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
sqlite3  # Built-in with Python
numpy>=1.24.0
```

## Project Structure

```
employee-performance-analytics/
├── data/
│   └── employees.csv          # Raw employee data
├── src/
│   ├── create_db.py          # CSV to SQLite loader
│   ├── queries.sql           # SQL KPI queries
│   ├── analyze_performance.py # Main analysis script
│   └── utils.py              # Helper functions
└── outputs/
    ├── department_kpis.csv
    ├── performance_summary.csv
    └── charts/               # Generated visualizations
```

## Data Schema

The project expects employee data with these columns:

| Column | Type | Description |
|--------|------|-------------|
| `employee_id` | int | Unique identifier |
| `name` | string | Employee name |
| `department` | string | Department (Engineering, Sales, etc.) |
| `role` | string | Job title |
| `date` | date | Record date (YYYY-MM-DD) |
| `tasks_completed` | int | Daily tasks completed |
| `hours_worked` | float | Hours worked |
| `rating` | float | Performance rating (1-5) |
| `projects` | int | Active projects |
| `absences` | int | 1 if absent, 0 otherwise |

## Key Commands

### 1. Load Data into SQLite

```bash
python src/create_db.py --csv data/employees.csv --db hr.db
```

**Options:**
- `--csv`: Path to input CSV file
- `--db`: Output SQLite database path
- `--table`: Table name (default: `employees`)

### 2. Run Performance Analysis

```bash
python src/analyze_performance.py --db hr.db --sql src/queries.sql --outdir outputs
```

**Options:**
- `--db`: Path to SQLite database
- `--sql`: Path to SQL queries file
- `--outdir`: Output directory for CSV reports and charts

## Core SQL Queries

The `queries.sql` file contains three main analytical views:

### Department KPIs

```sql
-- Department-level performance metrics
CREATE VIEW IF NOT EXISTS department_kpis AS
SELECT
    department,
    COUNT(DISTINCT employee_id) AS employee_count,
    AVG(rating) AS avg_rating,
    SUM(tasks_completed) AS total_tasks,
    SUM(hours_worked) AS total_hours,
    ROUND(AVG(CAST(absences AS FLOAT)), 2) AS absence_rate,
    ROUND(SUM(tasks_completed) * 1.0 / SUM(hours_worked), 2) AS tasks_per_hour
FROM employees
GROUP BY department
ORDER BY avg_rating DESC;
```

### Employee Summary

```sql
-- Individual employee performance aggregation
CREATE VIEW IF NOT EXISTS employee_summary AS
SELECT
    employee_id,
    name,
    department,
    role,
    SUM(tasks_completed) AS total_tasks,
    SUM(hours_worked) AS total_hours,
    AVG(rating) AS avg_rating,
    COUNT(DISTINCT projects) AS project_count,
    SUM(absences) AS total_absences,
    ROUND(SUM(tasks_completed) * 1.0 / SUM(hours_worked), 2) AS efficiency
FROM employees
GROUP BY employee_id, name, department, role
ORDER BY efficiency DESC;
```

### Daily Productivity

```sql
-- Day-by-day productivity tracking
CREATE VIEW IF NOT EXISTS daily_productivity AS
SELECT
    date,
    department,
    SUM(tasks_completed) AS daily_tasks,
    SUM(hours_worked) AS daily_hours,
    AVG(rating) AS daily_rating
FROM employees
GROUP BY date, department
ORDER BY date, department;
```

## Python API Usage

### Creating Database from CSV

```python
import pandas as pd
import sqlite3

def create_database(csv_path, db_path, table_name='employees'):
    """Load CSV into SQLite database."""
    df = pd.read_csv(csv_path)
    
    # Data validation
    required_cols = ['employee_id', 'name', 'department', 'date', 
                     'tasks_completed', 'hours_worked', 'rating']
    assert all(col in df.columns for col in required_cols), "Missing required columns"
    
    # Create database
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"✓ Database created: {db_path}")

# Usage
create_database('data/employees.csv', 'hr.db')
```

### Running SQL Queries

```python
import sqlite3
import pandas as pd

def execute_sql_file(db_path, sql_file_path):
    """Execute SQL script and return results."""
    conn = sqlite3.connect(db_path)
    
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()
    
    # Execute all statements
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    
    # Fetch view results
    dept_kpis = pd.read_sql_query("SELECT * FROM department_kpis", conn)
    emp_summary = pd.read_sql_query("SELECT * FROM employee_summary", conn)
    daily_prod = pd.read_sql_query("SELECT * FROM daily_productivity", conn)
    
    conn.close()
    
    return dept_kpis, emp_summary, daily_prod
```

### Generating Visualizations

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_department_ratings(dept_kpis, output_path):
    """Bar chart of average rating by department."""
    plt.figure(figsize=(12, 7))
    
    sns.barplot(
        data=dept_kpis,
        x='department',
        y='avg_rating',
        palette='viridis'
    )
    
    plt.title('Average Performance Rating by Department', fontsize=16, weight='bold')
    plt.xlabel('Department', fontsize=12)
    plt.ylabel('Average Rating', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 5)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_performance_vs_hours(emp_summary, output_path):
    """Scatter plot of tasks vs hours worked."""
    plt.figure(figsize=(12, 7))
    
    scatter = plt.scatter(
        emp_summary['total_hours'],
        emp_summary['total_tasks'],
        c=emp_summary['avg_rating'],
        cmap='RdYlGn',
        s=100,
        alpha=0.6,
        edgecolors='black'
    )
    
    plt.colorbar(scatter, label='Avg Rating')
    plt.title('Tasks Completed vs Hours Worked', fontsize=16, weight='bold')
    plt.xlabel('Total Hours Worked', fontsize=12)
    plt.ylabel('Total Tasks Completed', fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_efficiency_distribution(emp_summary, output_path):
    """Histogram of task completion rate."""
    plt.figure(figsize=(12, 7))
    
    plt.hist(
        emp_summary['efficiency'].dropna(),
        bins=30,
        color='steelblue',
        edgecolor='black',
        alpha=0.7
    )
    
    plt.axvline(
        emp_summary['efficiency'].median(),
        color='red',
        linestyle='--',
        linewidth=2,
        label=f"Median: {emp_summary['efficiency'].median():.2f}"
    )
    
    plt.title('Task Completion Rate Distribution', fontsize=16, weight='bold')
    plt.xlabel('Tasks per Hour', fontsize=12)
    plt.ylabel('Number of Employees', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

## Complete Analysis Pipeline

```python
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class HRAnalyzer:
    """Complete HR analytics pipeline."""
    
    def __init__(self, db_path, sql_path, output_dir):
        self.db_path = db_path
        self.sql_path = sql_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'charts').mkdir(exist_ok=True)
        
    def load_data(self):
        """Execute SQL and load analytical views."""
        conn = sqlite3.connect(self.db_path)
        
        # Execute SQL script
        with open(self.sql_path, 'r') as f:
            conn.executescript(f.read())
        
        # Load views
        self.dept_kpis = pd.read_sql_query("SELECT * FROM department_kpis", conn)
        self.emp_summary = pd.read_sql_query("SELECT * FROM employee_summary", conn)
        self.daily_prod = pd.read_sql_query("SELECT * FROM daily_productivity", conn)
        
        conn.close()
        print("✓ Data loaded from SQL views")
        
    def export_reports(self):
        """Save CSV reports."""
        self.dept_kpis.to_csv(
            self.output_dir / 'department_kpis.csv',
            index=False
        )
        self.emp_summary.to_csv(
            self.output_dir / 'performance_summary.csv',
            index=False
        )
        print(f"✓ Reports saved to {self.output_dir}")
        
    def generate_visualizations(self):
        """Create all performance charts."""
        charts_dir = self.output_dir / 'charts'
        
        # Department ratings
        plt.figure(figsize=(12, 7))
        sns.barplot(data=self.dept_kpis, x='department', y='avg_rating', palette='viridis')
        plt.title('Average Rating by Department', fontsize=16, weight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(charts_dir / 'avg_rating_by_department.png', dpi=300)
        plt.close()
        
        # Performance vs hours
        plt.figure(figsize=(12, 7))
        plt.scatter(
            self.emp_summary['total_hours'],
            self.emp_summary['total_tasks'],
            c=self.emp_summary['avg_rating'],
            cmap='RdYlGn',
            s=100,
            alpha=0.6
        )
        plt.colorbar(label='Avg Rating')
        plt.title('Performance vs Hours Worked', fontsize=16, weight='bold')
        plt.xlabel('Total Hours')
        plt.ylabel('Total Tasks')
        plt.tight_layout()
        plt.savefig(charts_dir / 'performance_vs_hours.png', dpi=300)
        plt.close()
        
        # Efficiency distribution
        plt.figure(figsize=(12, 7))
        plt.hist(self.emp_summary['efficiency'].dropna(), bins=30, color='steelblue', edgecolor='black')
        plt.axvline(self.emp_summary['efficiency'].median(), color='red', linestyle='--', linewidth=2)
        plt.title('Task Completion Rate Distribution', fontsize=16, weight='bold')
        plt.xlabel('Tasks per Hour')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(charts_dir / 'task_completion_rate.png', dpi=300)
        plt.close()
        
        print(f"✓ Visualizations saved to {charts_dir}")
        
    def run_full_analysis(self):
        """Execute complete analytics pipeline."""
        self.load_data()
        self.export_reports()
        self.generate_visualizations()
        print("✓ Analysis complete!")

# Usage
analyzer = HRAnalyzer(
    db_path='hr.db',
    sql_path='src/queries.sql',
    output_dir='outputs'
)
analyzer.run_full_analysis()
```

## Common Patterns

### Custom KPI Queries

```python
def get_top_performers(db_path, n=10):
    """Retrieve top N employees by efficiency."""
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        name, 
        department, 
        efficiency, 
        avg_rating
    FROM employee_summary
    ORDER BY efficiency DESC
    LIMIT ?
    """
    top_performers = pd.read_sql_query(query, conn, params=(n,))
    conn.close()
    return top_performers

def get_department_trends(db_path, department):
    """Get time-series data for specific department."""
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        date, 
        daily_tasks, 
        daily_hours, 
        daily_rating
    FROM daily_productivity
    WHERE department = ?
    ORDER BY date
    """
    trends = pd.read_sql_query(query, conn, params=(department,))
    conn.close()
    return trends
```

### Filtering and Aggregation

```python
def analyze_by_role(db_path, role_filter):
    """Aggregate performance by specific role."""
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        role,
        AVG(rating) as avg_rating,
        AVG(tasks_completed) as avg_tasks,
        AVG(hours_worked) as avg_hours
    FROM employees
    WHERE role LIKE ?
    GROUP BY role
    """
    role_stats = pd.read_sql_query(query, conn, params=(f'%{role_filter}%',))
    conn.close()
    return role_stats
```

### Adding New Metrics

```python
def calculate_workload_balance(emp_summary):
    """Calculate workload balance score."""
    emp_summary['workload_score'] = (
        emp_summary['total_tasks'] / emp_summary['total_tasks'].max() * 0.4 +
        emp_summary['total_hours'] / emp_summary['total_hours'].max() * 0.3 +
        emp_summary['avg_rating'] / 5 * 0.3
    )
    return emp_summary
```

## Configuration

### Custom Chart Styling

```python
# Set global matplotlib style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Custom colors
DEPT_COLORS = {
    'Engineering': '#3498db',
    'Sales': '#e74c3c',
    'Finance': '#2ecc71',
    'HR': '#f39c12',
    'Support': '#9b59b6'
}
```

### Database Configuration

```python
# For larger datasets, enable performance optimizations
def optimize_database(db_path):
    """Apply SQLite performance settings."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA journal_mode = WAL")
    cursor.execute("PRAGMA synchronous = NORMAL")
    cursor.execute("PRAGMA cache_size = 10000")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dept ON employees(department)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON employees(date)")
    
    conn.commit()
    conn.close()
```

## Troubleshooting

### Missing Columns Error

```python
# Validate CSV before loading
required_columns = [
    'employee_id', 'name', 'department', 'role', 
    'date', 'tasks_completed', 'hours_worked', 
    'rating', 'projects', 'absences'
]

df = pd.read_csv('data/employees.csv')
missing = set(required_columns) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")
```

### SQL View Not Found

```python
# Check if views exist
def verify_views(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
    views = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    expected = ['department_kpis', 'employee_summary', 'daily_productivity']
    missing = set(expected) - set(views)
    if missing:
        print(f"⚠ Missing views: {missing}. Re-run queries.sql")
    else:
        print("✓ All views exist")
```

### Division by Zero in Efficiency

```python
# Safe efficiency calculation
emp_summary['efficiency'] = emp_summary.apply(
    lambda row: row['total_tasks'] / row['total_hours'] 
    if row['total_hours'] > 0 else None,
    axis=1
)
```

### Date Parsing Issues

```python
# Ensure proper date format
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
df = df.dropna(subset=['date'])
```

## Advanced Use Cases

### Time Series Analysis

```python
def plot_monthly_trends(db_path, department):
    """Monthly productivity trends for a department."""
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        strftime('%Y-%m', date) as month,
        AVG(rating) as avg_rating,
        SUM(tasks_completed) as total_tasks
    FROM employees
    WHERE department = ?
    GROUP BY month
    ORDER BY month
    """
    df = pd.read_sql_query(query, conn, params=(department,))
    conn.close()
    
    fig, ax1 = plt.subplots(figsize=(14, 7))
    ax2 = ax1.twinx()
    
    ax1.plot(df['month'], df['avg_rating'], 'b-', linewidth=2, label='Avg Rating')
    ax2.bar(df['month'], df['total_tasks'], alpha=0.3, color='gray', label='Total Tasks')
    
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Average Rating', color='b')
    ax2.set_ylabel('Total Tasks', color='gray')
    plt.title(f'{department} Performance Trends')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

### Comparative Analysis

```python
def compare_departments(dept_kpis):
    """Generate department comparison report."""
    comparison = dept_kpis[['department', 'avg_rating', 'tasks_per_hour', 'absence_rate']]
    
    # Normalize metrics
    for col in ['avg_rating', 'tasks_per_hour']:
        comparison[f'{col}_norm'] = (
            (comparison[col] - comparison[col].min()) / 
            (comparison[col].max() - comparison[col].min())
        )
    
    comparison['performance_index'] = (
        comparison['avg_rating_norm'] * 0.5 + 
        comparison['tasks_per_hour_norm'] * 0.5
    )
    
    return comparison.sort_values('performance_index', ascending=False)
```

This skill provides comprehensive guidance for using the Employee Performance Analytics project to build HR dashboards, analyze workforce metrics, and generate actionable insights from employee data.

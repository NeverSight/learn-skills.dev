---
name: llm-intelligent-public-opinion-analytics
description: Deploy and use an LLM-powered public opinion analytics assistant that crawls 26 hot lists from 15 platforms, performs sentiment analysis, topic clustering, and multi-channel alerting
triggers:
  - set up public opinion monitoring system
  - analyze social media trending topics
  - deploy sentiment analysis crawler
  - configure hot topic push notifications
  - cluster trending news topics
  - monitor multiple platform hot searches
  - build opinion analytics dashboard
  - aggregate cross-platform trending content
---

# LLM-Based Intelligent Public Opinion Analytics Assistant

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project is a comprehensive public opinion analytics platform that combines real-time data from **26 hot lists across 15 mainstream platforms** (Weibo, Bilibili, Zhihu, Baidu, etc.) with large language model (LLM) analysis capabilities. It provides conversational query interfaces for hot searches, topic clustering, sentiment analysis, and multi-channel push notifications (WeChat, Email, Telegram).

**Key Capabilities:**
- Real-time crawler cluster for 15+ platforms
- LLM-powered content analysis (including video content extraction)
- Natural language query interface
- Topic clustering and sentiment analysis
- Multi-channel alert system (Email, WeChat Work, Telegram)
- Keyboard shortcuts for crawler control

## Installation

### Prerequisites

1. **Browser Driver Setup** (Required for detail page scraping):

```bash
# Check your Chrome/Edge version first
# Chrome: chrome://settings/help
# Edge: edge://settings/help

# Download matching driver:
# ChromeDriver: https://chromedriver.chromium.org/
# EdgeDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

# Linux/macOS - place driver in PATH:
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Verify installation:
chromedriver --version
```

2. **MySQL Database**:

```bash
# Install MySQL 8.0+
# Create database and user
mysql -u root -p

CREATE DATABASE hotsearch_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hotsearch_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON hotsearch_db.* TO 'hotsearch_user'@'localhost';
FLUSH PRIVILEGES;
```

3. **Python Environment**:

```bash
# Clone repository
git clone https://github.com/hmmnxkl/LLM-Based-Intelligent-Public-Opinion-Analytics-Assistant.git
cd LLM-Based-Intelligent-Public-Opinion-Analytics-Assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Initialization

Reference the `init.py` file to create necessary tables:

```python
# Example table structure (adapt from init.py)
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='hotsearch_user',
    password='your_password',
    database='hotsearch_db',
    charset='utf8mb4'
)

cursor = connection.cursor()

# Hot search items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS hot_search_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    rank INT,
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000),
    heat_value VARCHAR(100),
    crawl_time DATETIME NOT NULL,
    detail_content TEXT,
    sentiment VARCHAR(20),
    INDEX idx_platform (platform),
    INDEX idx_crawl_time (crawl_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")

connection.commit()
connection.close()
```

## Configuration

### Environment Variables

Create `.env` file in the project root:

```bash
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=hotsearch_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=hotsearch_db

# LLM API Configuration (OpenAI-compatible format)
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://your-llm-endpoint.com/v1
OPENAI_MODEL=gpt-4

# Huawei Pangu Model (recommended alternative)
PANGU_API_KEY=your_pangu_key
PANGU_API_BASE=https://pangu-api.huaweicloud.com

# Push Notification Channels
# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# WeChat Work Bot
WECHAT_WORK_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY

# WeChat Work Application
WECHAT_WORK_CORP_ID=your_corp_id
WECHAT_WORK_APP_SECRET=your_app_secret
WECHAT_WORK_AGENT_ID=your_agent_id

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Crawler Settings

Edit `hotsearchcrawler/settings.py`:

```python
# MySQL Connection Pool
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'charset': 'utf8mb4',
    'autocommit': True
}

# Optional: Platform-specific cookies for authenticated access
PLATFORM_COOKIES = {
    'weibo': 'your_weibo_cookies',  # Optional, for better access
    'bilibili': 'your_bilibili_cookies'
}

# Concurrent requests
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1

# User-Agent rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
]
```

## Usage

### Starting the System

```bash
# Activate virtual environment
source venv/bin/activate

# Start the main application (web interface + API)
python app.py

# Access web interface at http://localhost:5000
```

### Crawler Management

```python
# Manual crawler test (single platform)
cd hotsearchcrawler
python runspider-test.py

# Start all crawlers (typically triggered via web UI)
python run_spiders.py
```

**Via Web Interface:**
- Use keyboard shortcuts to start/stop crawlers
- View real-time crawling status
- Monitor data collection metrics

### Natural Language Queries

```python
# Examples of conversational queries via web interface:

# "Show me today's top 10 trending topics on Weibo"
# "What's trending about AI technology across all platforms?"
# "Analyze sentiment for news about electric vehicles"
# "Cluster topics related to economic policy"
# "Compare hot topics between Bilibili and Zhihu"
```

### Programmatic API Usage

```python
from hotsearch_analysis_agent.analyzer import OpinionAnalyzer
from datetime import datetime, timedelta

# Initialize analyzer
analyzer = OpinionAnalyzer()

# Query hot searches
results = analyzer.query_hot_searches(
    platforms=['weibo', 'zhihu', 'bilibili'],
    time_range=(datetime.now() - timedelta(hours=24), datetime.now()),
    keyword='人工智能'
)

# Perform sentiment analysis
sentiment = analyzer.analyze_sentiment(results)
print(f"Overall sentiment: {sentiment['overall']}")
print(f"Positive: {sentiment['positive_ratio']}%")

# Topic clustering
clusters = analyzer.cluster_topics(results, num_clusters=5)
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}: {cluster['keywords']}")
    print(f"  Items: {len(cluster['items'])}")
```

### Push Notification Setup

```python
from hotsearch_analysis_agent.push_service import PushService

# Initialize push service
push_service = PushService()

# Create scheduled push task
task = push_service.create_task(
    name="AI Technology Daily Report",
    keywords=['人工智能', '大模型', '机器学习'],
    platforms=['weibo', 'zhihu', 'bilibili'],
    schedule='0 8,12,18 * * *',  # Cron format: 8am, 12pm, 6pm daily
    channels=['wechat_work', 'email'],
    threshold={'heat_value': 100000, 'sentiment': 'positive'}
)

# Test push task
python test_push_task.py
```

### Analysis Report Generation

```python
from hotsearch_analysis_agent.report_generator import ReportGenerator

generator = ReportGenerator()

# Generate comprehensive report
report = generator.generate_report(
    topic="人工智能与前沿科技",
    time_range=(datetime.now() - timedelta(days=7), datetime.now()),
    include_sentiment=True,
    include_clustering=True,
    include_trend_analysis=True
)

# Report includes:
# - Core findings with data highlights
# - Detailed news content with source URLs
# - Sentiment distribution
# - Topic clusters
# - Trend analysis
# - Information spread characteristics

# Save report
report.save_markdown('output/ai_tech_report.md')
report.save_pdf('output/ai_tech_report.pdf')
```

## Common Patterns

### Multi-Platform Data Aggregation

```python
from hotsearch_analysis_agent.aggregator import DataAggregator

aggregator = DataAggregator()

# Fetch and merge data from multiple platforms
merged_data = aggregator.aggregate(
    platforms=['weibo', 'douyin', 'zhihu', 'bilibili', 'baidu'],
    dedup_threshold=0.8,  # Similarity threshold for deduplication
    sort_by='heat_value',
    limit=50
)

# Cross-platform topic correlation
correlations = aggregator.find_correlations(merged_data)
print(f"Found {len(correlations)} cross-platform trending topics")
```

### Video Content Analysis

```python
# The system automatically extracts text from video news
# using browser automation and LLM analysis

from hotsearch_analysis_agent.video_analyzer import VideoAnalyzer

video_analyzer = VideoAnalyzer()

# Analyze video-based hot topics (e.g., from Bilibili, Douyin)
video_topics = video_analyzer.extract_content(
    url='https://www.bilibili.com/video/BV13pSoBBEvX/',
    extract_comments=True,
    max_comments=100
)

print(f"Video title: {video_topics['title']}")
print(f"Description: {video_topics['description']}")
print(f"Top comments sentiment: {video_topics['comments_sentiment']}")
```

### Custom LLM Integration

```python
from hotsearch_analysis_agent.llm_client import LLMClient

# Use Huawei Pangu Model (recommended)
llm = LLMClient(
    api_base=os.getenv('PANGU_API_BASE'),
    api_key=os.getenv('PANGU_API_KEY'),
    model='pangu-embedded-7b'
)

# Or use any OpenAI-compatible endpoint
llm = LLMClient(
    api_base=os.getenv('OPENAI_API_BASE'),
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-4'
)

# Analyze custom content
analysis = llm.analyze(
    content=news_content,
    task='sentiment_and_summary',
    language='zh'
)
```

### Scheduled Monitoring

```python
from hotsearch_analysis_agent.scheduler import MonitorScheduler

scheduler = MonitorScheduler()

# Add monitoring rule
scheduler.add_rule(
    name="Tech Company Crisis Monitoring",
    keywords=['某公司', '丑闻', '争议'],
    alert_conditions={
        'heat_spike': 2.0,  # 2x normal heat
        'sentiment_drop': -0.3,  # 30% sentiment decrease
        'platforms_count': 3  # Trending on 3+ platforms
    },
    notification_channels=['wechat_work', 'telegram', 'email'],
    urgent=True
)

# Start scheduler
scheduler.start()
```

## Troubleshooting

### Browser Driver Issues

```bash
# Error: "Message: 'chromedriver' executable needs to be in PATH"
# Solution: Verify driver installation
which chromedriver  # Should return path

# If not found, reinstall:
# 1. Check browser version
google-chrome --version  # or microsoft-edge --version

# 2. Download exact matching driver version
# 3. Place in /usr/local/bin/ and chmod +x

# Alternative: Specify driver path in settings
CHROMEDRIVER_PATH=/path/to/chromedriver
```

### Database Connection Errors

```python
# Error: "Can't connect to MySQL server"
# Check MySQL service
sudo systemctl status mysql

# Verify credentials
mysql -u hotsearch_user -p -h localhost hotsearch_db

# Check .env file encoding (must be UTF-8 without BOM)
file -I .env  # Should show charset=utf-8

# Test connection in Python
import pymysql
try:
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")
```

### Crawler Rate Limiting

```python
# Error: HTTP 429 or blocked requests
# Solution: Adjust crawler settings

# In hotsearchcrawler/settings.py:
CONCURRENT_REQUESTS = 8  # Reduce from 16
DOWNLOAD_DELAY = 2  # Increase delay

# Enable AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10

# Rotate User-Agents and proxies
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}
```

### LLM API Timeouts

```python
# Error: Request timeout or rate limit
# Solution: Implement retry logic and fallback

from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_llm_with_retry(prompt):
    return llm.analyze(prompt)

# Use batch processing for large datasets
from hotsearch_analysis_agent.batch_processor import BatchProcessor

processor = BatchProcessor(batch_size=10, delay=2)
results = processor.process_items(news_items, analyze_func)
```

### Memory Issues with Large Datasets

```python
# Error: MemoryError or slow processing
# Solution: Use pagination and streaming

from hotsearch_analysis_agent.db_client import DBClient

db = DBClient()

# Stream results instead of loading all at once
for batch in db.stream_hot_searches(batch_size=100):
    process_batch(batch)
    # Process and discard to free memory

# Use database aggregation instead of in-memory
aggregated = db.aggregate_by_platform(
    start_date='2026-01-01',
    end_date='2026-05-01'
)
```

## Project Structure Reference

```
.
├── app.py                          # Main application entry
├── hotsearch_analysis_agent/       # Analysis system
│   ├── analyzer.py                 # Core analysis logic
│   ├── llm_client.py              # LLM integration
│   ├── report_generator.py        # Report generation
│   ├── push_service.py            # Notification service
│   └── scheduler.py               # Task scheduling
├── hotsearchcrawler/              # Crawler cluster
│   ├── spiders/                   # Platform-specific spiders
│   ├── settings.py                # Crawler settings
│   └── run_spiders.py            # Crawler launcher
├── test_push_task.py              # Push notification testing
├── runspider-test.py              # Single crawler testing
├── init.py                        # Database initialization
├── requirements.txt               # Python dependencies
└── .env                          # Environment configuration
```

## Best Practices

1. **Database Indexing**: Ensure indexes on `platform`, `crawl_time`, and `title` columns for fast queries
2. **LLM Cost Management**: Cache analysis results to avoid redundant API calls
3. **Crawler Politeness**: Respect platform rate limits and robots.txt
4. **Notification Throttling**: Implement cooldown periods to avoid alert fatigue
5. **Data Retention**: Set up automatic archival for data older than 90 days
6. **Model Choice**: Consider Huawei Pangu for better Chinese language understanding and local deployment

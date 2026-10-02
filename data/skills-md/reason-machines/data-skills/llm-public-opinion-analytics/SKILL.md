---
name: llm-public-opinion-analytics
description: Multi-platform public opinion analysis assistant with web scraping, LLM-powered analytics, topic clustering, sentiment analysis, and multi-channel alerts
triggers:
  - analyze public opinion trends across social media platforms
  - scrape hot search rankings from Chinese platforms
  - set up sentiment analysis for news topics
  - cluster trending topics using LLM
  - configure multi-channel alerts for hot topics
  - build a public opinion monitoring system
  - analyze trending news with deep learning
  - track social media hot searches in real-time
---

# LLM-Based Public Opinion Analytics Assistant

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project is an intelligent public opinion analysis assistant that integrates real-time data from **15 mainstream platforms** across **26 ranking lists** with large language model (LLM) analysis capabilities. It provides conversational hot search queries, topic-specific searches, topic clustering, and sentiment analysis. The system supports:

- Real-time web scraping from platforms like Weibo, Bilibili, Douyin, Baidu, etc.
- LLM-powered content analysis (including video content extraction)
- Multi-channel push notifications (WeChat, Enterprise WeChat, Telegram, Email)
- Keyboard shortcuts for crawler control
- Quick data lookup and platform jumping

## Installation

### Prerequisites

1. **Python Environment**: Python 3.8+
2. **MySQL Database**: MySQL 5.7+ or 8.0+
3. **Browser Driver**: ChromeDriver or EdgeDriver

### Step 1: Browser Driver Setup

Download the driver matching your browser version:

- **Chrome**: [ChromeDriver Downloads](https://chromedriver.chromium.org/)
- **Edge**: [EdgeDriver Downloads](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

Add the driver to your system PATH:

```bash
# macOS/Linux
export PATH=$PATH:/path/to/driver/directory

# Windows: Add to System Environment Variables
```

Verify installation:

```bash
chromedriver --version
# or
msedgedriver --version
```

### Step 2: Clone and Install Dependencies

```bash
git clone https://github.com/hmmnxkl/LLM-Based-Intelligent-Public-Opinion-Analytics-Assistant.git
cd LLM-Based-Intelligent-Public-Opinion-Analytics-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Database Setup

Create MySQL database and tables:

```python
# Reference init.py for schema
import mysql.connector

conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD')
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS hotsearch_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
cursor.execute("USE hotsearch_db")

# Create tables (see init.py for full schema)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS hot_search_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        platform VARCHAR(50),
        title VARCHAR(500),
        url TEXT,
        rank_index INT,
        heat_value VARCHAR(100),
        collected_at DATETIME,
        content TEXT,
        sentiment VARCHAR(20),
        INDEX idx_platform (platform),
        INDEX idx_collected (collected_at)
    )
""")

conn.commit()
```

### Step 4: Environment Configuration

Create `.env` file in project root:

```bash
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=hotsearch_db

# LLM Configuration (OpenAI-compatible API)
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4

# Or use Huawei Pangu Model (local deployment)
# PANGU_MODEL_PATH=/path/to/pangu/model
# PANGU_API_URL=http://localhost:8080

# Push Notification Channels
# WeChat Work Bot
WECHAT_WORK_BOT_WEBHOOK=your_webhook_url

# WeChat Work App
WECHAT_WORK_CORP_ID=your_corp_id
WECHAT_WORK_AGENT_ID=your_agent_id
WECHAT_WORK_SECRET=your_secret

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_RECIPIENTS=recipient1@example.com,recipient2@example.com
```

## Core Components

### 1. Web Scraping System (`hotsearchcrawler/`)

The crawler cluster supports 15 platforms with 26 ranking lists:

```python
# Run all spiders
python run_spiders.py

# Test specific spider
python runspider-test.py weibo  # Test Weibo scraper
```

#### Crawler Configuration

Edit `hotsearchcrawler/settings.py`:

```python
# MySQL settings
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'hotsearch_db')

# Optional: Platform-specific cookies
COOKIES = {
    'weibo': 'your_weibo_cookies',
    'bilibili': 'your_bilibili_cookies'
}

# Crawler settings
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
```

#### Available Platforms

- Social Media: Weibo, Douyin, Kuaishou
- Video: Bilibili, Tencent Video
- News: Baidu, Toutiao, Zhihu
- E-commerce: Taobao, JD.com
- Gaming: Steam, Tap Tap
- Others: Tieba, Douban, etc.

### 2. Analysis System (`hotsearch_analysis_agent/`)

LLM-powered analysis engine for topic clustering, sentiment analysis, and report generation.

```python
from hotsearch_analysis_agent.analyzer import HotSearchAnalyzer

# Initialize analyzer
analyzer = HotSearchAnalyzer(
    api_key=os.getenv('OPENAI_API_KEY'),
    api_base=os.getenv('OPENAI_API_BASE'),
    model_name=os.getenv('MODEL_NAME', 'gpt-4')
)

# Analyze topics
topics = analyzer.fetch_topics(
    platform='weibo',
    start_date='2026-05-01',
    end_date='2026-05-20'
)

# Topic clustering
clusters = analyzer.cluster_topics(topics, n_clusters=5)

# Sentiment analysis
for topic in topics:
    sentiment = analyzer.analyze_sentiment(topic['title'], topic['content'])
    print(f"{topic['title']}: {sentiment}")

# Generate report
report = analyzer.generate_report(
    query="人工智能与前沿科技",
    platforms=['weibo', 'bilibili', 'zhihu'],
    days=7
)
print(report)
```

#### Custom LLM Integration

```python
# Using Huawei Pangu Model (local deployment)
from hotsearch_analysis_agent.llm import PanguLLM

pangu = PanguLLM(
    model_path=os.getenv('PANGU_MODEL_PATH'),
    api_url=os.getenv('PANGU_API_URL')
)

response = pangu.generate(
    prompt="分析以下新闻的情感倾向:\n{news_content}",
    max_tokens=500
)
```

### 3. Web Application (`app.py`)

FastAPI-based web interface for interactive queries and control.

```python
# Start the web application
python app.py

# Default runs on http://localhost:8000
```

#### API Endpoints

```python
from fastapi import FastAPI
from hotsearch_analysis_agent.api import router

app = FastAPI()
app.include_router(router)

# Example API calls
import httpx

# Query hot searches
response = httpx.get('http://localhost:8000/api/hot-search', params={
    'platform': 'weibo',
    'limit': 20
})

# Search by keyword
response = httpx.post('http://localhost:8000/api/search', json={
    'keyword': '人工智能',
    'platforms': ['weibo', 'zhihu'],
    'days': 7
})

# Start crawler
response = httpx.post('http://localhost:8000/api/crawler/start', json={
    'platforms': ['weibo', 'bilibili']
})

# Stop crawler
response = httpx.post('http://localhost:8000/api/crawler/stop')
```

## Push Notification System

Configure and test multi-channel alerts:

```python
# test_push_task.py
from hotsearch_analysis_agent.push import PushManager

manager = PushManager()

# Configure push task
task = {
    'name': 'AI Tech Monitor',
    'query': '人工智能',
    'platforms': ['weibo', 'zhihu', 'bilibili'],
    'schedule': '0 9,18 * * *',  # Cron format: 9 AM and 6 PM daily
    'channels': ['wechat_work', 'telegram', 'email'],
    'min_heat': 100000  # Minimum heat value threshold
}

manager.create_task(task)

# Test push manually
report = """
## AI Technology Hot Topics - 2026-05-20

### Key Findings
- GPT-6 context window leaked: 2M tokens
- DeepSeek V4 uses Huawei Ascend chips
- Chinese LLM API calls lead globally for 5 weeks

[Full report content...]
"""

# Send to WeChat Work
manager.send_wechat_work(report)

# Send to Telegram
manager.send_telegram(report)

# Send email
manager.send_email(
    subject="AI Technology Hot Topics - 2026-05-20",
    content=report
)
```

### Push Channel Configuration

```python
# WeChat Work Bot (Group Webhook)
import requests

def send_wechat_work_bot(content):
    webhook = os.getenv('WECHAT_WORK_BOT_WEBHOOK')
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    requests.post(webhook, json=data)

# Telegram Bot
from telegram import Bot

def send_telegram(content):
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot.send_message(chat_id=chat_id, text=content, parse_mode='Markdown')

# Email via SMTP
import smtplib
from email.mime.text import MIMEText

def send_email(subject, content):
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = os.getenv('SMTP_USER')
    msg['To'] = os.getenv('SMTP_RECIPIENTS')
    
    with smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
        server.send_message(msg)
```

## Common Usage Patterns

### Pattern 1: Daily Hot Topic Monitoring

```python
from datetime import datetime, timedelta
from hotsearch_analysis_agent.analyzer import HotSearchAnalyzer
from hotsearch_analysis_agent.push import PushManager

analyzer = HotSearchAnalyzer()
push_manager = PushManager()

# Get yesterday's hot topics
yesterday = datetime.now() - timedelta(days=1)
topics = analyzer.fetch_topics(
    platforms=['weibo', 'zhihu', 'bilibili'],
    start_date=yesterday.strftime('%Y-%m-%d'),
    heat_threshold=50000
)

# Cluster and analyze
clusters = analyzer.cluster_topics(topics, n_clusters=5)

# Generate report
report = analyzer.generate_report_from_clusters(clusters)

# Push to all channels
push_manager.broadcast(report, channels=['wechat_work', 'telegram', 'email'])
```

### Pattern 2: Keyword Alert System

```python
# Monitor specific keywords and send immediate alerts
from hotsearch_analysis_agent.monitor import KeywordMonitor

monitor = KeywordMonitor(
    keywords=['芯片', 'AI', '大模型', '华为'],
    platforms=['weibo', 'toutiao', 'zhihu'],
    check_interval=300  # Check every 5 minutes
)

def on_match(topic):
    """Callback when keyword is matched"""
    alert = f"""
    🔔 Keyword Alert: {topic['title']}
    Platform: {topic['platform']}
    Heat: {topic['heat_value']}
    URL: {topic['url']}
    """
    push_manager.send_telegram(alert)

monitor.start(callback=on_match)
```

### Pattern 3: Deep Content Analysis

```python
# Analyze news detail pages (including video content)
from hotsearch_analysis_agent.content_extractor import ContentExtractor

extractor = ContentExtractor()

# Get detailed content from URL
url = 'https://www.bilibili.com/video/BV13pSoBBEvX/'
content = extractor.extract(url)

print(f"Title: {content['title']}")
print(f"Type: {content['type']}")  # 'video' or 'article'
print(f"Content: {content['text'][:500]}...")  # Extracted transcript/text

# Analyze sentiment
sentiment = analyzer.analyze_sentiment(content['title'], content['text'])
print(f"Sentiment: {sentiment}")

# Extract entities
entities = analyzer.extract_entities(content['text'])
print(f"Entities: {entities}")
```

### Pattern 4: Custom Report Generation

```python
# Generate custom analytical report
report_config = {
    'title': '科技行业周报',
    'query': '人工智能 OR 芯片 OR 量子计算',
    'platforms': ['all'],
    'date_range': 7,
    'sections': [
        'core_findings',  # Key discoveries
        'news_details',   # Detailed news list
        'trend_analysis', # Trend analysis
        'entity_network'  # Entity relationship graph
    ],
    'output_format': 'markdown'
}

report = analyzer.generate_custom_report(**report_config)

# Save to file
with open(f"report_{datetime.now().strftime('%Y%m%d')}.md", 'w', encoding='utf-8') as f:
    f.write(report)
```

## Troubleshooting

### Issue 1: Browser Driver Errors

```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**Solution**: Ensure ChromeDriver/EdgeDriver is in system PATH and matches browser version.

```bash
# Check driver version
chromedriver --version

# Check Chrome version
google-chrome --version  # Linux
# or open chrome://version in browser

# Download matching version from https://chromedriver.chromium.org/
```

### Issue 2: Database Connection Failures

```
mysql.connector.errors.ProgrammingError: Access denied for user
```

**Solution**: Verify MySQL credentials in `.env` and ensure user has proper permissions.

```sql
-- Grant permissions
GRANT ALL PRIVILEGES ON hotsearch_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### Issue 3: LLM API Rate Limits

```
openai.error.RateLimitError: Rate limit exceeded
```

**Solution**: Implement request throttling or switch to local model:

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=10):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_minute=10)
def call_llm(prompt):
    return analyzer.generate(prompt)
```

### Issue 4: Crawler Being Blocked

**Solution**: Rotate user agents and add delays:

```python
# In hotsearchcrawler/settings.py
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 2
```

### Issue 5: Encoding Issues with Chinese Text

**Solution**: Ensure UTF-8 encoding throughout:

```python
# Database connection
import mysql.connector

conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE'),
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

# File operations
with open('report.md', 'w', encoding='utf-8') as f:
    f.write(report)
```

## Advanced Configuration

### Using Huawei Pangu Model (Local Deployment)

Download and deploy the model:

```bash
# Download from https://ai.gitcode.com/ascend-tribe/openpangu-embedded-7b-model
# Start model service
python -m hotsearch_analysis_agent.llm.pangu_server --model_path /path/to/model --port 8080
```

Configure in code:

```python
from hotsearch_analysis_agent.llm import PanguLLM

analyzer = HotSearchAnalyzer(
    llm=PanguLLM(api_url='http://localhost:8080')
)
```

### Distributed Crawling

Scale up with multiple crawler instances:

```bash
# Instance 1: Weibo, Zhihu
python run_spiders.py --platforms weibo,zhihu

# Instance 2: Bilibili, Douyin
python run_spiders.py --platforms bilibili,douyin

# Instance 3: News platforms
python run_spiders.py --platforms baidu,toutiao
```

## Project Structure Reference

```
.
├── app.py                          # Web application entry
├── run_spiders.py                  # Crawler launcher
├── runspider-test.py               # Crawler testing
├── test_push_task.py               # Push notification testing
├── init.py                         # Database initialization
├── requirements.txt                # Python dependencies
├── .env                            # Environment configuration
├── hotsearchcrawler/               # Crawler cluster
│   ├── spiders/                    # Platform-specific spiders
│   ├── settings.py                 # Crawler settings
│   └── pipelines.py                # Data pipelines
└── hotsearch_analysis_agent/       # Analysis system
    ├── analyzer.py                 # Core analysis engine
    ├── llm/                        # LLM integrations
    ├── push/                       # Push notification modules
    ├── api/                        # Web API endpoints
    └── content_extractor.py        # Content extraction utilities
```

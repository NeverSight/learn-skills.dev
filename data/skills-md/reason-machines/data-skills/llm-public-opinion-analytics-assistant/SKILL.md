---
name: llm-public-opinion-analytics-assistant
description: Multi-platform hot search crawler and LLM-powered public opinion analysis system with clustering, sentiment analysis, and multi-channel push notifications
triggers:
  - set up public opinion monitoring system
  - analyze hot topics from multiple platforms
  - configure sentiment analysis for social media
  - create hot search crawler with push notifications
  - implement topic clustering and sentiment tracking
  - build multi-platform trending data aggregator
  - deploy LLM-based opinion analytics
  - monitor and analyze public sentiment trends
---

# LLM-Based Intelligent Public Opinion Analytics Assistant

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## Overview

This project is an intelligent public opinion analysis assistant that combines real-time data from **26 trending lists across 15 mainstream platforms** with large language model (LLM) analysis capabilities. It provides conversational hot search queries, topic-specific searches, topic clustering analysis, and sentiment analysis through a web interface. The system supports keyboard shortcuts for crawler control, multi-platform data retrieval with direct navigation, and multi-channel hot topic push notifications (email, WeChat, Enterprise WeChat, Telegram).

## Key Features

- **Multi-Platform Data Collection**: Crawls 26 trending lists from 15 platforms
- **LLM-Powered Analysis**: Topic clustering, sentiment analysis, and trend detection
- **Conversational Interface**: Natural language queries for data exploration
- **Video Content Analysis**: Extracts information even from video-based news
- **Multi-Channel Notifications**: Email, WeChat Work, Telegram bot push notifications
- **Crawler Control**: Quick start/stop via keyboard shortcuts
- **Database Storage**: MySQL-based data persistence

## Installation

### Prerequisites

**Browser Driver Setup** (Required for news detail extraction):

1. **Check browser version**:
   - Open Edge/Chrome → Settings → About
   - Note your version (e.g., `115.0.5790.102`)

2. **Download matching driver**:
   - Chrome: https://chromedriver.chromium.org/
   - Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

3. **Install driver**:
   ```bash
   # Linux/macOS
   sudo mv chromedriver /usr/local/bin/
   sudo chmod +x /usr/local/bin/chromedriver
   
   # Windows: Add driver directory to PATH
   # e.g., C:\WebDriver\chromedriver.exe
   ```

4. **Verify installation**:
   ```bash
   chromedriver --version
   ```

### Environment Setup

```bash
# Clone repository
git clone https://github.com/hmmnxkl/LLM-Based-Intelligent-Public-Opinion-Analytics-Assistant.git
cd LLM-Based-Intelligent-Public-Opinion-Analytics-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Configuration

1. **Install MySQL** (8.0+ recommended)

2. **Create database and tables**:
   ```python
   # Reference init.py for schema
   import mysql.connector
   
   conn = mysql.connector.connect(
       host='localhost',
       user='your_user',
       password='your_password'
   )
   cursor = conn.cursor()
   
   # Create database
   cursor.execute("CREATE DATABASE IF NOT EXISTS hotsearch_db CHARACTER SET utf8mb4")
   cursor.execute("USE hotsearch_db")
   
   # Create tables (see init.py for full schema)
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS hot_searches (
       id INT AUTO_INCREMENT PRIMARY KEY,
       platform VARCHAR(50),
       title VARCHAR(500),
       url VARCHAR(1000),
       rank INT,
       heat_value VARCHAR(100),
       timestamp DATETIME,
       content TEXT,
       sentiment VARCHAR(50),
       INDEX idx_platform_timestamp (platform, timestamp)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
   """)
   
   conn.commit()
   cursor.close()
   conn.close()
   ```

### Configuration Files

**Create `.env` file in project root**:
```bash
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=hotsearch_db

# LLM Configuration (OpenAI-compatible API)
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4

# Or use Huawei Pangu Model (recommended for Chinese)
# PANGU_API_KEY=your_pangu_key
# PANGU_BASE_URL=your_pangu_endpoint

# Push Notification Channels
# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com

# Enterprise WeChat Bot
WECHAT_WORK_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

**Crawler Configuration** (`hotsearchcrawler/settings.py`):
```python
# MySQL settings
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'your_user'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'hotsearch_db'

# Optional: Platform-specific cookies
COOKIES = {
    'weibo': 'your_weibo_cookie',
    'douyin': 'your_douyin_cookie'
}

# Concurrent requests
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
```

## Usage

### Starting the System

**1. Launch the web application**:
```bash
python app.py
```
Access at: `http://localhost:5000`

**2. Start crawlers** (via web interface or CLI):
```bash
# Manual crawler start for testing
python run_spiders.py

# Or test individual spider
cd hotsearchcrawler
scrapy crawl weibo_spider
scrapy crawl bilibili_spider
```

### Core API Usage

#### Conversational Query Interface

```python
from hotsearch_analysis_agent.agent import OpinionAnalysisAgent

# Initialize agent
agent = OpinionAnalysisAgent(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL'),
    model=os.getenv('OPENAI_MODEL', 'gpt-4')
)

# Query hot searches
response = agent.query("Show me top trending topics about AI")
print(response['analysis'])

# Topic clustering
clusters = agent.cluster_topics("人工智能", days=7)
for cluster in clusters:
    print(f"Cluster: {cluster['theme']}")
    print(f"Articles: {len(cluster['articles'])}")
    print(f"Sentiment: {cluster['sentiment']}")

# Sentiment analysis
sentiment = agent.analyze_sentiment("特定主题关键词", platform="weibo")
print(f"Positive: {sentiment['positive']}%")
print(f"Negative: {sentiment['negative']}%")
print(f"Neutral: {sentiment['neutral']}%")
```

#### Direct Database Access

```python
import mysql.connector
from datetime import datetime, timedelta

conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)

cursor = conn.cursor(dictionary=True)

# Get recent hot searches
cursor.execute("""
    SELECT platform, title, heat_value, url, timestamp
    FROM hot_searches
    WHERE timestamp >= %s
    ORDER BY rank ASC
    LIMIT 50
""", (datetime.now() - timedelta(hours=24),))

hot_topics = cursor.fetchall()

for topic in hot_topics:
    print(f"[{topic['platform']}] {topic['title']} - {topic['heat_value']}")
```

#### Setting Up Push Notifications

```python
from hotsearch_analysis_agent.push_service import PushService

# Initialize push service
push_service = PushService()

# Create push task
task_config = {
    'name': 'AI Tech Trending Monitor',
    'keywords': ['人工智能', '大模型', 'AI技术'],
    'platforms': ['weibo', 'bilibili', 'zhihu'],
    'schedule': '0 9,18 * * *',  # Twice daily at 9 AM and 6 PM
    'channels': ['email', 'wechat_work', 'telegram'],
    'analysis_depth': 'detailed',  # 'summary' or 'detailed'
    'min_heat_threshold': 100000
}

push_service.create_task(task_config)

# Test push notification
push_service.test_push(
    channel='email',
    subject='Test: AI Trending Report',
    content='This is a test notification.'
)
```

### Crawler Management

```python
from hotsearchcrawler.crawler_manager import CrawlerManager

manager = CrawlerManager()

# Start all crawlers
manager.start_all()

# Start specific platform
manager.start_spider('weibo_spider')

# Stop all crawlers
manager.stop_all()

# Get crawler status
status = manager.get_status()
print(f"Active crawlers: {status['active']}")
print(f"Items scraped: {status['items_count']}")
```

## Common Patterns

### Pattern 1: Daily Hot Topic Report

```python
from hotsearch_analysis_agent.report_generator import ReportGenerator
from datetime import datetime

generator = ReportGenerator()

# Generate daily report
report = generator.generate_daily_report(
    date=datetime.now(),
    topics=['科技', '财经', '国际'],
    include_sentiment=True,
    include_clustering=True,
    output_format='markdown'
)

# Save report
with open(f"report_{datetime.now().strftime('%Y%m%d')}.md", 'w', encoding='utf-8') as f:
    f.write(report)

# Auto-push report
generator.push_report(report, channels=['email', 'wechat_work'])
```

### Pattern 2: Real-Time Keyword Monitoring

```python
from hotsearch_analysis_agent.monitor import KeywordMonitor
import time

monitor = KeywordMonitor()

# Define alert keywords
critical_keywords = ['安全事故', '数据泄露', '产品召回']

monitor.add_keywords(critical_keywords)

# Start monitoring
while True:
    alerts = monitor.check_new_mentions()
    
    for alert in alerts:
        print(f"ALERT: {alert['keyword']} mentioned in {alert['platform']}")
        print(f"Title: {alert['title']}")
        print(f"Heat: {alert['heat_value']}")
        print(f"URL: {alert['url']}")
        
        # Immediate push notification
        monitor.push_alert(alert, priority='high')
    
    time.sleep(300)  # Check every 5 minutes
```

### Pattern 3: Multi-Platform Topic Correlation

```python
from hotsearch_analysis_agent.correlator import TopicCorrelator

correlator = TopicCorrelator()

# Find correlated topics across platforms
topic_keyword = "芯片技术"
correlation = correlator.find_cross_platform_correlation(
    keyword=topic_keyword,
    platforms=['weibo', 'zhihu', 'toutiao', 'bilibili'],
    time_window_hours=48
)

print(f"Topic: {topic_keyword}")
print(f"Total mentions: {correlation['total_mentions']}")
print(f"Platform distribution: {correlation['platform_dist']}")
print(f"Peak time: {correlation['peak_timestamp']}")
print(f"Related topics: {', '.join(correlation['related_topics'])}")
```

### Pattern 4: Sentiment Trend Analysis

```python
from hotsearch_analysis_agent.sentiment_tracker import SentimentTracker
import matplotlib.pyplot as plt

tracker = SentimentTracker()

# Track sentiment over time
sentiment_history = tracker.track_sentiment(
    keyword="新能源汽车",
    days=30,
    platforms=['weibo', 'zhihu']
)

# Visualize trend
dates = [s['date'] for s in sentiment_history]
positive = [s['positive'] for s in sentiment_history]
negative = [s['negative'] for s in sentiment_history]

plt.figure(figsize=(12, 6))
plt.plot(dates, positive, label='Positive', color='green')
plt.plot(dates, negative, label='Negative', color='red')
plt.xlabel('Date')
plt.ylabel('Sentiment Score (%)')
plt.title('Sentiment Trend: 新能源汽车')
plt.legend()
plt.savefig('sentiment_trend.png')
```

## Testing

### Test Individual Components

```bash
# Test crawler functionality
python runspider-test.py

# Test push notification
python test_push_task.py

# Test LLM analysis
python -m hotsearch_analysis_agent.test_analysis
```

### Sample Test Script

```python
# test_system.py
import os
from dotenv import load_dotenv
from hotsearch_analysis_agent.agent import OpinionAnalysisAgent

load_dotenv()

def test_query():
    agent = OpinionAnalysisAgent()
    result = agent.query("What are the top 5 trending topics today?")
    assert result is not None
    assert 'analysis' in result
    print("✓ Query test passed")

def test_clustering():
    agent = OpinionAnalysisAgent()
    clusters = agent.cluster_topics("科技", days=3)
    assert len(clusters) > 0
    print(f"✓ Clustering test passed ({len(clusters)} clusters found)")

def test_sentiment():
    agent = OpinionAnalysisAgent()
    sentiment = agent.analyze_sentiment("人工智能")
    assert 'positive' in sentiment
    assert 'negative' in sentiment
    print("✓ Sentiment analysis test passed")

if __name__ == '__main__':
    test_query()
    test_clustering()
    test_sentiment()
    print("\nAll tests passed!")
```

## Troubleshooting

### Browser Driver Issues

**Error**: `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solution**:
```bash
# Verify driver location
which chromedriver  # Linux/macOS
where chromedriver  # Windows

# Add to PATH if missing
export PATH=$PATH:/path/to/driver/directory  # Linux/macOS

# Or specify driver path in code
from selenium import webdriver
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
```

### Database Connection Errors

**Error**: `mysql.connector.errors.ProgrammingError: Access denied for user`

**Solution**:
```sql
-- Grant proper privileges
GRANT ALL PRIVILEGES ON hotsearch_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### Crawler Not Collecting Data

**Diagnostics**:
```python
# Check crawler logs
import logging
logging.basicConfig(level=logging.DEBUG)

# Verify platform accessibility
import requests
response = requests.get('https://weibo.com/hot/search')
print(f"Status: {response.status_code}")

# Test individual spider
cd hotsearchcrawler
scrapy crawl weibo_spider -L DEBUG
```

### LLM Analysis Returning Empty Results

**Check**:
- API key validity and rate limits
- Network connectivity to LLM endpoint
- Input text encoding (must be UTF-8)

```python
# Debug LLM connection
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_BASE_URL')

try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Test"}]
    )
    print("✓ LLM connection successful")
except Exception as e:
    print(f"✗ LLM error: {e}")
```

### Push Notifications Not Sending

**Email (SMTP)**:
```python
# Test SMTP connection
import smtplib
from email.mime.text import MIMEText

try:
    server = smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT')))
    server.starttls()
    server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
    print("✓ SMTP connection successful")
    server.quit()
except Exception as e:
    print(f"✗ SMTP error: {e}")
```

**WeChat Work**:
```python
# Test webhook
import requests
import json

webhook_url = os.getenv('WECHAT_WORK_WEBHOOK')
data = {
    "msgtype": "text",
    "text": {"content": "Test notification"}
}
response = requests.post(webhook_url, json=data)
print(f"Response: {response.json()}")
```

## Advanced Configuration

### Custom LLM Model (Huawei Pangu)

```python
# hotsearch_analysis_agent/llm_config.py
from pangu_client import PanguClient

client = PanguClient(
    api_key=os.getenv('PANGU_API_KEY'),
    endpoint=os.getenv('PANGU_BASE_URL')
)

def analyze_with_pangu(text, task='sentiment'):
    response = client.complete(
        prompt=f"分析以下文本的{task}:\n{text}",
        max_tokens=2000,
        temperature=0.7
    )
    return response['text']
```

### Adding New Platform Crawlers

```python
# hotsearchcrawler/spiders/custom_spider.py
import scrapy
from hotsearchcrawler.items import HotSearchItem

class CustomPlatformSpider(scrapy.Spider):
    name = 'custom_spider'
    start_urls = ['https://example.com/trending']
    
    def parse(self, response):
        for item in response.css('.trending-item'):
            yield HotSearchItem(
                platform='custom_platform',
                title=item.css('.title::text').get(),
                url=item.css('a::attr(href)').get(),
                rank=item.css('.rank::text').get(),
                heat_value=item.css('.heat::text').get(),
                timestamp=datetime.now()
            )
```

### Custom Analysis Pipelines

```python
# hotsearch_analysis_agent/custom_analyzer.py
from hotsearch_analysis_agent.base_analyzer import BaseAnalyzer

class IndustrySpecificAnalyzer(BaseAnalyzer):
    def __init__(self, industry_keywords):
        super().__init__()
        self.industry_keywords = industry_keywords
    
    def filter_relevant_topics(self, topics):
        return [
            t for t in topics 
            if any(kw in t['title'] for kw in self.industry_keywords)
        ]
    
    def generate_industry_report(self, topics):
        relevant = self.filter_relevant_topics(topics)
        sentiment = self.batch_sentiment_analysis(relevant)
        clusters = self.cluster_by_subtopic(relevant)
        
        return {
            'total_mentions': len(relevant),
            'sentiment_distribution': sentiment,
            'topic_clusters': clusters,
            'key_influencers': self.identify_influencers(relevant)
        }
```

## Resources

- **Official Repository**: https://github.com/hmmnxkl/LLM-Based-Intelligent-Public-Opinion-Analytics-Assistant
- **Huawei Pangu Model**: https://ai.gitcode.com/ascend-tribe/openpangu-embedded-7b-model
- **Scrapy Documentation**: https://docs.scrapy.org/
- **Selenium WebDriver**: https://www.selenium.dev/documentation/

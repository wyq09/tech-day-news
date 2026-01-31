"""
配置文件
"""
import os

# 基础配置
BASE_DIR = "/home/ubuntu/www/tech-day-news"
OUTPUT_DIR = os.path.join(BASE_DIR, "{year}")
ARCHIVE_INDEX = os.path.join(BASE_DIR, "index.html")

# RSS 源配置（优先使用 RSS，更稳定）
RSS_SOURCES = {
    "hacker_news": {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/rss",
        "category": "tech"
    },
    "v2ex": {
        "name": "V2EX",
        "url": "https://www.v2ex.com/index.xml",
        "category": "tech"
    },
    "infoq": {
        "name": "InfoQ",
        "url": "https://www.infoq.cn/feed",
        "category": "tech"
    },
    "oschina": {
        "name": "开源中国",
        "url": "https://www.oschina.net/news/rss",
        "category": "tech"
    },
    "solidot": {
        "name": "Solidot",
        "url": "https://www.solidot.org/index.rss",
        "category": "tech"
    },
}

# 需要抓取的站点（RSS不可用时使用）
WEB_SOURCES = {
    "kr36": {
        "name": "36氪",
        "url": "https://36kr.com/",
        "category": "hot"
    },
    "sspai": {
        "name": "少数派",
        "url": "https://sspai.com/",
        "category": "product"
    },
    "huxiu": {
        "name": "虎嗅",
        "url": "https://www.huxiu.com/",
        "category": "hot"
    }
}

# 栏目配置
CATEGORIES = {
    "hot": {
        "name": "今日热点",
        "min_items": 3,
        "max_items": 5,
        "keywords": ["热点", "爆", "突发", "重磅", "大新闻", "发布"]
    },
    "tech": {
        "name": "技术趋势",
        "min_items": 3,
        "max_items": 5,
        "keywords": ["技术", "架构", "开发", "开源", "算法", "编程", "框架"]
    },
    "product": {
        "name": "产品观察",
        "min_items": 3,
        "max_items": 5,
        "keywords": ["AI", "人工智能", "产品", "应用", "工具", "App", "平台"]
    },
    "recommend": {
        "name": "推荐阅读",
        "min_items": 3,
        "max_items": 5,
        "keywords": ["深度", "分析", "思考", "观察", "研究", "干货"]
    }
}

# AI 关键词（产品观察优先）
AI_KEYWORDS = ["AI", "人工智能", "GPT", "LLM", "大模型", "机器学习", "深度学习", "ChatGPT", "Claude"]

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
        "category": "tech",
        "count": 20
    },
    "v2ex": {
        "name": "V2EX",
        "url": "https://www.v2ex.com/index.xml",
        "category": "tech",
        "count": 20
    },
    "infoq": {
        "name": "InfoQ",
        "url": "https://www.infoq.cn/feed",
        "category": "tech",
        "count": 20
    },
    "oschina": {
        "name": "开源中国",
        "url": "https://www.oschina.net/news/rss",
        "category": "tech",
        "count": 20
    },
    "solidot": {
        "name": "Solidot",
        "url": "https://www.solidot.org/index.rss",
        "category": "tech",
        "count": 20
    },
    "jianshu": {
        "name": "简书",
        "url": "https://www.jianshu.com/top/monthly/rss",
        "category": "tech",
        "count": 20
    },
    "csdn": {
        "name": "CSDN",
        "url": "https://blog.csdn.net/rss/new",
        "category": "tech",
        "count": 20
    },
}

# 需要抓取的站点（RSS不可用时使用）
WEB_SOURCES = {
    "kr36": {
        "name": "36氪",
        "url": "https://36kr.com/",
        "category": "hot",
        "count": 20
    },
    "sspai": {
        "name": "少数派",
        "url": "https://sspai.com/",
        "category": "product",
        "count": 20
    },
    "huxiu": {
        "name": "虎嗅",
        "url": "https://www.huxiu.com/",
        "category": "hot",
        "count": 20
    }
}

# 栏目配置（黑客帝国风格）
CATEGORIES = {
    "hot": {
        "name": "系统警报 - 今日热点",
        "min_items": 5,
        "max_items": 10,
        "keywords": ["热点", "爆", "突发", "重磅", "大新闻", "发布", "AI", "人工智能"]
    },
    "tech": {
        "name": "核心代码 - 技术趋势",
        "min_items": 5,
        "max_items": 10,
        "keywords": ["技术", "架构", "开发", "开源", "算法", "编程", "框架", "大模型", "LLM", "深度学习"]
    },
    "product": {
        "name": "矩阵程序 - AI产品观察",
        "min_items": 5,
        "max_items": 10,
        "keywords": ["AI", "人工智能", "GPT", "产品", "应用", "工具", "App", "平台", "模型", "智能"]
    },
    "recommend": {
        "name": "数据流 - 推荐阅读",
        "min_items": 5,
        "max_items": 10,
        "keywords": ["深度", "分析", "思考", "观察", "研究", "干货", "白皮书", "报告"]
    }
}

# AI 关键词（扩充版）
AI_KEYWORDS = [
    "AI", "人工智能", "GPT", "LLM", "大模型", "机器学习", "深度学习",
    "ChatGPT", "Claude", "OpenAI", "神经网络", "Transformer", "提示词",
    "Prompt", "智能", "自动化", "生成式", "AGI", "Stable Diffusion",
    "Midjourney", "Copilot", "文心一言", "通义千问", "Kimi", "月之暗面",
    "智谱", "豆包", "RAG", "Agent", "多模态", "计算机视觉", "NLP"
]

"""
RSS 订阅源抓取
"""
import feedparser
from typing import List
from src.utils.article import Article
from src.config import RSS_SOURCES

def fetch_rss_feeds() -> List[Article]:
    """抓取所有 RSS 源"""
    articles = []

    # 优先抓取国内源
    sources_order = ['v2ex', 'infoq', 'oschina', 'solidot', 'hacker_news']

    for source_id in sources_order:
        if source_id not in RSS_SOURCES:
            continue

        config = RSS_SOURCES[source_id]
        try:
            print(f"正在抓取 {config['name']}...")
            feed = feedparser.parse(config['url'])

            for entry in feed.entries[:20]:  # 每个源取前20条
                # 提取摘要
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description

                # 清理 HTML 标签
                summary = strip_html(summary)

                article = Article(
                    title=entry.title,
                    url=entry.link,
                    summary=summary[:200] + "..." if len(summary) > 200 else summary,
                    source=config['name'],
                    category=config['category']
                )

                articles.append(article)

            print(f"  ✓ {config['name']} 抓取了 {len(feed.entries[:20])} 条")

        except Exception as e:
            print(f"  ✗ {config['name']} 抓取失败: {e}")

    return articles

def strip_html(text: str) -> str:
    """移除 HTML 标签"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

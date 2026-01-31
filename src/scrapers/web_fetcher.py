"""
Web 站点抓取（用于没有 RSS 的站点）
"""
import requests
from bs4 import BeautifulSoup
from typing import List
from src.utils.article import Article
from src.config import WEB_SOURCES

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_web_sites() -> List[Article]:
    """抓取 Web 站点"""
    articles = []

    # 优先抓取国内源
    sources_order = ['sspai', 'kr36', 'huxiu']

    for source_id in sources_order:
        if source_id not in WEB_SOURCES:
            continue

        config = WEB_SOURCES[source_id]
        try:
            print(f"正在抓取 {config['name']}...")
            articles.extend(fetch_site(source_id, config))
        except Exception as e:
            print(f"  ✗ {config['name']} 抓取失败: {e}")

    return articles

def fetch_site(site_id: str, config: dict) -> List[Article]:
    """根据站点类型抓取"""
    if site_id == "kr36":
        return fetch_36kr(config)
    elif site_id == "sspai":
        return fetch_sspai(config)
    elif site_id == "huxiu":
        return fetch_huxiu(config)
    return []

def fetch_36kr(config: dict) -> List[Article]:
    """抓取 36氪"""
    articles = []
    url = "https://36kr.com/api/market/channel/nextpage"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()

        if data.get('data') and data['data'].get('item'):
            for item in data['data']['item'][:15]:
                if not item.get('widgetTitle') or not item.get('widgetUrl'):
                    continue

                article = Article(
                    title=item['widgetTitle'],
                    url=f"https://36kr.com/p/{item['itemId']}",
                    summary=item.get('widgetSummary', '')[:200] if item.get('widgetSummary') else '',
                    source=config['name'],
                    category=config['category']
                )
                articles.append(article)

        print(f"  ✓ 36氪 抓取了 {len(articles)} 条")

    except Exception as e:
        print(f"  ✗ 36氪 API 抓取失败，尝试 HTML 抓取...")
        articles = fetch_36kr_html(config)

    return articles

def fetch_36kr_html(config: dict) -> List[Article]:
    """备用：HTML 方式抓取 36氪"""
    articles = []
    response = requests.get(config['url'], headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, 'lxml')

    # 找文章标题链接
    for item in soup.select('article.item')[:15]:
        title_tag = item.select_one('h2 a, a.article-title')
        if not title_tag:
            continue

        article = Article(
            title=title_tag.get_text(strip=True),
            url=f"https://36kr.com{title_tag['href']}" if title_tag['href'].startswith('/') else title_tag['href'],
            summary=item.get_text(strip=True)[:200],
            source=config['name'],
            category=config['category']
        )
        articles.append(article)

    return articles

def fetch_sspai(config: dict) -> List[Article]:
    """抓取少数派（使用 RSS）"""
    articles = []
    try:
        import feedparser
        feed = feedparser.parse("https://sspai.com/feed")

        for entry in feed.entries[:15]:
            summary = entry.get('summary', entry.get('description', ''))

            article = Article(
                title=entry.title,
                url=entry.link,
                summary=summary[:200] + "..." if len(summary) > 200 else summary,
                source=config['name'],
                category=config['category']
            )
            articles.append(article)

        print(f"  ✓ 少数派 抓取了 {len(articles)} 条")

    except Exception as e:
        print(f"  ✗ 少数派 RSS 抓取失败: {e}")

    return articles

def fetch_huxiu(config: dict) -> List[Article]:
    """抓取虎嗅（使用 RSS）"""
    articles = []
    try:
        import feedparser
        feed = feedparser.parse("https://www.huxiu.com/rss/0.xml")

        for entry in feed.entries[:15]:
            summary = entry.get('summary', entry.get('description', ''))

            article = Article(
                title=entry.title,
                url=entry.link,
                summary=summary[:200] + "..." if len(summary) > 200 else summary,
                source=config['name'],
                category=config['category']
            )
            articles.append(article)

        print(f"  ✓ 虎嗅 抓取了 {len(articles)} 条")

    except Exception as e:
        print(f"  ✗ 虎嗅 RSS 抓取失败: {e}")

    return articles

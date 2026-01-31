"""
RSS 订阅源抓取
"""
import feedparser
import socket
import requests
from typing import List
from src.utils.article import Article
from src.config import RSS_SOURCES

# 设置全局超时
socket.setdefaulttimeout(20)

# 代理配置
PROXIES = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

def fetch_rss_feeds() -> List[Article]:
    """抓取所有 RSS 源"""
    articles = []

    # 源抓取顺序（国内源优先，国外源放后面）
    sources_order = ['infoq', 'oschina', 'solidot', 'jianshu', 'csdn', 'v2ex', 'hacker_news']

    for source_id in sources_order:
        if source_id not in RSS_SOURCES:
            continue

        config = RSS_SOURCES[source_id]
        count = config.get('count', 20)

        # 根据源是否在国内决定是否使用代理
        domestic_sources = ['infoq', 'oschina', 'solidot', 'jianshu', 'csdn']
        use_proxy = source_id not in domestic_sources

        # 重试机制（3次）
        for retry in range(3):
            try:
                print(f"正在抓取 {config['name']}... (尝试 {retry + 1}/3) {'[代理]' if use_proxy else '[直连]'}")

                # 使用requests抓取（带超时和可选代理）
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }

                kwargs = {'headers': headers, 'timeout': 15, 'verify': False}
                if use_proxy:
                    kwargs['proxies'] = PROXIES

                response = requests.get(config['url'], **kwargs)
                response.raise_for_status()

                # 用feedparser解析
                feed = feedparser.parse(response.content)

                # 检查是否有错误
                if feed.get('bozo') and retry == 0:
                    print(f"  ⚠ {config['name']} 解析出错，重试中...")
                    continue

                entries = feed.get('entries', [])

                if not entries:
                    print(f"  ⚠ {config['name']} 没有获取到数据")
                    break

                for entry in entries[:count]:  # 每个源取配置的数量
                    try:
                        # 提取摘要
                        summary = ""
                        if hasattr(entry, 'summary'):
                            summary = entry.summary
                        elif hasattr(entry, 'description'):
                            summary = entry.description

                        # 清理 HTML 标签和图片
                        summary = strip_html(summary)
                        summary = strip_images(summary)

                        article = Article(
                            title=entry.title,
                            url=entry.link,
                            summary=summary[:300] + "..." if len(summary) > 300 else summary,
                            source=config['name'],
                            category=config['category']
                        )

                        articles.append(article)
                    except Exception as e:
                        print(f"    ✗ 处理文章失败: {e}")
                        continue

                print(f"  ✓ {config['name']} 抓取了 {len(entries[:count])} 条")
                break  # 成功，跳出重试循环

            except requests.exceptions.Timeout:
                if retry < 2:
                    print(f"  ⚠ {config['name']} 超时，重试中...")
                    continue
                else:
                    print(f"  ✗ {config['name']} 多次超时，跳过")
                    break
            except requests.exceptions.RequestException as e:
                if retry < 2:
                    print(f"  ⚠ {config['name']} 抓取失败: {e}，重试中...")
                    continue
                else:
                    print(f"  ✗ {config['name']} 最终失败: {e}")
                    break
            except Exception as e:
                if retry < 2:
                    print(f"  ⚠ {config['name']} 抓取失败: {e}，重试中...")
                    continue
                else:
                    print(f"  ✗ {config['name']} 最终失败: {e}")
                    break

    return articles

def strip_html(text: str) -> str:
    """移除 HTML 标签"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def strip_images(text: str) -> str:
    """移除图片相关内容"""
    import re
    # 移除图片标签
    text = re.sub(r'<img[^>]*>', '', text, flags=re.IGNORECASE)
    # 移除图片描述
    text = re.sub(r'\[图片\]', '', text)
    text = re.sub(r'图片[:：].*?(?:\n|$)', '', text)
    return text.strip()

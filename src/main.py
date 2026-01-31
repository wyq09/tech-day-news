#!/usr/bin/env python3
"""
科技日报主程序
"""
import sys
import os
from datetime import datetime
from typing import List

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.scrapers.rss_fetcher import fetch_rss_feeds
from src.scrapers.web_fetcher import fetch_web_sites
from src.categorizer import categorize_articles
from src.generator import HTMLGenerator

def main(date: datetime = None):
    """主函数"""
    if date is None:
        date = datetime.now()

    print(f"\n{'='*60}")
    print(f"开始生成科技日报 - {date.strftime('%Y-%m-%d')}")
    print(f"{'='*60}\n")

    # 1. 抓取所有源
    print("第一步：抓取资讯源...")
    articles = []

    # RSS 源
    rss_articles = fetch_rss_feeds()
    articles.extend(rss_articles)

    # Web 源
    web_articles = fetch_web_sites()
    articles.extend(web_articles)

    print(f"\n✓ 共抓取 {len(articles)} 条资讯\n")

    if not articles:
        print("✗ 没有抓取到任何资讯")
        return False

    # 2. 分类
    print("第二步：分类整理...")
    categorized = categorize_articles(articles)

    for cat_id, arts in categorized.items():
        print(f"  {cat_id}: {len(arts)} 条")

    # 3. 生成日报
    print("\n第三步：生成日报页面...")
    generator = HTMLGenerator()
    daily_path = generator.generate_daily(date, categorized)

    # 4. 更新归档
    print("\n第四步：更新归档页面...")
    archive_data = generator.load_archive_data()
    archive_path = generator.generate_archive(archive_data)

    print(f"\n{'='*60}")
    print(f"✓ 完成！")
    print(f"  日报: {daily_path}")
    print(f"  归档: {archive_path}")
    print(f"{'='*60}\n")

    return True

if __name__ == '__main__':
    main()

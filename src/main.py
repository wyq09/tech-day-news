"""主程序入口"""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from classifier import ZhipuClassifier
from generator import HTMLGenerator
from archive import ArchiveManager

# 导入各站点抓取器
from fetchers.hackernews import HackerNewsFetcher
from fetchers.v2ex import V2EXFetcher
from fetchers.kr36 import Kr36Fetcher
from fetchers.sspai import SspaiFetcher
from fetchers.huxiu import HuxiuFetcher
from fetchers.infoq import InfoQFetcher
from fetchers.oschina import OschinaFetcher
from fetchers.solidot import SolidotFetcher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/news-generator.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


# 所有抓取器列表
FETCHERS = [
    HackerNewsFetcher(),
    V2EXFetcher(),
    Kr36Fetcher(),
    SspaiFetcher(),
    HuxiuFetcher(),
    InfoQFetcher(),
    OschinaFetcher(),
    SolidotFetcher(),
]


def fetch_all_news(limit_per_source: int = 15) -> list:
    """从所有站点抓取资讯

    Args:
        limit_per_source: 每个站点最多抓取条数

    Returns:
        list: 所有资讯列表
    """
    logger.info(f"开始抓取资讯，共 {len(FETCHERS)} 个站点")

    all_items = []

    for fetcher in FETCHERS:
        try:
            items = fetcher.fetch(limit=limit_per_source)
            all_items.extend(items)
            logger.info(f"{fetcher.__class__.__name__}: 抓取 {len(items)} 条")
        except Exception as e:
            logger.error(f"{fetcher.__class__.__name__}: 抓取失败 - {e}")

    logger.info(f"总共抓取 {len(all_items)} 条资讯")
    return all_items


def deduplicate_items(items: list) -> list:
    """去重（基于 URL）"""
    seen = set()
    unique_items = []

    for item in items:
        url_key = item.url.lower()
        if url_key not in seen:
            seen.add(url_key)
            unique_items.append(item)

    if len(unique_items) < len(items):
        logger.info(f"去重: {len(items)} -> {len(unique_items)}")

    return unique_items


def main():
    """主函数"""
    # 确保日志目录存在
    os.makedirs("logs", exist_ok=True)

    logger.info("=" * 50)
    logger.info("科技日报生成器启动")
    logger.info("=" * 50)

    try:
        # 1. 抓取资讯
        logger.info("第一步：抓取资讯")
        items = fetch_all_news(limit_per_source=15)

        if not items:
            logger.warning("没有抓取到任何资讯")
            return

        # 2. 去重
        logger.info("第二步：去重")
        items = deduplicate_items(items)

        # 3. AI 分类
        logger.info("第三步：AI 分类")
        classifier = ZhipuClassifier()
        categorized = classifier.classify_items(items)

        # 4. 生成导语
        logger.info("第四步：生成导语")
        date = datetime.now().strftime("%Y-%m-%d")
        intro = classifier.generate_intro(categorized, date)

        # 5. 生成 HTML
        logger.info("第五步：生成 HTML")
        generator = HTMLGenerator(output_dir=".")
        html = generator.generate_daily(date, categorized, intro)
        filepath = generator.save_daily(date, html)

        # 6. 更新归档
        logger.info("第六步：更新归档")
        archive_manager = ArchiveManager(data_dir="data", output_dir=".")
        archive_manager.add_and_update(date, intro, filepath)

        logger.info("=" * 50)
        logger.info(f"科技日报生成完成: {filepath}")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"生成失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

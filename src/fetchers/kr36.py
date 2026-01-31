"""36氪 抓取器 - 使用 RSS"""
import logging
import feedparser
from typing import List
from datetime import datetime

from ..models import NewsItem
from .base import BaseFetcher, retry

logger = logging.getLogger(__name__)


class Kr36Fetcher(BaseFetcher):
    """36氪 抓取器

    使用 RSS: https://36kr.com/feed
    """

    FETCH_TYPE = "rss"
    RSS_URL = "https://36kr.com/feed"

    @retry(times=3)
    def fetch(self, limit: int = 20) -> List[NewsItem]:
        """抓取 36氪 最新资讯"""
        try:
            feed = feedparser.parse(self.RSS_URL)

            items = []
            for entry in feed.entries[:limit]:
                item = self._parse_entry(entry)
                if item:
                    items.append(item)

            logger.info(f"Fetched {len(items)} items from 36氪")
            return items

        except Exception as e:
            logger.error(f"Failed to fetch 36氪: {e}")
            return []

    def _parse_entry(self, entry) -> NewsItem:
        """解析 RSS 条目"""
        try:
            # 获取发布时间
            publish_time = ""
            if hasattr(entry, "published_parsed"):
                publish_time = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")

            # 获取简介
            summary = ""
            if hasattr(entry, "summary"):
                summary = self._clean_text(entry.summary)
            elif hasattr(entry, "description"):
                summary = self._clean_text(entry.description)

            return NewsItem(
                title=entry.get("title", ""),
                url=entry.get("link", ""),
                summary=summary[:200],
                source="36氪",
                publish_time=publish_time
            )

        except Exception as e:
            logger.warning(f"Failed to parse 36氪 entry: {e}")
            return None

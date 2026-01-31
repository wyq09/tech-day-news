"""Solidot 抓取器 - 使用 RSS"""
import logging
import feedparser
from typing import List
from datetime import datetime

from ..models import NewsItem
from .base import BaseFetcher, retry

logger = logging.getLogger(__name__)


class SolidotFetcher(BaseFetcher):
    """Solidot 抓取器

    使用 RSS: https://www.solidot.org/index.rss
    """

    FETCH_TYPE = "rss"
    RSS_URL = "https://www.solidot.org/index.rss"

    @retry(times=3)
    def fetch(self, limit: int = 20) -> List[NewsItem]:
        """抓取 Solidot 最新文章"""
        try:
            feed = feedparser.parse(self.RSS_URL)

            items = []
            for entry in feed.entries[:limit]:
                item = self._parse_entry(entry)
                if item:
                    items.append(item)

            logger.info(f"Fetched {len(items)} items from Solidot")
            return items

        except Exception as e:
            logger.error(f"Failed to fetch Solidot: {e}")
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
                source="Solidot",
                publish_time=publish_time
            )

        except Exception as e:
            logger.warning(f"Failed to parse Solidot entry: {e}")
            return None

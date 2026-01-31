"""Hacker News 抓取器 - 使用官方 API"""
import logging
import requests
from typing import List
from datetime import datetime

from ..models import NewsItem
from .base import BaseFetcher, retry

logger = logging.getLogger(__name__)


class HackerNewsFetcher(BaseFetcher):
    """Hacker News 抓取器

    使用官方 API: https://github.com/HackerNews/API
    """

    FETCH_TYPE = "api"
    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    @retry(times=3)
    def fetch(self, limit: int = 20) -> List[NewsItem]:
        """抓取 Hacker News Top Stories"""
        try:
            # 获取 top stories 的 ID 列表
            response = requests.get(
                f"{self.BASE_URL}/topstories.json",
                timeout=self.timeout
            )
            response.raise_for_status()
            story_ids = response.json()[:limit]

            items = []
            for story_id in story_ids:
                item = self._fetch_story(story_id)
                if item:
                    items.append(item)

            logger.info(f"Fetched {len(items)} items from Hacker News")
            return items

        except Exception as e:
            logger.error(f"Failed to fetch Hacker News: {e}")
            return []

    @retry(times=2)
    def _fetch_story(self, story_id: int) -> NewsItem:
        """获取单条资讯"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/item/{story_id}.json",
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            # 过滤掉没有 url 的条目（如 ask hn 等）
            if not data.get("url"):
                return None

            # 转换时间戳
            timestamp = data.get("time", 0)
            publish_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

            return NewsItem(
                title=data.get("title", ""),
                url=data.get("url", ""),
                summary=data.get("text", "")[:200] if data.get("text") else "",
                source="Hacker News",
                publish_time=publish_time
            )

        except Exception as e:
            logger.warning(f"Failed to fetch story {story_id}: {e}")
            return None

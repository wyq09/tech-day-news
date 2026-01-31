"""
文章数据结构
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    """文章数据结构"""
    title: str
    url: str
    summary: str
    source: str
    category: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_ai_related: bool = False

    def to_dict(self):
        """转换为字典"""
        return {
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "source": self.source,
            "category": self.category,
            "pub_date": self.pub_date.isoformat() if self.pub_date else None,
            "is_ai_related": self.is_ai_related
        }

"""数据模型定义"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NewsItem:
    """资讯条目"""
    title: str          # 标题
    url: str            # 原文链接
    summary: str        # 简介
    source: str         # 来源站点
    publish_time: Optional[str] = None  # 发布时间
    category: Optional[str] = None       # AI分类结果


@dataclass
class DailyArchive:
    """每日归档记录"""
    date: str           # 日期 YYYY-MM-DD
    file: str           # HTML 文件路径
    title: str          # 标题
    intro: str          # 导语


@dataclass
class ArchiveIndex:
    """归档索引"""
    archives: list[DailyArchive]
    updated_at: str  # ISO 格式时间戳

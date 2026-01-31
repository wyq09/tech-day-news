"""HTML 生成器 - 使用 Jinja2 模板"""
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import NewsItem, DailyArchive

logger = logging.getLogger(__name__)


class HTMLGenerator:
    """HTML 页面生成器"""

    def __init__(self, template_dir: str = None, output_dir: str = "."):
        """初始化生成器

        Args:
            template_dir: 模板目录路径
            output_dir: 输出目录路径
        """
        if template_dir is None:
            # 默认使用项目根目录下的 templates
            template_dir = Path(__file__).parent.parent / "templates"

        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)

        # 初始化 Jinja2 环境
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
        )

    def generate_daily(
        self,
        date: str,
        categorized: Dict[str, List[NewsItem]],
        intro: str
    ) -> str:
        """生成每日简报 HTML

        Args:
            date: 日期 (YYYY-MM-DD)
            categorized: 分类后的资讯字典
            intro: 导语

        Returns:
            str: 生成的 HTML 内容
        """
        try:
            template = self.env.get_template("daily.html")

            # 每个分类最多 5 条
            items_by_category = {
                cat: categorized.get(cat, [])[:5]
                for cat in ["今日热点", "技术趋势", "产品观察", "推荐阅读"]
            }

            html = template.render(
                date=date,
                date_display=datetime.strptime(date, "%Y-%m-%d").strftime("%Y年%m月%d日"),
                intro=intro,
                hot=items_by_category["今日热点"],
                tech=items_by_category["技术趋势"],
                product=items_by_category["产品观察"],
                reading=items_by_category["推荐阅读"],
            )

            logger.info(f"生成每日简报 HTML: {date}")
            return html

        except Exception as e:
            logger.error(f"生成每日简报失败: {e}")
            raise

    def save_daily(self, date: str, html: str) -> Path:
        """保存每日简报 HTML 到文件

        Args:
            date: 日期 (YYYY-MM-DD)
            html: HTML 内容

        Returns:
            Path: 保存的文件路径
        """
        try:
            # 解析年份
            year = datetime.strptime(date, "%Y-%m-%d").year

            # 创建年度目录
            year_dir = self.output_dir / str(year)
            year_dir.mkdir(parents=True, exist_ok=True)

            # 保存文件
            filename = f"news-{date}.html"
            filepath = year_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)

            logger.info(f"保存每日简报: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"保存每日简报失败: {e}")
            raise

    def generate_archive(self, archives: List[DailyArchive]) -> str:
        """生成归档页 HTML

        Args:
            archives: 归档记录列表

        Returns:
            str: 生成的 HTML 内容
        """
        try:
            template = self.env.get_template("archive.html")

            html = template.render(
                archives=archives,
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            )

            logger.info("生成归档页 HTML")
            return html

        except Exception as e:
            logger.error(f"生成归档页失败: {e}")
            raise

    def save_archive(self, html: str) -> Path:
        """保存归档页 HTML 到文件

        Args:
            html: HTML 内容

        Returns:
            Path: 保存的文件路径
        """
        try:
            filepath = self.output_dir / "archive.html"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)

            logger.info(f"保存归档页: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"保存归档页失败: {e}")
            raise

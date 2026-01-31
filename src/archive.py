"""归档索引管理器"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .models import DailyArchive, ArchiveIndex
from .generator import HTMLGenerator

logger = logging.getLogger(__name__)


class ArchiveManager:
    """归档管理器"""

    def __init__(self, data_dir: str = "data", output_dir: str = "."):
        """初始化归档管理器

        Args:
            data_dir: 数据目录路径
            output_dir: 输出目录路径
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.index_file = self.data_dir / "archive.json"
        self.generator = HTMLGenerator(output_dir=str(output_dir))

        # 确保数据目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_index(self) -> ArchiveIndex:
        """加载归档索引

        Returns:
            ArchiveIndex: 归档索引对象
        """
        if not self.index_file.exists():
            return ArchiveIndex(archives=[], updated_at="")

        try:
            with open(self.index_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return ArchiveIndex(
                    archives=[DailyArchive(**a) for a in data.get("archives", [])],
                    updated_at=data.get("updated_at", "")
                )
        except Exception as e:
            logger.error(f"加载归档索引失败: {e}")
            return ArchiveIndex(archives=[], updated_at="")

    def save_index(self, index: ArchiveIndex):
        """保存归档索引

        Args:
            index: 归档索引对象
        """
        try:
            data = {
                "archives": [
                    {
                        "date": a.date,
                        "file": a.file,
                        "title": a.title,
                        "intro": a.intro
                    }
                    for a in index.archives
                ],
                "updated_at": datetime.now().isoformat()
            }

            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"保存归档索引: {len(index.archives)} 条记录")

        except Exception as e:
            logger.error(f"保存归档索引失败: {e}")
            raise

    def add(self, date: str, intro: str, filepath: Path) -> DailyArchive:
        """添加新的归档记录

        Args:
            date: 日期 (YYYY-MM-DD)
            intro: 导语
            filepath: HTML 文件路径

        Returns:
            DailyArchive: 新创建的归档记录
        """
        index = self.load_index()

        # 检查是否已存在
        for archive in index.archives:
            if archive.date == date:
                logger.info(f"归档记录已存在: {date}")
                return archive

        # 计算相对路径
        rel_path = Path(filepath).relative_to(self.output_dir)

        # 创建新记录
        archive = DailyArchive(
            date=date,
            file=str(rel_path),
            title=f"科技日报 {date}",
            intro=intro[:100] + "..." if len(intro) > 100 else intro
        )

        # 添加到索引（按日期倒序）
        index.archives.insert(0, archive)

        # 保存索引
        self.save_index(index)

        logger.info(f"添加归档记录: {date}")
        return archive

    def get_all(self) -> List[DailyArchive]:
        """获取所有归档记录

        Returns:
            List[DailyArchive]: 归档记录列表（按日期倒序）
        """
        index = self.load_index()
        return index.archives

    def update_archive_page(self) -> Path:
        """更新归档页面

        Returns:
            Path: 归档页面文件路径
        """
        try:
            archives = self.get_all()
            html = self.generator.generate_archive(archives)
            filepath = self.generator.save_archive(html)
            logger.info("更新归档页面完成")
            return filepath

        except Exception as e:
            logger.error(f"更新归档页面失败: {e}")
            raise

    def add_and_update(self, date: str, intro: str, filepath: Path) -> Path:
        """添加归档记录并更新归档页面

        Args:
            date: 日期 (YYYY-MM-DD)
            intro: 导语
            filepath: HTML 文件路径

        Returns:
            Path: 归档页面文件路径
        """
        self.add(date, intro, filepath)
        return self.update_archive_page()

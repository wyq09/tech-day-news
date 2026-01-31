"""
HTML 生成器
"""
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
from src.config import CATEGORIES, OUTPUT_DIR, ARCHIVE_INDEX
from src.summarizer import generate_summary

class HTMLGenerator:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def generate_daily(self, date: datetime, categorized: dict) -> str:
        """生成日报页面"""
        # 准备数据
        date_str = date.strftime("%Y-%m-%d")
        year = date.strftime("%Y")

        # 生成导语
        summary = generate_summary(categorized, date)

        # 确保输出目录存在
        output_dir = OUTPUT_DIR.format(year=year)
        os.makedirs(output_dir, exist_ok=True)

        # 生成文件名
        filename = f"news-{date_str}.html"
        filepath = os.path.join(output_dir, filename)

        # 渲染模板
        template = self.env.get_template('daily.html.j2')
        html = template.render(
            date=date_str,
            summary=summary,
            categories=CATEGORIES,
            articles=categorized
        )

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ 日报已生成: {filepath}")
        return filepath

    def generate_archive(self, archive_data: list) -> str:
        """生成归档页面"""
        # 提取年份
        years = sorted(set(item['year'] for item in archive_data), reverse=True)

        # 按日期排序
        archive_data = sorted(archive_data, key=lambda x: x['date_str'], reverse=True)

        # 渲染模板
        template = self.env.get_template('archive.html.j2')
        html = template.render(
            archive=archive_data,
            years=years
        )

        # 写入文件
        with open(ARCHIVE_INDEX, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ 归档页已更新: {ARCHIVE_INDEX}")
        return ARCHIVE_INDEX

    def load_archive_data(self) -> list:
        """加载归档数据"""
        archive = []
        base_dir = "/home/ubuntu/www/tech-day-news"

        if not os.path.exists(base_dir):
            return archive

        # 遍历年份目录
        for year in os.listdir(base_dir):
            year_dir = os.path.join(base_dir, year)

            if not os.path.isdir(year_dir) or not year.isdigit():
                continue

            # 遍历HTML文件
            for filename in os.listdir(year_dir):
                if not filename.startswith('news-') or not filename.endswith('.html'):
                    continue

                # 解析文件名获取日期
                date_str = filename[5:-5]  # 去掉 'news-' 和 '.html'

                # 提取导语
                filepath = os.path.join(year_dir, filename)
                summary = self.extract_summary(filepath)

                archive.append({
                    'date': date_str,
                    'date_str': date_str,
                    'year': year,
                    'path': f"{year}/{filename}",
                    'summary': summary
                })

        return archive

    def extract_summary(self, filepath: str) -> str:
        """从HTML中提取导语"""
        try:
            from bs4 import BeautifulSoup

            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'lxml')

            summary_div = soup.find('div', class_='summary')
            if summary_div:
                return summary_div.get_text(strip=True)

        except Exception as e:
            print(f"  ✗ 无法提取导语: {e}")

        return "科技资讯日报"

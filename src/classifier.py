"""AI 分类器 - 使用智谱 API"""
import json
import logging
import os
from typing import List, Dict
from zhipuai import ZhipuAI

from .models import NewsItem

logger = logging.getLogger(__name__)

CATEGORIES = ["今日热点", "技术趋势", "产品观察", "推荐阅读"]


class ZhipuClassifier:
    """智谱 AI 分类器"""

    def __init__(self, api_key: str = None):
        """初始化分类器

        Args:
            api_key: 智谱 API Key，如不传则从环境变量 ZHIPU_API_KEY 读取
        """
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("智谱 API Key 未设置，请设置 ZHIPU_API_KEY 环境变量")

        self.client = ZhipuAI(api_key=self.api_key)

    def classify_items(self, items: List[NewsItem]) -> Dict[str, List[NewsItem]]:
        """批量分类资讯

        Args:
            items: 待分类的资讯列表

        Returns:
            Dict[str, List[NewsItem]]: 按分类分组的资讯字典
        """
        if not items:
            return {cat: [] for cat in CATEGORIES}

        logger.info(f"开始分类 {len(items)} 条资讯")

        # 构建分类请求
        items_text = self._format_items(items)

        prompt = f"""请将以下科技资讯分类到四个类别之一：

分类说明：
- 今日热点：行业重大新闻、突发热点、投融资、政策变化
- 技术趋势：技术发展、编程、架构、开源、开发工具
- 产品观察：AI 产品、硬件、软件发布、产品评测
- 推荐阅读：深度文章、有价值的长文、行业分析

请以 JSON 格式返回，每条资讯只需要返回其对应的 category。
JSON 格式示例：
[
  {{"index": 0, "category": "今日热点"}},
  {{"index": 1, "category": "技术趋势"}},
  ...
]

资讯列表：
{items_text}
"""

        try:
            response = self.client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "system", "content": "你是一个科技资讯分类助手，擅长将资讯准确分类。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )

            result = response.choices[0].message.content
            logger.info(f"智谱 API 响应: {result[:200]}...")

            # 解析 JSON 响应
            classifications = self._parse_classification(result)

            # 应用分类
            categorized = {cat: [] for cat in CATEGORIES}
            for i, item in enumerate(items):
                cat = classifications.get(i, "推荐阅读")  # 默认归入推荐阅读
                if cat in CATEGORIES:
                    item.category = cat
                    categorized[cat].append(item)
                else:
                    item.category = "推荐阅读"
                    categorized["推荐阅读"].append(item)

            # 打印分类统计
            for cat in CATEGORIES:
                logger.info(f"  {cat}: {len(categorized[cat])} 条")

            return categorized

        except Exception as e:
            logger.error(f"分类失败: {e}")
            # 失败时全部归入推荐阅读
            for item in items:
                item.category = "推荐阅读"
            return {cat: items if cat == "推荐阅读" else [] for cat in CATEGORIES}

    def generate_intro(self, categorized: Dict[str, List[NewsItem]], date: str) -> str:
        """生成今日导语

        Args:
            categorized: 分类后的资讯字典
            date: 日期

        Returns:
            str: 生成的导语
        """
        summary = self._format_summary(categorized, date)

        prompt = f"""基于今日抓取的科技资讯，生成一段 100-150 字的导语。

导语要求：
1. 简洁概括今日要点
2. 语气专业但不失活泼
3. 突出科技感和前瞻性
4. 字数控制在 100-150 字

今日资讯概览：
{summary}
"""

        try:
            response = self.client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "system", "content": "你是一个科技媒体编辑，擅长撰写简洁有力的导语。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )

            intro = response.choices[0].message.content.strip()
            logger.info(f"生成导语: {intro[:100]}...")
            return intro

        except Exception as e:
            logger.error(f"生成导语失败: {e}")
            # 返回默认导语
            total = sum(len(items) for items in categorized.values())
            return f"今日共收录 {total} 条科技资讯，涵盖热点、技术、产品等多个维度，带你快速了解行业动态。"

    def _format_items(self, items: List[NewsItem]) -> str:
        """格式化资讯列表用于提示词"""
        lines = []
        for i, item in enumerate(items):
            lines.append(f"{i}. 标题：{item.title}\n   来源：{item.source}\n   简介：{item.summary[:100]}")
        return "\n\n".join(lines)

    def _format_summary(self, categorized: Dict[str, List[NewsItem]], date: str) -> str:
        """格式化分类摘要用于导语生成"""
        lines = [f"日期：{date}\n"]
        for cat in CATEGORIES:
            items = categorized.get(cat, [])
            lines.append(f"\n{cat}（{len(items)}条）：")
            for item in items[:3]:  # 只取前3条
                lines.append(f"  - {item.title}")
        return "\n".join(lines)

    def _parse_classification(self, result: str) -> Dict[int, str]:
        """解析分类结果 JSON"""
        try:
            # 尝试直接解析
            data = json.loads(result)
            return {item["index"]: item["category"] for item in data}
        except json.JSONDecodeError:
            # 尝试提取 JSON 部分
            try:
                start = result.find("[")
                end = result.rfind("]") + 1
                if start >= 0 and end > start:
                    json_str = result[start:end]
                    data = json.loads(json_str)
                    return {item["index"]: item["category"] for item in data}
            except:
                pass

            logger.error(f"无法解析分类结果: {result}")
            return {}

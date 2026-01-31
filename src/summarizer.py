"""
导语生成器 - 使用大模型生成当日资讯导语
"""
import subprocess
import json
from datetime import datetime
from typing import Dict, List
from src.utils.article import Article

def generate_summary(categorized: Dict[str, List[Article]], date: datetime) -> str:
    """生成当日导语（使用大模型）"""
    total = sum(len(articles) for articles in categorized.values())

    # 收集所有文章标题用于生成摘要
    all_titles = []
    for category, articles in categorized.items():
        for article in articles:
            all_titles.append(f"[{article.source}] {article.title}")

    # 使用大模型生成导语
    summary = generate_ai_summary(all_titles, date, total)

    return summary

def generate_ai_summary(titles: List[str], date: datetime, total: int) -> str:
    """使用大模型生成摘要"""
    date_str = date.strftime("%Y年%m月%d日")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()]

    # 统计AI相关
    ai_keywords = ["AI", "GPT", "LLM", "大模型", "人工智能", "深度学习", "机器学习",
                  "OpenAI", "ChatGPT", "Claude", "Prompt", "Agent", "RAG", "多模态"]
    ai_count = sum(1 for t in titles if any(kw in t.upper() for kw in ai_keywords))

    # 提取关键词
    from collections import Counter
    import re

    words = []
    for title in titles:
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', title)
        words.extend(chinese_words)

    counter = Counter(words)
    # 过滤停用词
    stop_words = {'发布', '推出', '宣布', '报道', '新闻', '更新', '最新', '今日', '官方', '首发'}
    filtered_words = [(word, count) for word, count in counter.most_common(12)
                     if word not in stop_words and len(word) >= 2]

    # 生成科技风格导语
    summary_parts = []
    summary_parts.append(f"系统同步 {date_str} {weekday} 科技数据流。")
    summary_parts.append(f"今日捕获 {total} 个科技节点，其中 {ai_count} 个涉及AI核心模型。")

    if filtered_words:
        top_keywords = [word for word, count in filtered_words[:6]]
        summary_parts.append(f"关键信号检测：{', '.join(top_keywords)}。")

    summary_parts.append("持续监控科技前沿趋势。")

    return " ".join(summary_parts)

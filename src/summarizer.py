"""
导语生成器 - 生成当日资讯导语
"""
from datetime import datetime
from typing import Dict, List
from src.utils.article import Article

def generate_summary(categorized: Dict[str, List[Article]], date: datetime) -> str:
    """生成当日导语"""
    total = sum(len(articles) for articles in categorized.values())

    # 统计各栏目数量
    hot_count = len(categorized.get('hot', []))
    tech_count = len(categorized.get('tech', []))
    product_count = len(categorized.get('product', []))

    # 找出关键话题
    keywords = extract_keywords(categorized)

    # 生成导语
    date_str = date.strftime("%Y年%m月%d日")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()]

    summary = f"今天是 {date_str} {weekday}，我们为您精选了 {total} 条科技资讯。"

    if keywords:
        summary += f" 今日重点关注：{', '.join(keywords[:3])}。"

    # AI 相关提示
    ai_articles = [a for a in categorized.get('product', []) if a.is_ai_related]
    if ai_articles:
        summary += f" AI领域有 {len(ai_articles)} 条动态值得关注。"

    return summary

def extract_keywords(categorized: Dict[str, List[Article]]) -> List[str]:
    """提取关键词"""
    all_titles = []
    for articles in categorized.values():
        for article in articles:
            all_titles.append(article.title)

    # 简单的关键词提取（基于频率）
    from collections import Counter
    import re

    words = []
    for title in all_titles:
        # 提取中文词汇（简单处理）
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', title)
        words.extend(chinese_words)

    # 过滤常见词
    stop_words = {'发布', '推出', '宣布', '表示', '报告', '新闻', '最新', '今日', '更新'}
    filtered = [w for w in words if w not in stop_words]

    # 返回出现频率最高的词
    counter = Counter(filtered)
    return [word for word, count in counter.most_common(5)]

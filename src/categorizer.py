"""
智能分类器 - 将文章归类到不同栏目
"""
import re
from typing import List, Dict
from src.utils.article import Article
from src.config import CATEGORIES, AI_KEYWORDS

def categorize_articles(articles: List[Article]) -> Dict[str, List[Article]]:
    """将文章分类到各个栏目"""
    categorized = {cat: [] for cat in CATEGORIES.keys()}

    # 先标记 AI 相关文章
    mark_ai_articles(articles)

    # 按关键词分类
    for article in articles:
        # AI 相关优先归到产品观察
        if article.is_ai_related and article.category != 'product':
            article.category = 'product'

        # 如果还没有分类，按关键词匹配
        if not article.category:
            category = match_category(article.title + " " + article.summary)
            if category:
                article.category = category

        # 归类
        if article.category and article.category in categorized:
            categorized[article.category].append(article)

    # 按优先级补充数量不足的栏目
    fill_categories(categorized, articles)

    return categorized

def mark_ai_articles(articles: List[Article]) -> None:
    """标记 AI 相关文章"""
    for article in articles:
        text = (article.title + " " + article.summary).lower()
        for keyword in AI_KEYWORDS:
            if keyword.lower() in text:
                article.is_ai_related = True
                break

def match_category(text: str) -> str:
    """根据关键词匹配栏目"""
    text = text.lower()

    for cat_id, config in CATEGORIES.items():
        for keyword in config['keywords']:
            if keyword.lower() in text:
                return cat_id

    return None

def fill_categories(categorized: Dict[str, List[Article]], all_articles: List[Article]) -> None:
    """补充数量不足的栏目"""
    for cat_id, articles in categorized.items():
        config = CATEGORIES[cat_id]
        needed = config['max_items'] - len(articles)

        if needed <= 0:
            continue

        # 找出未分配的文章
        used_articles = set()
        for arts in categorized.values():
            for art in arts:
                used_articles.add(art.url)

        # 按优先级补充
        for article in all_articles:
            if len(articles) >= config['max_items']:
                break

            if article.url not in used_articles:
                articles.append(article)
                used_articles.add(article.url)

    # 限制每个栏目最大数量
    for cat_id in categorized:
        max_items = CATEGORIES[cat_id]['max_items']
        categorized[cat_id] = categorized[cat_id][:max_items]

# 科技日报 (Tech Day News) 设计文档

**日期**: 2026-01-31
**状态**: 设计完成

## 概述

一个自动化科技资讯抓取工具，每日从多个科技媒体站点抓取最新资讯，通过 AI 分类整理成结构化的每日简报网页。

## 核心功能

1. **多站点资讯抓取** - V2EX、Hacker News、36氪、少数派、虎嗅、InfoQ、开源中国、Solidot
2. **AI 智能分类** - 使用智谱 API 将资讯分为：今日热点、技术趋势、产品观察、推荐阅读
3. **自动生成导语** - AI 汇总生成当日内容导语
4. **静态网页输出** - 生成未来主义风格的每日简报 HTML 页面
5. **归档索引** - 维护历史简报索引，支持按时间浏览

## 项目结构

```
tech-day-news/
├── .github/
│   └── workflows/
│       └── daily-news.yml       # GitHub Actions 定时任务
├── src/
│   ├── fetchers/                 # 各站点抓取器
│   │   ├── base.py              # 基础抓取器类
│   │   ├── v2ex.py              # V2EX
│   │   ├── hackernews.py        # Hacker News (API)
│   │   ├── kr36.py              # 36氪 (RSS)
│   │   ├── sspai.py             # 少数派 (RSS)
│   │   ├── huxiu.py             # 虎嗅
│   │   ├── infoq.py             # InfoQ
│   │   ├── oschina.py           # 开源中国
│   │   └── solidot.py           # Solidot
│   ├── classifier.py             # AI 分类器（智谱）
│   ├── generator.py              # HTML 生成器
│   ├── archive.py                # 归档索引管理
│   ├── models.py                 # 数据模型定义
│   └── main.py                   # 主入口
├── templates/
│   ├── daily.html                # 每日简报模板
│   └── archive.html              # 归档页模板
├── data/
│   └── archive.json              # 归档索引
├── static/
│   └── styles.css                # 自定义样式（未来主义）
├── {年}/                         # 生成的年度简报目录
├── logs/                         # 运行日志
├── requirements.txt
└── README.md
```

## 数据流程

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Actions 触发                       │
│                    (每日 7:00 UTC+8 或手动)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      各站点抓取器 (RSS/API/爬虫)                  │
│  V2EX │ Hacker News │ 36氪 │ 少数派 │ 虎嗅 │ InfoQ │ 开源中国    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据清洗与去重                              │
│            (去除重复项、过滤无效内容、提取关键字)                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI 分类 + 导语生成 (智谱 API)                  │
│   今日热点 │ 技术趋势 │ 产品观察 │ 推荐阅读 │ AI 导语             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      生成 HTML 页面                               │
│            (每日简报页 + 更新归档索引 + 提交到 Git)               │
└─────────────────────────────────────────────────────────────────┘
```

## 技术实现

### 1. 抓取器设计

**优先级**: RSS > API > HTML 爬虫

```python
class BaseFetcher(ABC):
    @abstractmethod
    def fetch(self) -> List[NewsItem]:
        """抓取资讯，返回统一格式的 NewsItem 列表"""
        pass

    def _retry(self, func, times: int = 3):
        """重试机制"""
```

**站点配置**:
- **Hacker News**: 官方 API
- **36氪**: RSS
- **少数派**: RSS
- **V2EX**: RSS
- **其他站点**: 优先 RSS，无 RSS 则爬虫

**统一数据格式**:
```python
@dataclass
class NewsItem:
    title: str      # 标题
    url: str        # 原文链接
    summary: str    # 简介
    source: str     # 来源站点
    publish_time: str  # 发布时间
```

### 2. AI 分类器（智谱 API）

```python
class ZhipuClassifier:
    CATEGORIES = ["今日热点", "技术趋势", "产品观察", "推荐阅读"]

    def classify_items(self, items: List[NewsItem]) -> Dict[str, List[NewsItem]]:
        """批量分类，返回按分类分组的资讯"""

    def generate_intro(self, categorized: Dict[str, List[NewsItem]]) -> str:
        """生成今日导语"""
```

**分类规则**:
- 今日热点：行业重大新闻、突发热点
- 技术趋势：技术发展、编程、架构、开源
- 产品观察：AI 产品、硬件、软件发布
- 推荐阅读：深度文章、有价值的长文

### 3. HTML 生成器

```python
class HTMLGenerator:
    def generate_daily(self, date: str, categorized: Dict, intro: str) -> str:
        """生成每日简报 HTML"""

    def generate_archive(self, archives: List) -> str:
        """生成归档页 HTML"""
```

**模板引擎**: Jinja2
**样式框架**: Tailwind CSS + 自定义 CSS

### 4. 归档索引管理

**archive.json 结构**:
```json
{
  "archives": [
    {
      "date": "2026-01-31",
      "file": "2026/news-2026-01-31.html",
      "title": "科技日报 2026-01-31",
      "intro": "今日 AI 领域迎来重大突破..."
    }
  ],
  "updated_at": "2026-01-31T07:00:00Z"
}
```

### 5. GitHub Actions 配置

**触发方式**:
- 定时: 每天 UTC 23:00 (北京时间 07:00)
- 手动: workflow_dispatch

**环境变量**:
- `ZHIPU_API_KEY`: GitHub Secrets

**工作流程**:
1. Checkout 代码
2. 安装 Python 依赖
3. 运行抓取器 → 分类 → 生成页面
4. Git commit 并 push

## UI 设计风格

**主题**: 未来主义、速度、动态、科技崇拜

**设计元素**:
- 动态线条：CSS 渐变 + 动画
- 重叠形式：绝对定位 + z-index
- 激进排版：大字号 + 粗体对比
- 深色背景 + 霓虹配色

## 错误处理

1. **抓取失败**: 记录日志 + 重试 3 次
2. **API 失败**: 记录日志 + 跳过该站点
3. **分类失败**: 使用默认分类规则

## 文件命名规范

- 每日简报: `{年}/news-{YYYY-MM-DD}.html`
- 归档页: `archive.html`
- 年度目录: `{YYYY}/`

## 待确认事项

- [ ] 智谱 API Key 配置
- [ ] 各站点 RSS/API 地址确认
- [ ] UI 样式细节确认

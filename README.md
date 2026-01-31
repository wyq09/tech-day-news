# 科技日报 (Tech Day News)

> 每日自动抓取科技资讯，生成结构化简报网页

## 功能特点

- **多站点抓取**: V2EX、Hacker News、36氪、少数派、虎嗅、InfoQ、开源中国、Solidot
- **AI 智能分类**: 使用智谱 AI 自动分类为：今日热点、技术趋势、产品观察、推荐阅读
- **自动导语**: AI 汇总生成当日内容导语
- **未来主义 UI**: 动态线条、霓虹效果、科技风格
- **归档索引**: 按时间浏览历史简报

## 本地运行

### 环境要求

- Python 3.11+
- 智谱 AI API Key

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置 API Key

设置环境变量 `ZHIPU_API_KEY`：

```bash
export ZHIPU_API_KEY="your_api_key_here"
```

### 运行

```bash
python src/main.py
```

生成的文件：
- 每日简报: `{年}/news-{YYYY-MM-DD}.html`
- 归档页: `archive.html`
- 归档索引: `data/archive.json`

## GitHub Actions

1. 在 GitHub 仓库设置中添加 Secret: `ZHIPU_API_KEY`
2. 推送代码后，每天 07:00 (北京时间) 自动运行
3. 也可在 Actions 页面手动触发

## 项目结构

```
tech-day-news/
├── src/
│   ├── fetchers/         # 各站点抓取器
│   ├── classifier.py     # AI 分类器
│   ├── generator.py      # HTML 生成器
│   ├── archive.py        # 归档管理器
│   └── main.py           # 主入口
├── templates/            # HTML 模板
├── data/                 # 归档索引
├── logs/                 # 运行日志
└── {年}/                 # 生成的简报
```

## 数据来源

- V2EX: https://www.v2ex.com/index.xml
- Hacker News: Official API
- 36氪: https://36kr.com/feed
- 少数派: https://sspai.com/feed
- 虎嗅: https://www.huxiu.com/rss/0.xml
- InfoQ: https://www.infoq.cn/feed
- 开源中国: https://www.oschina.net/news/rss
- Solidot: https://www.solidot.org/index.rss

## License

MIT

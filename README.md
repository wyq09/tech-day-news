# 科技日报 - 每日科技资讯简报

自动化抓取和整理科技资讯的每日简报系统。

## 访问地址

- **归档主页**: https://aiform.youyongai.com/tech-day-news/
- **今日日报**: https://aiform.youyongai.com/tech-day-news/2026/news-2026-01-31.html

## 功能特性

### 自动抓取
- V2EX
- Hacker News Top
- 36氪
- 少数派
- 虎嗅
- InfoQ
- 开源中国
- Solidot

### 智能分类
- **今日热点**: 关注热点资讯
- **技术趋势**: 关注技术相关资讯
- **产品观察**: 关注科技产品（AI人工智能优先）
- **推荐阅读**: 深度分析和有价值的内容

### 每日简报
每个栏目包含 3-5 条精选资讯，每条包含：
- 标题（可点击跳转原文）
- 来源
- 简介
- AI 标签（AI相关文章）

### 归档系统
- 按年份归档
- 时间筛选
- 一键访问历史日报

## 技术栈

- Python 3.12
- BeautifulSoup4 (HTML解析)
- Feedparser (RSS订阅)
- Jinja2 (模板引擎)
- Nginx (静态文件服务)

## 目录结构

```
tech-day-news/
├── src/
│   ├── config.py           # 配置文件
│   ├── main.py             # 主程序
│   ├── generator.py        # HTML生成器
│   ├── categorizer.py      # 分类器
│   ├── summarizer.py       # 导语生成
│   ├── scrapers/           # 爬虫模块
│   │   ├── rss_fetcher.py  # RSS抓取
│   │   └── web_fetcher.py  # Web抓取
│   └── utils/              # 工具模块
│       └── article.py      # 文章数据结构
├── templates/              # HTML模板
│   ├── daily.html.j2       # 日报模板
│   └── archive.html.j2     # 归档模板
├── 2026/                   # 2026年日报
│   └── news-2026-01-31.html
├── index.html              # 归档主页
├── run_daily.sh            # 每日运行脚本
└── requirements.txt        # Python依赖
```

## 使用方法

### 手动运行

```bash
cd /home/ubuntu/www/tech-day-news
python3 src/main.py
```

### 定时任务

已设置 cron，每天早上 8:00 自动运行：

```bash
crontab -l
```

### 自定义运行时间

编辑 crontab：

```bash
crontab -e
```

## 部署说明

### Nginx 配置

Nginx 已配置为服务静态文件：

```nginx
server {
    server_name aiform.youyongai.com;
    root /home/ubuntu/www;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # SSL 配置
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/aiform.youyongai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/aiform.youyongai.com/privkey.pem;
}
```

### 权限设置

```bash
sudo chown -R www-data:www-data /home/ubuntu/www/tech-day-news/
```

## 日志查看

```bash
# 查看运行日志
tail -f /home/ubuntu/www/tech-day-news/cron.log

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 扩展开发

### 添加新的资讯源

编辑 `src/config.py`，在 `RSS_SOURCES` 或 `WEB_SOURCES` 中添加新源。

### 调整分类规则

编辑 `src/config.py` 中的 `CATEGORIES` 和 `AI_KEYWORDS`。

### 自定义模板

编辑 `templates/` 目录下的 Jinja2 模板。

## Git 仓库

- 仓库地址: git@github.com:wyq09/tech-day-news.git
- 本地目录: /home/ubuntu/www/tech-day-news

每次运行后会自动提交并推送到 GitHub。

## 问题排查

### 抓取失败
检查网络连接，某些源可能需要代理或超时调整。

### 分类不准确
调整 `src/config.py` 中的关键词列表。

### 页面 404
检查 Nginx 配置和文件权限。

---

**生成时间**: 2026-01-31
**版本**: v1.0
**作者**: 小龙虾 🦞

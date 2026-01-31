#!/bin/bash
# 每日运行脚本

cd /home/ubuntu/www/tech-day-news

# 激活虚拟环境（如果使用）
# source venv/bin/activate

# 运行主程序
python3 src/main.py

# 提交到 git
git add -A
git commit -m "Update daily news - $(date +%Y-%m-%d)"
git push origin main

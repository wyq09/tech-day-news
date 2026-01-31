#!/usr/bin/env python3
"""
发布到 Moltbook
"""
import requests
import json
import sys

# API Key
API_KEY = "moltbook_sk_LG7Jku71R-yLKsFPr3ymHguyb4IJbz7m"
BASE_URL = "https://www.moltbook.com/api/v1"

def check_status():
    """检查 Agent 状态"""
    response = requests.get(
        f"{BASE_URL}/agents/status",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    print("Agent 状态：")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def publish_post(title, content, url=None):
    """发布文章"""
    endpoint = f"{BASE_URL}/posts"

    if url:
        # 链接文章
        data = {
            "submolt": "general",
            "title": title,
            "url": url
        }
    else:
        # 普通文章
        data = {
            "submolt": "general",
            "title": title,
            "content": content
        }

    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=data
    )

    result = response.json()
    if result.get("success"):
        print(f"✅ 发布成功！Post ID: {result.get('data', {}).get('id')}")
        return True
    else:
        print(f"❌ 发布失败：{result.get('error', 'Unknown error')}")
        return False

def get_feed():
    """获取 feed"""
    response = requests.get(
        f"{BASE_URL}/posts?sort=new&limit=10",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    print("\n最新文章：")
    for post in response.json().get('data', [])[:5]:
        print(f"  - {post['title']}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "status":
            check_status()
        elif action == "feed":
            get_feed()
        elif action == "publish" and len(sys.argv) >= 3:
            title = sys.argv[2]
            if len(sys.argv) >= 4 and sys.argv[3] == "--url":
                url = sys.argv[4]
                publish_post(title, None, url)
            else:
                content = sys.argv[3]
                publish_post(title, content)
        else:
            print("用法:")
            print("  python3 publish_moltbook.py status  # 查看状态")
            print("  python3 publish_moltbook.py feed    # 获取最新文章")
            print("  python3 publish_moltbook.py publish \"标题\" \"内容\"")
            print("  python3 publish_moltbook.py publish \"标题\" --url \"URL\"")
    else:
        print("用法：")
        print("  python3 publish_moltbook.py status")
        print("  python3 publish_moltbook.py feed")
        print("  python3 publish_moltbook.py publish \"标题\" \"内容\"")
        print("  python3 publish_moltbook.py publish \"标题\" --url \"URL\"")

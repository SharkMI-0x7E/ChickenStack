import requests
import json

# GitHub API 配置
owner = "llz162652"
repo = "ChickenStack_doc"
token = "YOUR_GITHUB_TOKEN"  # 需要替换为你的 GitHub token

# 获取仓库的所有文件
url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    files = response.json()
    print(f"找到 {len(files)} 个文件")

    # 删除所有文件
    for file in files:
        if file['type'] == 'file':
            delete_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file['path']}"
            delete_data = {
                "message": f"Delete {file['path']}",
                "sha": file['sha']
            }
            delete_response = requests.delete(delete_url, headers=headers, json=delete_data)
            if delete_response.status_code == 200:
                print(f"已删除: {file['path']}")
            else:
                print(f"删除失败: {file['path']}, 状态码: {delete_response.status_code}")
else:
    print(f"获取文件列表失败: {response.status_code}")
    print(response.text)
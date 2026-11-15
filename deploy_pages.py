#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通过 GitHub Git Data API 提交整站文件并触发 Pages 重建。

本地 git 在非交互环境下可能因凭证助手/传输问题失败
（`fetch-pack: invalid index-pack output`），此脚本走 REST API，
绕开本地 git，只依赖已登录的 gh CLI（`gh auth login`）。

用法：
    python deploy_pages.py                 # 使用默认提交说明
    python deploy_pages.py -m "说明文本"    # 追加自定义说明
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

REPO = "EasonQuantico/EasonQuantico"
BRANCH = "main"
HERE = os.path.dirname(os.path.abspath(__file__))

TOKEN = subprocess.check_output(["gh", "auth", "token"], text=True).strip()

# (本地文件, 仓库内路径)
FILES = [
    ("index.html", "index.html"),
    ("README.md", "README.md"),
    ("匡烨-个人主页-单文件版.html", "standalone.html"),
    ("deploy_pages.py", "deploy_pages.py"),
]

DEFAULT_MSG = (
    "更新个人主页\n\n"
    "- index.html：主页面\n"
    "- standalone.html：单文件离线版（资源 base64 内联）\n"
    "- README.md / deploy_pages.py：文档与部署脚本"
)


def api(method, path, payload=None):
    url = "https://api.github.com" + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise SystemExit("HTTP %s on %s %s\n%s" % (e.code, method, path, body[:800]))


def blob_sha(path):
    with open(os.path.join(HERE, path), "rb") as f:
        content = base64.b64encode(f.read()).decode()
    return api("POST", "/repos/%s/git/blobs" % REPO,
               {"content": content, "encoding": "base64"})["sha"]


def main():
    msg = DEFAULT_MSG
    if "-m" in sys.argv:
        msg = sys.argv[sys.argv.index("-m") + 1]

    ref = api("GET", "/repos/%s/git/ref/heads/%s" % (REPO, BRANCH))
    head = ref["object"]["sha"]
    base_tree = api("GET", "/repos/%s/git/commits/%s" % (REPO, head))["tree"]["sha"]
    print("head %s  tree %s" % (head[:8], base_tree[:8]))

    tree = []
    for local, remote in FILES:
        sha = blob_sha(local)
        size = os.path.getsize(os.path.join(HERE, local))
        tree.append({"path": remote, "mode": "100644", "type": "blob", "sha": sha})
        print("  %-14s %s  %7.1f KB" % (remote, sha[:8], size / 1024))

    new_tree = api("POST", "/repos/%s/git/trees" % REPO,
                   {"base_tree": base_tree, "tree": tree})
    commit = api("POST", "/repos/%s/git/commits" % REPO, {
        "message": msg,
        "tree": new_tree["sha"],
        "parents": [head],
        "author": {"name": "EasonQuantico", "email": "3473357872@qq.com"},
        "committer": {"name": "EasonQuantico", "email": "3473357872@qq.com"},
    })
    print("commit %s" % commit["sha"][:8])
    api("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH),
        {"sha": commit["sha"], "force": False})
    print("ref -> %s" % commit["html_url"])


if __name__ == "__main__":
    main()

# 个人主页 · 科幻风格个人档案站点

一个零依赖、单仓库部署的个人主页与线上简历系统。深色科幻视觉 + 访问门禁 + 云端同步的分享动态 + 浏览器内内容管理后台。

**在线地址**

- 主站（完整功能）：<https://kuangye-homepage.app.workbuddy.host/>
- GitHub Pages 镜像：<https://easonquantico.github.io/EasonQuantico/>
- 单文件离线版：<https://easonquantico.github.io/EasonQuantico/standalone.html>

---

## 功能总览

| 模块 | 说明 |
|---|---|
| 访问门禁 | 全屏终端风验证页，SHA-256 前端校验，会话内免重复输入，支持长期免输 |
| Hero 首屏 | AI 生成无缝循环视频背景 + 玻璃拟态文案层 + 八边形裁切头像 |
| 能力矩阵 | 6 张技能卡片 + 主干课程标签云 |
| 项目档案 | 实习经历 + 嵌入式 / 光电 / AI 方向项目卡片 |
| 荣誉认证 | 竞赛奖项与可查证成果 |
| 分享动态 | 卡片堆叠交互（顶卡飞出 / 箭头翻页 / 计数指示），数据存云端，全站可见 |
| 媒体上传 | 后台可为分享卡片配图片（≤6MB）或视频（≤24MB），以 data URI 存云端，访客端卡片内嵌渲染 |
| 管理后台 | 页脚入口 → 独立密码验证 → 抽屉式控制台，支持新增 / 编辑 / 删除 / 置顶 / JSON 导入导出 |
| 简历下载 | 页面内直接打开最新版 PDF 简历 |

## 技术栈

- **前端**：原生 HTML / CSS / JavaScript，单文件实现，零框架、零构建
- **背景视频**：AI 视频模型生成 → ffmpeg 裁剪水印（底部 100px）→ 与亮度渐变同步的 CSS 遮罩动画消除循环接缝
- **云端**：WorkBuddy Cloud Service（PostgreSQL + 行级安全 RLS + Origin 校验），前端经 CDN SDK 读写
- **部署**：WorkBuddy Sites（主站，云同步完整生效）+ GitHub Pages（代码镜像，云端不可达时自动降级）
- **字体**：系统字体栈 + 等宽字体做 HUD 标签

## 目录结构

```
├── index.html                      # 主页面（所有样式、脚本、结构均在此文件内）
├── standalone.html                 # 单文件离线版（视频/图片/PDF 全部 base64 内联，约 4.1MB）
├── hero-loop.mp4                   # 首屏背景循环视频（1920×980，约 2.6MB）
├── photo.jpg                       # 证件照
├── gate-logo.png                   # 门禁页标识图
├── 匡烨-简历.pdf                    # 最新版简历（单页 A4）
└── README.md
```

## 数据架构

分享动态使用云端数据库表 `share_posts`：

```
id BIGINT PK | tag | date | title | body | link | link_text | media_data | media_kind | sort_order | created_at
```

- **RLS 策略**：匿名可读可写（SELECT/INSERT/UPDATE/DELETE 全放行），配合数据面 **Origin 强制校验**限制写入来源——仅应用注册域名可通过，GitHub Pages 等外部来源的请求会被拒绝
- **前端数据流**：优先云端拉取 → 云端不可达时显示 `OFFLINE · 本地模式`，回退 localStorage / 内置默认数据；云端空表时自动播种默认内容
- **写入路径**：管理后台的所有增删改直接写云端，刷新即全网可见
- **媒体存储**：`media_data` 存完整 data URI（`data:image/*` 或 `data:video/*` 的 base64），`media_kind` 标记渲染方式。选择存库而非对象存储的原因：WorkBuddy Storage 仅对登录用户开放且无公开 URL，而分享媒体需要匿名可见；data URI 复用现有公开读通道，且 GitHub 镜像站也能加载。限制：图片 ≤6MB、视频 ≤24MB（前端校验），本地缓存超配额时自动剥离媒体重试

## 安全模型（如实说明）

- 两道密码（进站门禁 / 管理后台）**互相独立**，源码中只存 SHA-256 哈希 + djb2 兜底哈希，**无任何明文**
- 密码验证在前端完成，验证通过后写入 sessionStorage（会话级）
- **已知局限**（均为静态站点的物理边界，非实现缺陷）：
  1. 前端哈希校验可被懂行者绕过（关闭 JS、直接调用接口）；Origin 校验依赖请求头，非密码学鉴权
  2. 短密码的哈希可被暴力还原——建议使用长密码，或迁移到服务端鉴权
  3. 门禁页logo 为视觉设计的一部分，访客可见

## 更新流程

修改内容后需同步三个发布面：

1. **改 `index.html`**（源文件，一切改动从这里开始）
2. **重建单文件版**：运行内联构建脚本（资源 base64 化 + PDF 链接改写为运行时 Blob）
3. **重新部署 WorkBuddy 站点**（主站）并 **push GitHub**（Pages 自动重建）

## QA 方法

- headless Chrome（`--dump-dom` + 注入测试脚本）走**真实 UI 路径**：点击按钮 → 填写表单 → 触发 submit → 断言 DOM 状态
- 多断点视觉验证：桌面 / 平板 / 390px 手机（注意：headless Chrome 窗口宽度下限约 500px，真机小屏需 iframe 外壳模拟）
- 云端回路验证：线上「插入 → 读回 → 删除」完整闭环，测试数据用后即删
- 密码泄露扫描：全仓库大小写不敏感扫描明文，甄别 base64 随机子串误报

## 相关仓库

- [EasonQuantico/EasonQuantico](https://github.com/EasonQuantico/EasonQuantico) — 本站点代码

---

© 2026 匡烨 · Built with AI-assisted workflow

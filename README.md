# 个人主页 · Scuderia 赛道终端

一个零依赖、单仓库部署的个人主页与线上简历系统。视觉取意 F1 车队（法拉利红 × 碳纤黑 × 遥测仪表盘）+ 终端/ASCII 排版语言；功能保留访问门禁、云端同步的分享动态与浏览器内管理后台。

**在线地址**

- 主站（完整功能）：<https://kuangye-homepage.app.workbuddy.host/>
- GitHub Pages 镜像：<https://easonquantico.github.io/EasonQuantico/>
- 单文件离线版：<https://easonquantico.github.io/EasonQuantico/standalone.html>

---

## 功能总览

| 模块 | 说明 |
|---|---|
| 访问门禁 | 全屏发车格验证页（五灯起步动效），SHA-256 前端校验，会话内免重复输入，支持 7 天免输 |
| 首页 HERO | 法拉利红主视觉 + 速度流光 + **F1 赛道模拟器**（Canvas 内置小游戏，实时驱动下方遥测：速度 / 挡位 / RPM / 油门 / 刹车 / 三段计时） |
| 分区导航 | 01 首页 / 02 个人简介 / 03 作品展示 / 04 联系方式；滚动自动高亮 + 顶部赛道进度条 |
| 能力矩阵 | 6 张技能卡片 + 主干课程标签云 |
| 作品展示 | 实习经历 + 嵌入式 / 光电 / AI 方向项目条目（P1–P5 计时塔式排布 + 幽灵序号水印） |
| 荣誉认证 | 竞赛奖项与可查证成果 |
| 分享动态 | 卡片堆叠交互（顶卡飞出 / 箭头翻页 / 计数指示），数据存云端，全站可见 |
| 媒体上传 | 后台可为分享卡片配图片（≤6MB）或视频（≤24MB），以 data URI 存云端，访客端卡片内嵌渲染 |
| 管理后台 | 页脚入口 → 独立密码验证 → 抽屉式控制台，支持新增 / 编辑 / 删除 / 置顶 / JSON 导入导出 |
| 简历下载 | 页面内直接打开最新版 PDF 简历 |

## F1 赛道模拟器

首页右侧面板里的内置小游戏：俯角 60° 的「车顶朝前」跟随相机，随机赛道无限循环。

- **赛道生成**：随机星形多边形 → 每条边保留为直道、每个顶点按随机圆弧倒角成弯道 → 弧长均匀重采样。单圈 1.5–2.0 km，8–12 个弯道，弯道半径 27–500 m，直道占比约 40%；每完成一圈即刻换一条新赛道
- **玩法**：`←` `→` 转向，`↑` 加速，`↓` 制动；松手自动循迹行驶（部分抵消离心力 + 缓慢回中）。速度越快离心外抛越强，压路肩/护栏会掉速并闪光震动
- **相机**：针孔透视投影，相机位于车顶上方、朝车头方向俯视 60°，可视距离约 100 m；路面、路肩、护栏立柱、起跑格、小地图全部逐帧重绘
- **控制**：`Play` / `Quit` 按钮进出入；运行中方向键被 `preventDefault` 接管，不会滚动页面，退出后页面滚动恢复。画面离开视口、切换标签页或窗口失焦自动暂停（`Resume` 继续）
- **性能**：仅在运行中跑 `requestAnimationFrame`，暂停即停；画布按 devicePixelRatio 缩放并限制 DPR ≤ 2；单帧约 40 个路面采样点、200 次投影

## 技术栈

- **前端**：原生 HTML / CSS / JavaScript，单文件实现，零框架、零构建
- **视觉资产**：无背景视频、无位图纹理；赛道模拟器为 Canvas 2D 矢量绘制（透视投影 + 程序化赛道），其余全部由 CSS 渐变/遮罩绘制
- **分享卡片媒体**：卡片为固定宽高比（桌面 1.34、≤680px 0.82、≤380px 0.74），媒体区占满剩余高度，图片/视频以 `object-fit:contain` 整幅等比呈现——不裁切、不变形、卡片内不出现滚动条；左右留白用同图模糊衬底补齐，无配图的卡片改为刻度网格 + 幽灵序号
- **主题色**：`#e10600`（Rosso）/ `#070506`（碳纤黑）/ `#f6f0ea`（暖白），等宽字体承担 HUD 标签与数字
- **云端**：WorkBuddy Cloud Service（PostgreSQL + 行级安全 RLS + Origin 校验），前端经 CDN SDK 读写
- **部署**：GitHub Pages（`main` 分支根目录，提交后自动重建）+ WorkBuddy Cloud Service（分享动态的云端数据，不可达时前端自动降级为本地模式）
- **字体**：系统字体栈（含思源/苹方/雅黑回退）+ 等宽字体栈（JetBrains Mono → Cascadia → Consolas），零 Web Font 请求
- **无障碍**：`prefers-reduced-motion` 下关闭动效并保留首帧（游戏可玩，仅关闭屏幕震动与撞击闪光）；按钮与画布均有可读标签，正文语义结构完整

## 目录结构

```
├── index.html                      # 主页面（所有样式、脚本、结构均在此文件内）
├── 匡烨-个人主页-单文件版.html      # 单文件离线版（照片/PDF 全部 base64 内联，约 2.0MB）
├── photo.jpg                       # 证件照（420×560，页面内按原始比例与原始色彩完整呈现）
├── gate-logo.png                   # 门禁页标识图
├── 匡烨-简历.pdf / Kuang-Ye-Resume.pdf  # 中英文简历
├── build_standalone.py             # 单文件版构建脚本
├── deploy_pages.py                 # 部署脚本：经 GitHub API 提交并触发 Pages 重建
├── legacy/                         # 旧版（青色科幻风）存档，仅备份不参与部署
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
2. **重建单文件版**：`python build_standalone.py`（资源 base64 化 + PDF 链接改写为运行时 Blob）
3. **部署**：`python deploy_pages.py` 提交到 GitHub（Pages 自动重建，约 20 秒生效）

> 说明：本地 git 在非交互环境可能因凭证助手或传输问题失败（`fetch-pack: invalid index-pack output`），因此部署改用 GitHub Git Data API，只依赖已登录的 `gh` CLI。

## QA 方法

- headless Chrome（`--dump-dom` + 注入测试脚本）走**真实 UI 路径**：点击按钮 → 填写表单 → 触发 submit → 断言 DOM 状态
- 多断点视觉验证：桌面 / 平板 / 390px 手机（注意：headless Chrome 窗口宽度下限约 500px，真机小屏需 iframe 外壳模拟）
- 云端回路验证：线上「插入 → 读回 → 删除」完整闭环，测试数据用后即删
- 密码泄露扫描：全仓库大小写不敏感扫描明文，甄别 base64 随机子串误报

## 相关仓库

- [EasonQuantico/EasonQuantico](https://github.com/EasonQuantico/EasonQuantico) — 本站点代码

---

© 2026 匡烨 · Built with AI-assisted workflow

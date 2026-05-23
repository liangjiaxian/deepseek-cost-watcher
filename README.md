# DeepSeek Token Monitor

大模型 Token 使用量实时监测平台。通过代理转发 DeepSeek API 请求捕获每次调用的 Token 消耗，同时定时轮询余额和费用数据，提供实时监控面板、日报、周报及配置管理功能。

---

## 核心功能

- **代理转发** — 将 API 请求转发至 DeepSeek，自动记录每次调用的模型、Token 数、耗时
- **实时监控面板** — 账户余额、本月消费、今日消费、消费天数，每 10 秒轮询更新
- **模型消费分布** — 各模型费用占比环形图
- **每日报告** — 按小时聚合柱状图、模型用量排名、指定日期回溯
- **每周报告** — 日粒度趋势、模型对比、周维度汇总
- **余额追踪** — 定时记录余额快照，生成余额变化趋势
- **费用明细** — 从 DeepSeek 开放平台拉取每日费用，支持按模型、按日期下钻
- **API Key 管理** — 前端添加 / 删除 / 测试 Key，AES-256-GCM 加密存储
- **定时任务** — 可配置轮询间隔，自动记录余额和费用，调度日志可查
- **Docker 一键部署** — Docker Compose 编排前后端，开箱即用

---

## 快速开始

### Docker 部署（推荐）

```bash
# 克隆项目
git clone https://github.com/liangjiaxian/deepseek-cost-watcher.git && cd deepseek-monitor

# 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 MASTER_KEY 和 APP_SECRET（可用 openssl rand -base64 32 生成）

# 启动所有服务
docker compose up --build
```

访问 `http://localhost:5173`。

数据持久化在 `backend/data/monitor.db`，由 named volume 管理，重启不丢失。

### 本地开发

```bash
# 后端
cd backend
uv venv && source .venv/bin/activate && uv sync
cp .env.example .env
uv run uvicorn app.main:app --reload --port 8000

# 前端（新终端）
cd frontend
npm install
npm run dev
```

Vite 开发服务器自动代理 `/api` 和 `/v1` 到 `localhost:8000`，打开 `http://localhost:5173` 即可。

---

## 项目结构

```
deepseek-monitor/
├── docker-compose.yml          # Docker Compose：backend + frontend 编排
├── backend/
│   ├── Dockerfile              # 后端容器构建（uv + uvicorn）
│   ├── pyproject.toml          # Python 依赖声明
│   ├── .env                    # 运行时环境变量
│   ├── .env.example            # 环境变量模板
│   ├── data/                   # SQLite 数据文件持久化目录
│   └── app/
│       ├── main.py             # FastAPI 应用入口（路由注册 + 生命周期）
│       ├── api/                # HTTP 路由层
│       │   ├── usage.py        #   GET /api/v1/usage/* 查询接口
│       │   ├── models_api.py   #   GET /api/v1/models 模型列表
│       │   ├── settings.py     #   CRUD /api/v1/settings/* 配置管理
│       │   ├── proxy.py        #   POST /v1/chat/completions 代理转发
│       │   ├── status.py       #   GET /api/v1/status 服务状态
│       │   └── scheduler_api.py#   GET/POST /api/v1/scheduler/* 调度管理
│       ├── core/               # 基础设施
│       │   ├── config.py       #   Pydantic Settings（环境变量读取）
│       │   ├── database.py     #   SQLAlchemy async engine + session
│       │   └── security.py     #   Fernet AES-256-GCM 加密/解密
│       ├── models/             # SQLAlchemy ORM 模型（6 张表）
│       ├── schemas/            # Pydantic 请求/响应模型
│       ├── services/           # 业务逻辑层
│       │   ├── token_service.py    # Token 查询聚合
│       │   ├── balance_service.py  # 余额快照 + 趋势
│       │   ├── cost_service.py     # 费用拉取 + 查询
│       │   ├── key_service.py      # API Key CRUD
│       │   └── proxy_service.py    # 代理转发逻辑
│       └── tasks/
│           └── scheduler.py    # APScheduler 定时任务
├── frontend/
│   ├── Dockerfile              # 前端容器构建（node build + nginx）
│   ├── nginx.conf              # 生产环境反向代理配置
│   ├── package.json            # NPM 依赖（Vue 3 + ECharts + Tailwind）
│   ├── vite.config.js          # Vite 开发配置 + API 代理
│   ├── tailwind.config.js      # Tailwind 主题扩展
│   └── src/
│       ├── main.js             # Vue 应用入口
│       ├── App.vue             # 根组件
│       ├── style.css           # 全局样式 + CSS 自定义属性（明暗主题）
│       ├── api/index.js        # Axios 封装 + 全部 API 调用函数
│       ├── router/index.js     # 路由定义（5 个页面）
│       ├── stores/             # Pinia 状态管理
│       │   ├── app.js          #   应用状态（主题、刷新、时间范围）
│       │   ├── usage.js        #   用量数据（余额、费用、日报、周报）
│       │   └── settings.js     #   配置数据（密钥、状态、Platform Token）
│       ├── layouts/
│       │   └── MainLayout.vue  # 全局布局（侧边栏 + 顶栏 + 内容区）
│       ├── components/         # 通用组件
│       │   ├── Sidebar.vue     #   导航侧边栏
│       │   ├── TopBar.vue      #   顶栏（标题 + 时间范围 + 刷新）
│       │   ├── StatCard.vue    #   指标卡片
│       │   ├── ChartCard.vue   #   图表卡片（自动适配暗色主题）
│       │   ├── DataTable.vue   #   通用数据表格
│       │   └── StatusIndicator.vue # 状态指示灯
│       ├── composables/
│       │   └── useChartTheme.js    # ECharts 暗色主题适配
│       └── views/
│           ├── Dashboard.vue       # 实时监控面板
│           ├── DailyReport.vue     # 每日报告
│           ├── WeeklyReport.vue    # 每周报告
│           ├── SchedulerLogs.vue   # 调度日志
│           └── Settings.vue        # 系统设置
```

---

## 功能详情

### 代理转发（核心数据采集）

用户将 API 请求地址指向 `{monitor_url}/v1/chat/completions`，Monitor 转发至 `https://api.deepseek.com`，从响应中提取 `usage` 字段写入数据库，再将原始响应返回用户。这是 **DeepSeek 唯一获取 Token 用量明细的方式**。

### 余额追踪

APScheduler 定时调用 `/user/balance` 记录余额快照，生成余额变化趋势图。轮询间隔可在设置页动态调整（默认 30 分钟）。

### 费用明细

通过 DeepSeek 开放平台（platform.deepseek.com）的 Bearer Token，拉取每日按模型拆分的费用数据（含 Prompt / Cache Hit / Cache Miss / Response / Request 各项费用）。Token 需用户从浏览器手动获取，有效期有限，可在设置页配置和测试。

### 实时监控面板

| 区域 | 内容 |
|------|------|
| 指标卡片 | 账户余额、本月消费、今日消费、消费天数 |
| 余额趋势 | 折线/面积图，固定 7d 范围 |
| 模型消费分布 | 各模型费用占比环形图 |
| 月度费用 | 当月每日费用柱状图 |
| 自动刷新 | 前端每 10 秒轮询，页面不可见时暂停 |

### 每日报告

选择日期查看当日详情：起止余额、余额变化、活跃模型数、余额变化趋势、模型费用分布、费用类型明细（Prompt / Cache Hit / Cache Miss / Response / Request）。

### 每周报告

选择 ISO 周查看周度汇总：周总消耗、日均消耗、余额变化、每日费用柱状图、模型费用占比。

### 调度日志

记录定时任务的每次执行情况（状态、开始时间、结束时间、消息），支持手动触发余额和费用轮询。

### 系统设置

- **主题切换**：浅色 / 深色模式
- **API Key 管理**：添加 / 删除 / 测试，AES-256-GCM 加密存储至 SQLite
- **Platform Token**：配置 DeepSeek 开放平台 Token，用于拉取费用数据
- **系统配置**：代理轮询间隔、数据保留天数
- **服务状态**：DeepSeek 连通性、定时器下次执行时间、上次执行状态

---

## 技术框架

### 整体架构

```
┌──────────────────────────────────────────────────────────┐
│                    前端 (Vue 3)                          │
│   Vue Router / Pinia / ECharts / Tailwind / Axios       │
│   nginx 反向代理到后端 (生产) / Vite 代理 (开发)         │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP REST (JSON)
┌──────────────────────▼───────────────────────────────────┐
│                  后端 (Python FastAPI)                    │
│                                                         │
│   ┌───────────────┐  ┌────────────┐  ┌───────────────┐  │
│   │  Proxy 转发    │  │ 定时任务    │  │  REST API      │  │
│   │  /v1/chat/     │  │ 余额/费用   │  │  数据查询/配置  │  │
│   │  completions   │  │ 轮询       │  │               │  │
│   └───────┬───────┘  └─────┬──────┘  └───────┬───────┘  │
│           │                │                  │          │
│   ┌───────▼────────────────▼──────────────────▼───────┐  │
│   │              Service Layer                         │  │
│   │  Token / Balance / Cost / Key / Proxy Service     │  │
│   └──────────────────────┬────────────────────────────┘  │
│                          │                               │
│   ┌──────────────────────▼────────────────────────────┐  │
│   │           SQLAlchemy 2.0 Async ORM                │  │
│   └──────────────────────┬────────────────────────────┘  │
│                          │                               │
├──────────────────────────┼───────────────────────────────┤
│                   ┌──────▼──────┐                        │
│                   │   SQLite    │                        │
│                   │  data/*.db  │                        │
│                   └─────────────┘                        │
│                                                          │
│   ┌──────────────────────────────────────────────────┐   │
│   │              DeepSeek API                        │   │
│   │  POST /chat/completions → usage 字段              │   │
│   │  GET  /user/balance      → 余额数据               │   │
│   │  GET  /models            → 模型列表               │   │
│   │  platform.deepseek.com   → 费用明细               │   │
│   └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### 前后端关系

- **纯 REST 通信**，统一响应格式 `{code, message, data}`
- 前端通过 Axios 请求后端，**前端不直接调用 DeepSeek API**
- API Key 始终留在后端内存和加密存储中，前端仅可见 Key 前缀
- 生产环境通过 nginx 反向代理 `/api/` 和 `/v1/` 到 `backend:8000`

### 数据存储（SQLite）

数据库文件位于 `backend/data/monitor.db`，启动时自动创建。使用 WAL 模式提升并发性能。

#### 表设计

**token_records** — 代理转发采集的 Token 消耗明细

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| api_key_id | INTEGER FK | 关联 api_keys |
| request_id | VARCHAR(64) | DeepSeek 请求 ID |
| model | VARCHAR(64) | 模型名 |
| prompt_tokens | INTEGER | 输入 Token |
| completion_tokens | INTEGER | 输出 Token |
| total_tokens | INTEGER | 总计 |
| duration_ms | INTEGER | 请求耗时 |
| created_at | DATETIME | 记录时间（已索引） |

**balance_snapshots** — 定时轮询的余额快照

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| api_key_id | INTEGER FK | 关联 api_keys |
| balance | REAL | 余额 |
| total_usage | REAL | 累计使用 |
| currency | VARCHAR(10) | 货币 |
| recorded_at | DATETIME | 记录时间（已索引） |

**usage_cost_records** — 开放平台拉取的费用数据

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| date | VARCHAR(10) | 日期（已索引） |
| model | VARCHAR(64) | 模型名 |
| prompt_token_cost | FLOAT | Prompt 费用 |
| cache_hit_token_cost | FLOAT | 缓存命中费用 |
| cache_miss_token_cost | FLOAT | 缓存未中费用 |
| response_token_cost | FLOAT | 输出费用 |
| request_cost | FLOAT | 请求费用 |
| total_cost | FLOAT | 总费用 |
| currency | VARCHAR(10) | 货币 |
| UNIQUE(date, model) | | 联合唯一约束 |

**api_keys** — AES 加密存储的 API Key

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| name | VARCHAR(64) | 别名 |
| key_encrypted | TEXT | AES-256-GCM 密文 |
| key_prefix | VARCHAR(8) | 明文前缀用于显示 |
| is_active | INTEGER | 是否启用 |
| created_at / updated_at | DATETIME | 时间戳 |

**system_config** — KV 配置存储

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| config_key | VARCHAR(64) UNIQUE | 配置键名 |
| config_value | VARCHAR(512) | 配置值 |
| updated_at | DATETIME | 更新时间 |

**scheduler_logs** — 调度执行日志

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| task_name | VARCHAR(64) | 任务名 |
| status | VARCHAR(16) | success / error / skipped |
| message | VARCHAR(512) | 详情 |
| started_at / finished_at / created_at | DATETIME | 时间戳 |

### 前端说明

- **框架**：Vue 3 (Composition API + `<script setup>`)
- **构建**：Vite 5，HMR 开发体验
- **路由**：Vue Router 4（history 模式），5 个页面
- **状态管理**：Pinia，3 个 Store（app / usage / settings）
- **图表**：ECharts 5 + vue-echarts 7，适配明暗双主题
- **样式**：Tailwind CSS 3 + CSS 自定义属性（OKLCH 色值），完整明暗主题系统
- **图标**：lucide-vue-next
- **HTTP**：Axios，统一拦截器，30s 超时

### 后端说明

- **框架**：Python 3.12 + FastAPI
- **ORM**：SQLAlchemy 2.0 Async（aiosqlite）
- **定时调度**：APScheduler（AsyncIOScheduler），支持运行时调整间隔
- **API 转发**：httpx AsyncClient，流式 / 非流式均支持
- **加密**：cryptography 库 Fernet（AES-256-GCM），MASTER_KEY 派生
- **配置**：Pydantic Settings 读取环境变量

### 安全方案

| 措施 | 实现 |
|------|------|
| 静态加密 | AES-256-GCM (Fernet)，`MASTER_KEY` 从环境变量读取 |
| 前端隔离 | 前端请求 Key 列表时，后端仅返回 `key_prefix` 和 `id`，**不返回完整 Key** |
| 使用隔离 | 代理转发时后端从数据库读取解密后的 Key，请求链路不暴露明文 |
| 密钥轮换 | 设置页支持删除 / 重新添加 Key |
| Master Key | 由 `openssl rand -base64 32` 生成，写入 `.env` |
| 环境变量安全 | `.env` 仅在生产服务器本地维护，不提交至版本控制 |

---

## 开发者贡献

本项目全程使用 **DeepSeek 驱动的 Vibe Coding** 模式开发（花费3.08元），主要过程如下：

- **需求定义** → 通过对话明确监测需求、API 能力边界、数据采集策略
- **架构设计** → AI 分析 DeepSeek API 特性后提出双模式监测方案（代理转发 + 余额轮询）
- **代码生成** → 前后端代码由 AI 逐模块生成，人工审查后合并
- **UI 设计** → 从产品策略文档（PRODUCT.md）到设计规范（DESIGN.md）到 UI 规格书（UI_SPECIFICATION.md），全链路 AI 辅助产出
- **运维配置** → Docker Compose、Dockerfile、nginx 配置、健康检查均由 AI 生成和调优
- **迭代优化** → 全部 30+ 个 API 端点、6 张数据库表、5 个前端页面、3 个 Store 均为 AI 生成

---

> DeepSeek Token Monitor V1.0 — 基于 DeepSeek Vibe Coding 的全栈监控解决方案

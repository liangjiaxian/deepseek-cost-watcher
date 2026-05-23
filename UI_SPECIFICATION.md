# DeepSeek Monitor — UI 规范文档

> 本文档为视觉设计规范。设计令牌（Design Tokens）的完整定义见 [DESIGN.md](./DESIGN.md)，产品策略上下文见 [PRODUCT.md](./PRODUCT.md)。

---

## 1. 设计原则

- **答案驱动**：每个页面对应一个问题。没有问题就不需要这个页面。
- **数据优先**：数值是最重要的信息层级，获得最大的视觉权重。
- **主题自适应**：浅色和深色主题均由用户选择，无默认值。深色用于沉浸监控，浅色用于日间协作。
- **克制工具感**：标准导航、标准组件、标准交互。工具应当消失在任务中。
- **零焦虑状态**：每个加载态有骨架屏，每个空态有引导，每个错误态有恢复路径。

---

## 2. 色彩体系

基于 OKLCH 色彩空间。不使用 `#000` 或 `#fff`。中性色向品牌色方向做极低色度偏移（`chroma 0.006–0.018`）。

**色彩策略**：Restrained（克制型）—— 染色中性色 + 单强调色 ≤ 10% 面积。图表等局部可使用 Committed（承诺型）染色。

### 2.1 深色主题

| Token | 色值 | 用途 |
|-------|------|------|
| `--bg` | `#0F1118` | 页面画布 |
| `--surface` | `#1A1D28` | 卡片、面板、侧边栏 |
| `--surface-hover` | `#222536` | 悬浮态、下拉菜单 |
| `--surface-raised` | `#292D3E` | 弹窗、气泡、Tooltip |
| `--border` | `#2E3242` | 卡片边框、分割线 |
| `--border-subtle` | `#252838` | 轻度分割线（表格行） |
| `--text-primary` | `#EFF3F7` | 标题、数值、导航 |
| `--text-secondary` | `#94A3B8` | 标签、描述、元信息 |
| `--text-tertiary` | `#64748B` | 占位符、禁用 |
| `--brand` | `#4F8CFF` | 强调色、按钮、链接 |
| `--brand-hover` | `#3A73E0` | 品牌色 Hover |
| `--brand-subtle` | `#1E3A6E` | 品牌色背景染色（标签） |
| `--success` | `#34D399` | 健康 / 已连接 |
| `--warning` | `#FBBF24` | 阈值接近 |
| `--danger` | `#F87171` | 错误 / 超限 |

**深色主题特点**：无阴影，层级通过亮度区分（`--surface` → `--surface-hover` → `--surface-raised`）。

### 2.2 浅色主题

| Token | 色值 | 用途 |
|-------|------|------|
| `--bg` | `#F6F8FB` | 页面画布（温暖中性色） |
| `--surface` | `#EEF1F5` | 卡片、面板、侧边栏 |
| `--surface-hover` | `#E5E9EF` | 悬浮态、下拉菜单 |
| `--surface-raised` | `#FCFDFD` | 弹窗、气泡、Tooltip |
| `--border` | `#D5DAE2` | 卡片边框、分割线 |
| `--border-subtle` | `#E2E6ED` | 轻度分割线（表格行） |
| `--text-primary` | `#1E2233` | 标题、数值、导航 |
| `--text-secondary` | `#5F6B80` | 标签、描述、元信息 |
| `--text-tertiary` | `#909DAE` | 占位符、禁用 |
| `--brand` | `#3B82F6` | 强调色、按钮、链接 |
| `--brand-hover` | `#2563EB` | 品牌色 Hover |
| `--brand-subtle` | `#DBE8FF` | 品牌色背景染色（标签） |
| `--success` | `#22B572` | 健康 / 已连接 |
| `--warning` | `#E5A000` | 阈值接近 |
| `--danger` | `#DC4C4C` | 错误 / 超限 |

**浅色主题特点**：背景温暖染色（`chroma 0.006` 向品牌色偏移），避免纯白实验室观感。卡片用亮度区分，弹窗使用阴影。

### 2.3 图表色板（双主题共享色序）

| 序号 | 深色 | 浅色 |
|------|------|------|
| 1 (品牌) | `#4F8CFF` | `#3B82F6` |
| 2 (成功) | `#34D399` | `#22B572` |
| 3 (警告) | `#FBBF24` | `#E5A000` |
| 4 (危险) | `#F87171` | `#DC4C4C` |
| 5 (紫色) | `#A78BFA` | `#8B5CF6` |
| 6 (粉色) | `#F472B6` | `#E879A8` |
| 7 (浅蓝) | `#60A5FA` | `#60A5FA` |

面积填充：15% 不透明度。描线：80% 不透明度。无渐变填充。

### 2.4 主题切换

主题切换通过 HTML 根元素切换 `class="dark"` 实现。所有颜色值定义为 CSS 自定义属性：

```css
:root { /* 浅色主题 */ }
.dark  { /* 深色主题 */ }
```

无 `prefers-color-scheme` 自动检测。用户通过设置页手动选择，选择结果持久化。

---

## 3. 排版

### 3.1 字体

- 西文无衬线：`'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif`
- 等宽数字：`'JetBrains Mono', 'Fira Code', 'SF Mono', ui-monospace, monospace`
- 单一字体族，无展示体/正文字体配对

### 3.2 字号层级

固定 rem 比例，缩放比 1.2。无流体排版。

| 层级 | 字号 | 字重 | 行高 | 字间距 | 用途 |
|------|------|------|------|--------|------|
| H1 | 28px / 1.75rem | 700 | 36px / 2.25rem | -0.015em | 页面标题 |
| H2 | 22px / 1.375rem | 600 | 30px / 1.875rem | — | 区块标题 |
| H3 | 18px / 1.125rem | 600 | 26px / 1.625rem | — | 卡片标题 |
| Body | 14px / 0.875rem | 400 | 22px / 1.375rem | — | 正文、表格 |
| Small | 12px / 0.75rem | 400 | 18px / 1.125rem | — | 辅助文字、标签 |
| Number-LG | 32px / 2rem | 700 | 1 | — | 主要指标数值 |
| Number-MD | 24px / 1.5rem | 700 | 1 | — | 次要指标数值 |
| Nav | 15px / 0.9375rem | 500 | 20px / 1.25rem | — | 导航文字 |
| Button | 14px / 0.875rem | 500 | 1 | — | 按钮标签 |
| Label | 13px / 0.8125rem | 500 | 18px / 1.125rem | 0.01em | 表单标签、表头 |

### 3.3 数字

全部数值使用等宽字体。启用 `font-variant-numeric: tabular-nums` 保持数字对齐。

### 3.4 行长

正文容器最大 75ch。数据表格可运行至 120ch+。

---

## 4. 布局结构

```
+---------------------------+----------------------------------------+
|                           |  TopBar (56px)                          |
|   侧边栏 (260px)          +----------------------------------------+
|                           |                                        |
|   Logo / 应用名           |  内容区域 (padding: 24px)               |
|                           |                                        |
|   • Dashboard             |  +------+ +------+ +------+ +------+  |
|   • Daily Report          |  | Stat | | Stat | | Stat | | Stat |  |
|   • Weekly Report         |  +------+ +------+ +------+ +------+  |
|   • Scheduler Logs        |                                        |
|   • Settings              |  +----------------------------------+  |
|                           |  | ChartCard (面积折线图)            |  |
|   版本号 + 状态指示        |  +----------------------------------+  |
|                           |                                        |
|                           |  +----------------+ +---------------+  |
|                           |  | 环形分布图     | | 柱状图        |  |
|                           |  +----------------+ +---------------+  |
+---------------------------+----------------------------------------+
```

### 4.1 侧边栏

- 宽度 260px，固定定位
- 背景色 `--surface`
- Logo + 应用名（高度 48px）
- 导航项（每个带 lucide 图标，20px）：
  1. **Dashboard** (`/dashboard`) — 实时费用概览
  2. **Daily Report** (`/daily`) — 每日消耗明细
  3. **Weekly Report** (`/weekly`) — 周度聚合报告
  4. **Scheduler Logs** (`/scheduler-logs`) — 定时任务日志
  5. **Settings** (`/settings`) — 配置管理
- 激活项：`--brand-subtle` 背景
- 悬浮项：`--surface-hover` 背景
- 底部：版本号 (`--text-small`, `--text-tertiary`) + 运行状态指示器

### 4.2 顶部栏

- 高度 56px
- 背景 `--bg`（与内容区融合而非卡片层）
- 底部边框 `--border-subtle`
- 左侧：页面标题
- 右侧：时间范围选择器 + 自动刷新开关 + 手动刷新按钮，间距 `12px`（`--space-3`）

### 4.3 内容区

- 填充 `24px`（`--space-6`），垂直滚动
- 卡片网格间距 `24px`

### 4.4 响应式断点

| 断点 | 布局变化 |
|------|----------|
| ≥1400px | 4 列 StatCard 网格，2 列图表网格 |
| 960–1399px | 2 列 StatCard，单列图表 |
| 640–959px | 单列，侧边栏收起为汉堡菜单 |
| <640px | 单列，内容区 padding 缩减至 16px（`--space-4`） |

---

## 5. 页面规范

### 5.1 实时监测页 `/dashboard`

**功能目标**：展示当前 DeepSeek API 费用消耗的实时状态。

**区块 A — 统计卡片行（4 张）**

| 卡片 | 指标 | 格式 |
|------|------|------|
| 账户余额 | 当前余额 + 日变化 | `¥1,234.56` + `↓¥50.00` |
| 本月消耗 | 当月累计 | `¥890.34` |
| 今日消耗 | 今日累计 | `¥89.23` |
| 计费天数 | 本月已使用天数 | `12 / 30` |

每张卡片结构：
- 左侧彩色图标块（40px，`--radius-md`，背景色 15% 语义色）
- 数值（`--text-number-lg` 或 `--text-number-md`，等宽，`--text-primary`）
- 标签（`--text-small`，`--text-secondary`）
- 趋势指示（语义色，`--text-small`，箭头 + 数值）

**区块 B — 余额趋势图**
- 面积折线图，品牌色填充 15% 不透明度
- X 轴：时间 / Y 轴：余额（¥）
- hover 显示十字准线 + 详细数据

**区块 C — 模型消耗分布**
- 环形图，7 色图表色板
- 中心显示总模型数
- hover 显示模型名 + 百分比 + 金额

**区块 D — 月度日消耗柱状图**
- 柱状图，品牌色
- 每日一柱，hover 显示当日合计

### 5.2 每日报告页 `/daily`

**功能目标**：查询指定日期的完整消耗明细。

- 顶部：日期选择器（`<input type="date">`，默认当天）
- 统计卡片行：期初余额、期末余额、变动金额、活跃模型数
- 余额变动趋势面积图（绿色）
- 模型消耗分布环形图
- 消耗类型分解柱状图（横向，按 Token 类型分组）
- 月度日消耗柱状图（邻近参考）

### 5.3 每周报告页 `/weekly`

**功能目标**：查看周度聚合费用报告。

- 顶部：周选择器（`<input type="week">`）
- 统计卡片行：周总消耗、日均消耗、余额变动、活跃模型数
- 日消耗柱状图（标签显示数值）
- 模型消耗分布环形图

### 5.4 定时任务日志 `/scheduler-logs`

**功能目标**：查看后台采集任务的执行记录。

- DataTable 展示最近 10 次执行
- 列：状态（彩色圆点）、开始时间、结束时间、耗时、消息

### 5.5 设置页 `/settings`

- **API Key 管理**：添加/删除 Key，测试连接，状态显示
- **平台 Token**：输入 DeepSeek 平台 Bearer Token，测试 + 保存
- **系统配置**：自动刷新开关、刷新间隔、轮询间隔、数据保留天数、手动触发按钮
- **服务状态**：DeepSeek API 连接状态、调度器信息（下次运行、上次运行、状态）
- **主题切换**：浅色 / 深色，选择后持久化

---

## 6. 组件规范

所有交互组件定义以下状态：default、hover、focus、active、disabled、loading。

### 6.1 StatCard

| 属性 | 值 |
|------|-----|
| 背景 | `--surface` |
| 边框 | `1px solid --border` |
| 圆角 | `--radius-lg` (8px) |
| 内边距 | `--space-5` (20px) |
| 图标块 | 40px，圆角 `--radius-md` (6px)，背景 15% 语义色 |
| 数值 | `--text-number-lg` / `--text-number-md`，`--font-mono`，`--text-primary` |
| 标签 | `--text-small`，`--text-secondary` |

无侧条纹边框。无英雄指标模板（大数字+小标签）——始终配合图表或上下文。

### 6.2 ChartCard

| 属性 | 值 |
|------|-----|
| 基础样式 | 同 StatCard |
| 标题 | `--text-h3`，`--text-primary` |
| 维度切换 | 分段按钮行，`--text-small` |
| 图表最小高度 | 240px |
| 空态 | 居中图标 + 正文 + 操作按钮 |

### 6.3 DataTable

| 属性 | 值 |
|------|-----|
| 背景 | 透明（继承父容器） |
| 表头 | `--text-label`，`--text-secondary`，底部 `--border-subtle` |
| 行悬浮 | `--surface-hover` |
| 交替行 | 通过 `--border-subtle` 分割线表现（非交替色） |
| 单元格内边距 | `8px 12px` |
| 空态 | 居中插画 + 正文 |

### 6.4 Button

| 变体 | 背景 | 文字 | Hover | 焦点 |
|------|------|------|-------|------|
| Primary | `--brand` | `#fff` | `--brand-hover` | ring `--brand` |
| Secondary | `--surface` | `--text-primary` | `--surface-hover` | ring `--border` |
| Ghost | 透明 | `--text-secondary` | `--surface-hover` | — |
| Danger | `--danger` | `#fff` | 暗 10% | ring `--danger` |

全部：`--radius-md` (6px)，内边距 `12px 16px`，`--text-button`，过渡 150ms ease。

### 6.5 Tag

| 类型 | 背景 | 文字 |
|------|------|------|
| Brand | `--brand-subtle` | `--brand` |
| Success | 15% `--success` | `--success` |
| Warning | 15% `--warning` | `--warning` |
| Danger | 15% `--danger` | `--danger` |
| Neutral | `--surface-hover` | `--text-secondary` |

`--radius-sm` (4px)，内边距 `4px 8px`，`--text-small`。

### 6.6 Input / Select

| 属性 | 值 |
|------|-----|
| 背景 | `--surface` |
| 边框 | `1px solid --border` |
| 圆角 | `--radius-md` (6px) |
| 内边距 | `8px 12px` |
| 文字 | `--text-body`，`--text-primary` |
| 占位符 | `--text-tertiary` |
| 焦点态 | border `--brand`，ring 20% `--brand` |
| 禁用态 | `--text-tertiary`，`--border-subtle` |

### 6.7 Switch

| 属性 | 值 |
|------|-----|
| 轨道 | 36×20px，`--border` 背景 / 激活 `--brand` |
| 滑块 | 16px 正圆，白色 |
| 过渡 | 200ms ease，仅平移 transform（禁止动画面板布局属性） |

### 6.8 StatusIndicator

| 属性 | 值 |
|------|-----|
| 圆点 | 8px，语义色 |
| 标签 | `--text-small`，`--text-secondary` |
| 间距 | `--space-2` (8px) |

### 6.9 Skeleton Loading

| 属性 | 值 |
|------|-----|
| 背景 | `--surface-hover` |
| 动画 | 伪元素渐变扫光，1.5s 无限线性 |
| 形状 | 匹配内容块轮廓（卡片轮廓 / 文字行块） |

---

## 7. 交互规范

| 交互 | 行为 |
|------|------|
| **自动刷新** | 启动后按间隔轮询 API，页面数据平滑更新；页面不可见时暂停 |
| **手动刷新** | 点击刷新按钮触发强制轮询，按钮旋转 360° 动画持续到响应返回（仅旋转 transform） |
| **图表悬浮** | 面积图/柱状图 hover 显示十字准线 + 数据标签 |
| **时间范围** | 切换时重新请求后端数据，保持当前页面不刷新 |
| **主题切换** | 设置页切换浅色/深色，通过 `class="dark"` 切换，结果存入 localStorage |
| **空状态** | 首次使用显示居中图标 + "开始监测"引导按钮 |
| **错误状态** | API 异常时卡片显示错误遮罩 + "重试"按钮，不影响其他卡片 |
| **响应式** | 侧边栏 <640px 时收起为汉堡菜单；卡片网格自适应列数 |

### Motion 规范

| 场景 | 时长 | 缓动曲线 |
|------|------|----------|
| Hover / Focus | 150ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| 面板显隐 / 骨架→内容 | 200ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| 路由切换 | 250ms | `cubic-bezier(0.16, 1, 0.3, 1)` |

**规则**：
- 禁止动画化 CSS 布局属性（width, height, top, left, margin, padding）
- 无编排的页面加载序列
- motion 仅用于表达状态，无纯装饰动画
- `prefers-reduced-motion: reduce` 时所有过渡归零

---

## 8. 技术选型

| 层 | 技术 | 说明 |
|----|------|------|
| 前端框架 | Vue 3 (Composition API + `<script setup>`) | |
| 构建工具 | Vite | |
| 状态管理 | Pinia | |
| 路由 | Vue Router 4 (history mode) | |
| HTTP | Axios | |
| 图表 | ECharts 5 + vue-echarts 7 | |
| 样式 | Tailwind CSS 3 | |
| 图标 | lucide-vue-next | |
| 后端 | Python FastAPI | |
| ORM | SQLAlchemy + SQLite / PostgreSQL | |
| 定时任务 | APScheduler | |

---

## 9. API 接口约定

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/usage/realtime` | 实时用量摘要 |
| GET | `/api/v1/balance/trend?range=1h\|6h\|24h\|7d` | 余额趋势 |
| GET | `/api/v1/usage/daily?date=2026-05-23` | 日度详情 |
| GET | `/api/v1/usage/weekly?year=2026&week=21` | 周度报告 |
| GET | `/api/v1/usage/cost` | 消耗数据 |
| GET | `/api/v1/models/distribution` | 模型消耗分布 |
| GET | `/api/v1/status` | 服务连接状态 |
| GET | `/api/v1/scheduler/status` | 调度器状态 |
| GET | `/api/v1/scheduler/logs` | 调度器日志 |
| POST | `/api/v1/settings/keys` | 保存 API Key |
| GET | `/api/v1/settings/keys` | 获取 Key 列表 |
| POST | `/api/v1/settings/keys/test` | 测试 Key 连接 |
| POST | `/api/v1/settings/platform-token` | 保存平台 Token |
| POST | `/api/v1/settings/trigger-poll` | 手动触发轮询 |

响应格式：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

---

## 10. 路由设计

| 路径 | 页面 | 组件 |
|------|------|------|
| `/` | 重定向到 `/dashboard` | — |
| `/dashboard` | 实时监测 | Dashboard |
| `/daily` | 每日报告 | DailyReport |
| `/weekly` | 每周报告 | WeeklyReport |
| `/scheduler-logs` | 调度日志 | SchedulerLogs |
| `/settings` | 设置 | Settings |

---

## 11. 绝对禁止模式

与 Impeccable Design Laws 一致，以下模式在任何主题下均禁止出现：

- **侧条纹边框**：`border-left` / `border-right` > 1px 作为彩色装饰条
- **渐变文字**：`background-clip: text` + 渐变背景
- **毛玻璃默认**：大面积 `backdrop-filter: blur` 作为默认装饰
- **英雄指标模板**：大数字 + 小标签 + 渐变强调的 SaaS 风格指标卡
- **相同卡片网格**：重复的图标 + 标题 + 正文卡片排列
- **模态框优先**：未穷尽内联/渐进方案前使用弹窗
- **装饰动效**：不表达状态的动画
- **组件不一致**：不同页面出现不同样式的同类组件
- **展示字体用于 UI**：在按钮、标签、数据中使用展示字体
- **自定义标准控件**：自定义滚动条、非标准表单控件、非常规弹窗

---

## 附录 A：设计文件索引

| 文件 | 用途 |
|------|------|
| `PRODUCT.md` | 产品策略、用户画像、品牌个性 |
| `DESIGN.md` | 设计令牌完整定义（OKLCH 值、间距、阴影、动效曲线） |
| `UI_SPECIFICATION.md` | 本文档 — UI 规范和页面规范 |

*设计令牌以 DESIGN.md 为唯一事实来源。本文档中的色值为快速参考。*

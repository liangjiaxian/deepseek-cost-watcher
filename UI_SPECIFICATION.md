# DeepSeek Monitor — UI 规范文档

> 本文档为视觉设计规范。设计令牌的完整定义见 [DESIGN.md](./DESIGN.md)，产品策略上下文见 [PRODUCT.md](./PRODUCT.md)。

---

## 1. 设计原则

- **暖纸编辑风（Bifrost 基调）**：整体采用暖纸底色、直角、发丝线、2px 描边的编辑式排版，克制、书卷气，而非通用 SaaS 观感。
- **数据优先**：数值是最重要的信息层级，统计卡大数字使用衬线体获得最大视觉权重。
- **主题自适应**：浅色（暖纸）与深色（Bifrost 文档取色）两套主题共享同一套结构与组件规则，仅色值不同。
- **克制的工具感**：标准导航、标准组件、标准交互；装饰只作低对比度点缀，不参与信息表达。
- **零焦虑状态**：每个加载态有骨架屏，每个空态有引导，每个错误态有恢复路径。
- **设计来源**：
  - 主参考 `bifrost.ai`：暖纸色板、直角几何、2px 描边、mono 标签、Lora 衬线标题、像素网格角标、硬投影与焦点环。
  - 深色取色参考 `docs.getbifrost.ai`（Deployment Guides）：近黑画布、品牌绿高亮、灰阶文字。
  - 辅助参考 `spom-park-ai-agent.netlify.app`：半透明模糊顶栏、卡片右上角点阵装饰。

---

## 2. 色彩体系

**色彩策略**：Restrained（克制型）—— 暖纸中性色打底，单品牌蓝作为强调色，面积占比 ≤ 10%。图表等局部可使用 Committed（承诺型）染色。

### 2.1 浅色主题（暖纸 / Bifrost）

| Token | 色值 | 用途 |
|-------|------|------|
| `--color-bg` | `#FCFBF8` | 页面画布（暖纸） |
| `--color-surface` | `#FFFFFF` | 卡片、面板、侧边栏 |
| `--color-surface-hover` | `#F5F7FA` | 悬浮态、表头底、标签底 |
| `--color-surface-raised` | `#FEFDFB` | 次级按钮、弹窗、气泡 |
| `--color-border` | `#C7D3E8` | 2px 描边、输入框边框、深分隔 |
| `--color-border-subtle` | `#E6EBF1` | 发丝线（卡片边框、表格行） |
| `--color-hairline` | `#F5F7FA` | 最浅分割线 |
| `--color-text-primary` | `#0B1220` | 标题、数值、导航 |
| `--color-text-secondary` | `#475467` | 标签、描述、元信息 |
| `--color-text-tertiary` | `#96A0B0` | 占位符、禁用、坐标轴 |
| `--color-brand` | `#4F8BFF` | 主强调色、主按钮、占比条 |
| `--color-brand-hover` | `#3D7FF0` | 品牌 Hover |
| `--color-brand-subtle` | `#EEF4FF` | 激活导航底、淡淡品牌染色 |
| `--color-brand-line` | `#A8C8FC` | 浅蓝描边、深色硬投影映射 |
| `--color-kicker` | `#2E6BE0` | Kicker 标签文字、Ghost 按钮 |
| `--color-success` | `#22C55E` | 健康 / 已连接 |
| `--color-warning` | `#F59E0B` | 阈值接近 / 排名第 1 |
| `--color-danger` | `#EF4444` | 错误 / 超限 |
| `--color-bg-blur` | `rgba(252,251,248,.80)` | 顶栏半透明底 |
| `--color-success-subtle` | `rgba(34,197,94,.12)` | 成功状态浅底 |
| `--color-neutral-subtle` | `rgba(150,160,176,.16)` | 中性状态浅底 |
| `--color-dot` | `rgba(79,139,255,.20)` | 卡片点阵装饰 |
| `--color-on-brand` | `#FFFFFF` | 品牌色上的文字 |

**浅色主题特点**：暖纸画布 + 纯白卡片，卡片无阴影，仅靠发丝线分层（`--shadow-card: none`）。

### 2.2 深色主题（Bifrost 文档站取色）

深色取色基准：`docs.getbifrost.ai` 深色主题 —— 背景 `#090D0D`、高亮 `#07C983`、普通文字 `#9EA0A0`、高亮文字 `#EEEFF0`。表面层级与边框在此基础上按透明度推导，保持原有布局与边框规格不变。

| Token | 色值 | 用途 |
|-------|------|------|
| `--color-bg` | `#090D0D` | 页面画布 |
| `--color-surface` | `#161919` | 卡片、面板、侧边栏 |
| `--color-surface-hover` | `#1F2222` | 悬浮态、下拉菜单 |
| `--color-surface-raised` | `#222525` | 弹窗、气泡、次级按钮 |
| `--color-border` | `#2A2D2D` | 2px 描边、输入框边框 |
| `--color-border-subtle` | `#1E2121` | 发丝线（卡片边框、表格行） |
| `--color-hairline` | `#191C1C` | 最浅分割线 |
| `--color-text-primary` | `#EEEFF0` | 标题、数值、导航（高亮文字） |
| `--color-text-secondary` | `#9EA0A0` | 标签、描述、元信息（普通文字） |
| `--color-text-tertiary` | `#707172` | 占位符、禁用、坐标轴 |
| `--color-brand` | `#07C983` | 主强调色、主按钮、占比条（高亮色） |
| `--color-brand-hover` | `#06B877` | 品牌 Hover |
| `--color-brand-subtle` | `rgba(7,201,131,.12)` | 激活导航底 |
| `--color-brand-line` | `#0E7A55` | 深色硬投影映射 |
| `--color-kicker` | `#07C983` | Kicker 标签文字、Ghost 按钮 |
| `--color-on-brand` | `#08110E` | 品牌色上的文字（深色主题必须用深字） |
| `--color-success` | `#34D399` | 健康 / 已连接 |
| `--color-warning` | `#FBBF24` | 阈值接近 / 排名第 1 |
| `--color-danger` | `#F87171` | 错误 / 超限 |
| `--color-bg-blur` | `rgba(9,13,13,.80)` | 顶栏半透明底 |
| `--color-success-subtle` | `rgba(52,211,153,.15)` | 成功状态浅底 |
| `--color-neutral-subtle` | `rgba(158,160,160,.18)` | 中性状态浅底 |
| `--color-dot` | `rgba(7,201,131,.18)` | 卡片点阵装饰 |

**深色主题特点**：近黑画布 + 近黑卡片，层级通过轻微提亮与 1px 发丝线区分；无阴影、无硬投影光效。品牌绿为高饱和亮色，其上文字必须使用 `--color-on-brand`（近黑），不可用白色。

### 2.3 图表色板（单色系明度阶梯）

图表不使用语义色（成功/警告/危险仅用于状态提示），而是用品牌色的明度阶梯区分系列：

- **深色**：绿色为主（品牌绿 → 浅绿 → 深绿 → 薄荷 → 极浅绿 → 墨绿），白色作辅助色（第 2 系列）。
- **浅色**：蓝色为主，通过蓝色深浅区分系列。

| 序号 | 深色 | 浅色 |
|------|------|------|
| 1（品牌） | `#07C983` | `#4F8BFF` |
| 2（辅助） | `#EEEFF0` | `#A8C8FC` |
| 3 | `#34D399` | `#2E6BE0` |
| 4 | `#0E7A55` | `#1E40AF` |
| 5 | `#6EE7B7` | `#7EB3FF` |
| 6 | `#A7F3D0` | `#93C5FD` |
| 7 | `#0A5C42` | `#DCE9FF` |

单系列图表（余额趋势、每日消费柱状图）统一使用第 1 色（品牌色）；多系列图表（模型分布环形图）按序号取色，超过 7 个系列循环使用。

面积填充：系列色 15% 不透明度。描线：实色。柱状图：直角（`borderRadius: 0`），无渐变。

### 2.4 主题切换

主题通过 HTML 根元素切换 `class="dark"` 实现。所有颜色定义为 CSS 自定义属性：

```css
:root { /* 浅色（暖纸） */ }
.dark  { /* 深色（Bifrost 文档取色） */ }
```

- 首次访问：无本地记录时跟随系统 `prefers-color-scheme`。
- 手动切换：设置页选择后写入 `localStorage.theme`，后续访问以本地记录为准。
- 预览参数：URL 追加 `?theme=dark` 可强制深色渲染（仅调试/截图用，不写入本地）。

### 2.5 色彩使用约束

- 矩形组件一律直角；圆角仅允许出现在圆形状态点、Switch 滑块这类「本来就是圆」的元件上。
- 2px 描边只用于主按钮、次级按钮、强调面板（`.card-panel`）；普通卡片使用 1px 发丝线。
- `--color-brand` 大面积仅出现在主按钮与激活分段按钮；其余场景用 `--color-brand-subtle` 染色。
- 硬投影 `--shadow-hard`（`4px 4px 0`）为强调手段，单页最多一处。

---

## 3. 排版

### 3.1 字体

- 展示衬线（标题 / 统计大数字）：`'Lora', Georgia, 'Times New Roman', serif` → `font-display`
- 正文无衬线：`'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif` → `font-sans`
- 等宽（数字 / 标签 / 表头 / 按钮）：`'Roboto Mono', 'JetBrains Mono', 'Fira Code', 'SF Mono', ui-monospace, monospace` → `font-mono`

字体通过 Google Fonts 在 `index.html` 一次性加载（Inter + Lora + Roboto Mono）。

### 3.2 字号层级

| 层级 | 字号 | 字重 | 字距 | 字体 | 用途 |
|------|------|------|------|------|------|
| Kicker | 11px / 0.6875rem | 500 | 0.14em，全大写 | Roboto Mono | 页面/卡片上方眉标（蓝） |
| Note | 11px / 0.6875rem | 500 | 0.04em | Roboto Mono | 静默元信息（灰） |
| Page title | 18px / 1.125rem | 500 | tight | Lora | 顶栏页面标题（H1） |
| Section title | 16px / 1rem | 500 | tight | Lora | 设置页分区标题（H2） |
| Card title | 14px / 0.875rem | 500 | tight | Lora | 卡片标题（H3） |
| Stat value | 28px / 1.75rem | 500 | tight | Lora | 统计卡大数字 |
| Body | 14px / 0.875rem | 400 | — | Inter | 正文、表格、导航 |
| Small | 12px / 0.75rem | 400 | — | Inter | 辅助文字、趋势 |
| Stat label | 11px / 0.6875rem | 500 | 0.08em | Inter | 统计卡标签 |
| Table head | 10px / 0.625rem | 500 | 0.12em，全大写 | Roboto Mono | 表头、分段按钮 |
| Button | 13px / 0.8125rem | 500 | — | Inter（次级用 Mono） | 按钮标签 |

### 3.3 数字

- 统计卡主数值使用 **Lora 衬线**，是页面唯一的「展示型数字」。
- 其余数值（表格、明细、图表 tooltip、占比）一律 `font-mono` + `font-variant-numeric: tabular-nums`。

### 3.4 行长

正文容器最大 75ch。数据表格可运行至 120ch+。

---

## 4. 布局结构

```
+---------------------------+----------------------------------------+
|   侧边栏 (260px)          |  TopBar (64px, 半透明 + blur)           |
|                           +----------------------------------------+
|   [D] DeepSeek Monitor    |  KICKER                                 |
|       USAGE & COST        |  页面标题（Lora）      范围 · 刷新 · 刷新 |
|                           |                                        |
|   MENU                    |  +------+ +------+ +------+ +------+  |
|   01 实时监测（激活）      |  | Stat | | Stat | | Stat | | Stat |  |
|   02 每日报告             |  +------+ +------+ +------+ +------+  |
|   03 每周报告             |                                        |
|   04 每月报告             |  +----------------------------------+  |
|   05 调度日志             |  | ChartCard（Kicker + Lora 标题）    |  |
|   06 设置                 |  +----------------------------------+  |
|                           |  +----------------------------------+  |
|   STATUS                  |                                        |
|   ● 已连接 · 1 Key        |                                        |
+---------------------------+----------------------------------------+
```

### 4.1 侧边栏

- 宽度 260px，固定；背景 `--color-surface`，右缘 1px `--color-border-subtle`。
- **品牌块（64px）**：32px 品牌色方块内 `--color-on-brand` 字 `D` + Lora 字标 `DeepSeek Monitor` + 10px mono 副标 `USAGE & COST`；右上角像素网格角标（`.corner-motif`），超出裁切。
- **MENU kicker**：11px mono 全大写，`--color-text-secondary`。
- **导航项**：`px-3 py-2.5`，14px Inter + 16px lucide 图标 + 右侧 `01–06` 两位数 mono 编号（10px）。
  - 激活：`--color-brand-subtle` 底、`--color-kicker` 文字、编号同色、字重 500。
  - 悬浮：`--color-surface-hover` 底、`--color-text-primary` 文字。
- **STATUS 页脚**：kicker + 8px 状态点 + mono note，`border-t` 发丝线。
- 导航顺序：实时监测 / 每日报告 / 每周报告 / 每月报告 / 调度日志 / 设置。

### 4.2 顶部栏

- 高度 64px，`sticky top-0`，`z-10`。
- **背景半透明**：`--color-bg-blur` + `backdrop-filter: blur(16px)`（全站唯一允许的毛玻璃区域）。
- 底部 1px `--color-border-subtle`；右侧叠放像素网格角标（`.corner-motif`，裁切）。
- 左侧：10px kicker（页面英文名，蓝）+ Lora 18px 页面标题。
- 右侧：时间范围下拉（`.input`，宽 112/128px）+ 自动刷新状态按钮（Ghost，12px，绿点/灰点）+ 主刷新按钮（Primary，含旋转图标）。

### 4.3 内容区

- 内边距 `16px`（`lg` 起 `24px`），垂直滚动。
- 页面根容器纵向间距 `24px`；卡片网格间距 `16px`。

### 4.4 响应式断点

| 断点 | 布局变化 |
|------|----------|
| ≥1400px | 4 列 StatCard，图表 2 列 |
| 960–1399px | 2 列 StatCard，图表 1–2 列 |
| 640–959px | 单列，侧边栏收起为汉堡菜单 |
| <640px | 单列，内容区 padding 缩至 16px |

### 4.5 装饰元素

| 元素 | 类名 | 规格 | 使用范围 |
|------|------|------|----------|
| 像素网格角标 | `.corner-motif` | 144×144 SVG data-URI 方块阵列，低透明度；浅色为蓝 `#4F8BFF` + 橙 `#F0876B`，深色为品牌绿 `#07C983` + 深绿 `#0E7A55`（整体 35% 不透明度） | 侧栏品牌块、顶栏右上角（各 ≤1 处/屏） |
| 卡片点阵 | `.card-dots` | 卡片右上角 42% × 44% 区域，1px 圆点 / 11px 网格 `radial-gradient`，遮罩 `to top right, transparent → #000 82%`（内侧渐隐、角部最密），`z-index:-1` 置于内容之下 | 实时监测 / 每日报告 / 每周报告 / 每月报告页的所有卡片 |
| 硬投影 | `--shadow-hard` | `4px 4px 0` 品牌色，深色主题用 `--color-brand-line` | 强调卡片，单页 ≤1 处 |

点阵为纯静态装饰：不参与交互、不响应 hover、不做动画，且不得覆盖文字（必须位于内容层之下）。

---

## 5. 页面规范

### 5.1 实时监测页 `/dashboard`

**功能目标**：展示当前 DeepSeek API 费用消耗的实时状态。

**区块 A — 统计卡片行（4 张，均带点阵）**

| 卡片 | 指标 | 格式 |
|------|------|------|
| 账户余额 | `total_balance` + 赠金/充值拆分 + `is_available` 状态 | `¥1,234.56`，子项 `赠金 ¥200.00` / `充值 ¥1,034.00`，状态点 `可用于调用` |
| 本月消费 | 当月累计 | `¥890.34` |
| 今日消费 | 今日累计 | `¥89.23` |
| 今日请求数 | 当日 `REQUEST` 求和（来自 key 排行） | `1,204` |

每张卡片结构：
- 顶部行：16px 语义色图标 + 11px 标签（`--color-text-secondary`，0.08em 字距）；右侧可选趋势（12px，语义色，箭头 + 百分比）
- 数值：28px Lora `--color-text-primary`，`tracking-tight`
- **子项列表**（可选，仅余额卡）：顶部 1px 发丝线，每行 label 左 / mono 数值右，12px
- **状态行**（可选，仅余额卡）：6px 圆点 + 12px 文案，`is_available` 为真用 `--color-success`，为假用 `--color-danger`
- 右上角点阵装饰（`.card-dots`）

**区块 B — 余额趋势图**
- 与区块 C 按 2 : 1 左右分栏（余额趋势占 2/3，模型分布占 1/3）
- Kicker `BALANCE TREND`，标题「余额趋势」（Lora 14px）
- 面积折线图，品牌色填充 15%
- 标题栏右侧：`期初 ¥x → 期末 ¥y` mono 元信息
- hover 显示十字准线 + 详细数据；快照含拆分时 tooltip 追加一行 `赠金 ¥x · 充值 ¥y`

**区块 C — 模型消费分布**
- Kicker `DISTRIBUTION`，标题「模型消费分布 (CNY)」
- 环形图，单色系明度阶梯（深色绿/浅色蓝）；中心显示总模型数；hover 显示模型名 + 百分比 + 金额
- 底部横向图例（色块 + 模型名 + 金额 + 占比），不显示环形外标注；0 值模型不进入图表

**区块 D — Key 使用与费用排行（全宽）**
- Kicker `RANKING`，单张全宽卡
- 范围分段控件：`今日 | 近 30 天 | 今年`（仅 Dashboard 显示，报告页由页面上下文锁定）
- 指标分段控件：`费用 | 请求数 | Token`，**默认费用**
- 其余规范见 §6.4

### 5.2 每日报告页 `/daily`

- 顶部：日期选择器（`.input`）+ mono 摘要行（消费 / 请求数 / Key 数）
- 4 张统计卡：当日消费、当日请求数、余额变动、活跃模型数
- 余额变化趋势（`BALANCE TREND`，**独占一行全宽**，带期初→期末元信息）
- 下方按 2 : 1 两列：
  - 消费类型明细（`COST BY TYPE`，占 2/3，横向柱状图）
  - 模型消费分布（`DISTRIBUTION`，占 1/3，环形图，底部横向图例）
- Key 排行（`DAILY RANKING`，范围锁定所选日期）
- 所有卡片带点阵装饰；不再展示「本月每日消费」图表（该视图移至每月报告）

### 5.3 每周报告页 `/weekly`

- 顶部：周选择器（`<input type="week">`）+ mono 摘要行（消费 / 请求数 / 模型数）
- 4 张统计卡：本周消费、日均消费、余额变动、本周请求数
- 每日消费趋势（`DAILY TREND`，占 2/3）
- 模型消费分布（`DISTRIBUTION`，占 1/3，中心显示活跃模型数，底部横向图例，不设独立卡片）
- Key 排行（`WEEKLY RANKING`，范围锁定所选周）
- 所有卡片带点阵装饰

### 5.4 每月报告页 `/monthly`

布局与每周报告保持一致：

- 顶部：月份选择器（`<input type="month">`）+ mono 摘要行（消费 / 请求数 / 模型数）
- 4 张统计卡：本月消费、日均消费、余额变动、本月请求数
- 消费趋势（`MONTHLY TREND`，按当月每日消费的直角柱状图，占 2/3）
- 模型消费分布（`DISTRIBUTION`，占 1/3，中心显示活跃模型数，底部横向图例）
- 两张图表左右两列展示，比例与每周报告一致
- Key 排行（`MONTHLY RANKING`，范围锁定所选月份）
- 所有卡片带点阵装饰

### 5.5 定时任务日志 `/scheduler-logs`

- 页头：kicker `SCHEDULER LOG` + Lora 标题「调度执行记录」+ 右侧刷新按钮
- DataTable（kicker `RECENT RUNS`）展示最近 10 次执行
- 列：状态（彩色圆点）、开始时间、结束时间、耗时、消息
- 不使用点阵装饰（保持工具页安静）

### 5.6 设置页 `/settings`

- 每个分区：kicker（`THEME` / `API KEYS` / `PLATFORM TOKEN` / `SYSTEM` / `STATUS`）+ Lora 16px 标题
- **API Key 管理**：添加/删除 Key，测试连接，状态显示
- **平台 Token**：输入 DeepSeek 平台 Bearer Token，测试 + 保存
- **系统配置**：自动刷新开关、刷新间隔、轮询间隔、数据保留天数、手动触发按钮
- **服务状态**：DeepSeek API 连接状态、调度器信息（下次运行、上次运行、状态）
- **主题切换**：浅色 / 深色分段控件（`.segmented`），选中态为实心 `--color-brand`；选择后持久化
- 不使用点阵装饰

---

## 6. 组件规范

所有交互组件定义以下状态：default、hover、focus、active、disabled、loading。所有矩形组件圆角为 `0`。

### 6.1 基础卡片

| 类名 | 样式 | 用途 |
|------|------|------|
| `.card` | `--color-surface` 底、1px `--color-border-subtle`、直角、无阴影 | 默认卡片 |
| `.card-raised` | `--color-surface-raised` 底、发丝线、浅阴影（仅浅色） | 浮层内容 |
| `.card-panel` | 2px `--color-border` 描边、直角 | 强调面板（少用） |
| `.card-dots` | 叠加 `.card` 使用：右上角点阵装饰（规格见 §4.5） | 四张数据页的所有卡片 |

### 6.2 StatCard

| 属性 | 值 |
|------|-----|
| 容器 | `.card .card-dots`，内边距 20px |
| 图标 | 16px lucide，语义色（默认品牌蓝），与标签同行 |
| 标签 | 11px Inter 500，`0.08em` 字距，`--color-text-secondary` |
| 趋势 | 12px，上升 `--color-success` / 下降 `--color-danger`，箭头 + 百分比 |
| 数值 | 28px **Lora 500**，`tracking-tight`，`--color-text-primary`，超长截断 |
| 子项列表 `details` | 可选 `[{label, value}]`；顶部 1px 发丝线，label `--color-text-secondary`、value `font-mono` + `tabular-nums` |
| 状态行 `status` | 可选 `{ok, text}`；6px 圆点 + 12px，真 `--color-success` / 假 `--color-danger` |

无侧条纹边框。无渐变。图标块不再使用大色块，仅保留 16px 彩色线性图标。

### 6.3 ChartCard

| 属性 | 值 |
|------|-----|
| 容器 | `.card .card-dots`，直角 |
| 标题栏 | `px-5 pt-4 pb-3`，底部 1px 发丝线 |
| Kicker | 10px Roboto Mono 500 全大写 `0.14em`，`--color-kicker` |
| 标题 | 14px **Lora 500**，`tracking-tight` |
| 右上操作区 | 可选 slot，12px mono 元信息或分段按钮 |
| 图表区 | 内边距 4px，默认高度 320px（本页统一 360px） |
| 空态 | 居中「暂无数据」，`--color-text-tertiary` |
| 坐标轴 | 11px，轴线 `--color-border-subtle`，标签 `--color-text-tertiary`，网格虚线 `--color-border-subtle` |
| Tooltip | `--color-surface-raised` 底、1px `--color-border`、12px 文本 |
| 环形图图例 | 底部横向：8×8px 方形色块 + 模型名 + 金额 + 占比；11px Roboto Mono，`--color-text-secondary`；窄容器自动换行，系列 >4 时改为滚动翻页；隐藏环形外标注与引导线；小于 0.005 的模型不展示 |
| 环形图中心 | 可选 20px Roboto Mono 粗体数字（如活跃模型数），`--color-text-primary`，垂直居中于环心 |

### 6.4 KeyRanking（排行表）

| 属性 | 值 |
|------|-----|
| 容器 | `.card .card-dots`，内边距 20px，全宽 |
| 标题区 | Kicker（默认 `KEY RANKING`）+ Lora 14px 标题；右侧两组分段控件 |
| 分段控件 `.segmented` | 1px `--color-border` 外框、直角、无内衬；按钮 5px 10px、11px Roboto Mono 500、`0.06em`；相邻按钮以 1px 发丝线分隔 |
| 分段激活态 | 实心 `--color-brand` 底 + `--color-on-brand` 文字（深色主题为近黑字） |
| 分段禁用态 | `--color-text-tertiary` + `not-allowed` |
| 过渡 | 仅 `background-color` / `color`，150ms `ease-out` |
| 表头 | 10px Roboto Mono 500 全大写 `0.12em`；当前排序指标列 `--color-kicker`，其余 `--color-text-secondary`；底部发丝线 |
| 行 | 底部 `--color-border-subtle`，末行无；hover `--color-surface-hover`；单元格 `8px 12px` |
| 数值列 | `font-mono` + `tabular-nums`，右对齐 |
| 占比条 | 96×6px，**直角**；底 `--color-border-subtle`，填充 `--color-chart-1`；百分比 12px 右对齐 |
| 排名列 | 当前指标下第 1 名 `--color-warning`，第 2–3 名 `--color-text-primary` 加粗，其余 `--color-text-secondary` |
| 占比口径 | 个人值 ÷（同范围 + 同指标所有人合计）× 100%，各行加总 ≈ 100% |
| 降级态 | 该范围无费用数据时，费用列显示 `—`、费用按钮禁用、标题旁 mono note「费用数据采集中」，排序回落到请求数；数据到达后自动恢复费用 |
| 空态 | 居中「暂无使用数据」 |

### 6.5 DataTable

| 属性 | 值 |
|------|-----|
| 容器 | `.card`（不使用点阵） |
| 标题栏 | `px-5 pt-4 pb-3` + 底部发丝线；可选 kicker + Lora 14px 标题 |
| 表头 | 10px Roboto Mono 500 全大写 `0.12em`，`--color-text-secondary`，底部 `--color-border-subtle` |
| 行 | 1px 顶部发丝线，hover `--color-surface-hover` |
| 单元格 | `12px 20px`，正文 14px |
| 空态 | 居中提示文字 |

### 6.6 Button

| 变体 | 背景 | 文字 | 描边 | Hover |
|------|------|------|------|-------|
| Primary `.btn-primary` | `--color-brand` | `--color-on-brand` | 2px `--color-brand` | `--color-brand-hover` |
| Secondary `.btn-secondary` | `--color-surface-raised` | `--color-text-primary` | 2px `--color-border` | `--color-surface-hover` |
| Ghost `.btn-ghost` | 透明 | `--color-kicker` | 无 | `--color-brand-subtle` 底 |
| Danger `.btn-danger` | `--color-danger` | 白 | 2px `--color-danger` | 亮度 94% |

- 全部直角，内边距 `7px 14px`，13px / 500； **Secondary 使用 Roboto Mono**（Bifrost 特征）。
- 品牌色上的文字统一用 `--color-on-brand`：浅色主题为白字，深色主题（品牌绿）为近黑字，保证对比度。
- 焦点态：`0 0 0 2px surface, 0 0 0 4px brand` 双层焦点环。
- 禁用态：50% 不透明度 + `not-allowed`。

### 6.7 Tag

| 类型 | 背景 | 文字 |
|------|------|------|
| Neutral `.tag` | `--color-surface-hover` | `--color-text-secondary` |

- 1px `--color-border` 描边、直角，内边距 `2px 8px`，11px Roboto Mono 500，`0.06em` 字距。
- 语义色标签用 12%–15% 语义色底 + 语义色文字（`success-subtle` / `neutral-subtle` 等 token）。

### 6.8 Input / Select

| 属性 | 值 |
|------|-----|
| 背景 | `--color-surface` |
| 边框 | 1px `--color-border`，直角 |
| 内边距 | `8px 12px` |
| 文字 | 13px，`--color-text-primary` |
| 占位符 | `--color-text-tertiary` |
| 焦点态 | border `--color-brand` + 双层焦点环 |
| 禁用态 | `--color-text-tertiary`，`--color-border-subtle` |

### 6.9 Switch

| 属性 | 值 |
|------|-----|
| 轨道 | 36×20px，`--color-border` 背景 / 激活 `--color-brand`（轨道为胶囊形，属圆形例外） |
| 滑块 | 16px 正圆，白色 |
| 过渡 | 200ms ease，仅平移 transform |

### 6.10 StatusIndicator

| 属性 | 值 |
|------|-----|
| 圆点 | 8px，语义色 |
| 标签 | 12px，`--color-text-secondary` |
| 间距 | 8px |

### 6.11 Kicker / Note

| 类名 | 规格 | 用途 |
|------|------|------|
| `.kicker` | 11px Roboto Mono 500、`0.14em`、全大写、`--color-kicker` | 页面/卡片眉标（英文） |
| `.note` | 11px Roboto Mono 500、`0.04em`、`--color-text-tertiary` | 静默元信息、状态说明 |

Kicker 文本使用简短英文（如 `MONITOR`、`BALANCE TREND`、`RANKING`），中文标题由 Lora 承担。

### 6.12 Skeleton Loading

| 属性 | 值 |
|------|-----|
| 背景 | `--color-surface-hover` |
| 动画 | 伪元素渐变扫光，1.5s 无限线性 |
| 形状 | 匹配内容块轮廓（卡片轮廓 / 文字行块），直角 |

---

## 7. 交互规范

| 交互 | 行为 |
|------|------|
| **自动刷新** | 启动后按间隔轮询 API，页面数据平滑更新；页面不可见时暂停 |
| **手动刷新** | 点击刷新按钮触发强制轮询，图标旋转至响应返回（仅旋转 transform） |
| **图表悬浮** | 面积图/柱状图 hover 显示十字准线 + 数据标签 |
| **时间范围** | 切换时重新请求后端数据，保持当前页面不刷新 |
| **主题切换** | 设置页切换浅色/深色，通过 `class="dark"` 切换，结果存入 `localStorage.theme` |
| **空状态** | 首次使用显示居中图标 + "开始监测"引导按钮 |
| **错误状态** | API 异常时卡片显示错误遮罩 + "重试"按钮，不影响其他卡片 |
| **响应式** | 侧边栏 <640px 时收起为汉堡菜单；卡片网格自适应列数 |
| **焦点可见** | 键盘焦点统一使用双层焦点环，禁止 `outline: none` 后无替代 |

### Motion 规范

| 场景 | 时长 | 缓动曲线 |
|------|------|----------|
| Hover / Focus | 150ms | `ease-out` |
| 面板显隐 / 骨架→内容 | 200ms | `cubic-bezier(.22,1,.36,1)` |
| 路由切换 | 150ms | `ease`（仅淡入淡出） |

**规则**：
- 禁止动画化 CSS 布局属性（width, height, top, left, margin, padding）
- 点阵、像素角标等装饰元素不参与动画
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
| 图表 | ECharts 5 + vue-echarts 7 | 色板读取 CSS 变量 |
| 样式 | Tailwind CSS 3 | 直角预设：`borderRadius` sm/md/lg/xl = 0 |
| 字体 | Inter / Lora / Roboto Mono | Google Fonts，`index.html` 预加载 |
| 图标 | lucide-vue-next | 线性图标 16px |
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
| GET | `/api/v1/usage/cost` | 消耗数据（按日/按模型原始明细） |
| GET | `/api/v1/usage/cost/weekly?year=&week=` | 周度汇总 `{total_cost, daily_avg_cost, daily_breakdown[], model_breakdown[], balance_*, active_models}` |
| GET | `/api/v1/usage/cost/monthly?year=&month=` | 月度汇总（结构同周度汇总） |
| GET | `/api/v1/usage/balance/latest` | 最新余额快照（含赠金 / 充值 / 可用状态） |
| GET | `/api/v1/usage/key-rankings` | Key 排行：`{today, year, last_30_days}`，每项 `{items[], cost_available}`；item 含 `cost` |
| GET | `/api/v1/usage/key-rankings/daily?date=` | 单日 Key 排行 `{items[], cost_available}` |
| GET | `/api/v1/usage/key-rankings/weekly?year=&week=` | 单周 Key 排行 `{items[], cost_available}` |
| GET | `/api/v1/usage/key-rankings/monthly?year=&month=` | 单月 Key 排行 `{items[], cost_available}` |
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
| `/monthly` | 每月报告 | MonthlyReport |
| `/scheduler-logs` | 调度日志 | SchedulerLogs |
| `/settings` | 设置 | Settings |

---

## 11. 绝对禁止模式

以下模式在任何主题下均禁止出现（标注「例外」的条目按受限条件执行）：

- **侧条纹边框**：`border-left` / `border-right` > 1px 作为彩色装饰条。
- **圆角**：矩形组件出现大于 0 的圆角。例外：状态圆点、Switch 滑块/轨道、进度圆环等本质为圆的元件。
- **渐变文字**：`background-clip: text` + 渐变背景。
- **毛玻璃滥用**：除顶栏（半透明 + `blur(16px)`）外，任何大面积 `backdrop-filter` 均禁止。例外：顶栏，且必须有 1px 发丝线收边。
- **软阴影堆叠**：卡片默认禁止多层柔光阴影。例外：浅色主题下浮层（tooltip/弹窗）允许单层浅阴影；深色主题一律无阴影。
- **英雄指标模板**：大数字 + 小标签 + 渐变强调的 SaaS 风格指标卡。例外：StatCard 允许 Lora 大数字，但不得使用渐变、发光或彩色描边。
- **展示字体越界**：Lora 只允许用于页面标题、块标题、卡片标题、统计卡大数字。按钮、导航、标签、表格、正文、工具提示一律禁止衬线体。
- **相同卡片网格**：重复的图标 + 标题 + 正文卡片排列。
- **模态框优先**：未穷尽内联/渐进方案前使用弹窗。
- **装饰动效**：点阵、像素角标、硬投影等装饰元素出现动画或 hover 反应。
- **点阵干扰内容**：点阵不得位于文字/图表上方，不得提高不透明度至影响可读性，不得出现在设置页与调度日志页卡片上。
- **组件不一致**：不同页面出现不同样式的同类组件。
- **自定义标准控件**：自定义滚动条、非标准表单控件、非常规弹窗。

---

## 附录 A：设计文件索引

| 文件 | 用途 |
|------|------|
| `PRODUCT.md` | 产品策略、用户画像、品牌个性 |
| `DESIGN.md` | 设计令牌完整定义（色值、间距、阴影、动效曲线） |
| `UI_SPECIFICATION.md` | 本文档 — UI 规范和页面规范 |

*设计令牌以 `frontend/src/style.css` 的 CSS 变量为运行时事实来源；本文档与 DESIGN.md 中的色值为规范参考。*

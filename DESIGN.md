# DeepSeek Monitor — Design System

## Theme Philosophy

Two themes, one intent: get the user to the number.

The visual language is **warm-paper editorial** (main reference: `bifrost.ai`): warm paper canvas, white panels, hairline rules, sharp corners, 2px frames, mono labels, serif display type. A dot-matrix corner motif and a translucent top bar are borrowed from `spom-park-ai-agent.netlify.app` as restrained decoration.

**Light** — warm paper, white panels, ink-dark type, blue kickers. For daytime review and shared screens.

**Dark** — near-black canvas `#090D0D` with Bifrost-docs green accent `#07C983`; body text `#9EA0A0`, emphasized text `#EEEFF0`. Same geometry and component rules, no shadows. For prolonged monitoring sessions.

Both themes share the same typography, spacing scale, component vocabulary, and interaction patterns. Only color changes.

---

## Color

All values are CSS custom properties on `:root` (light) and `.dark` (dark). Hex is the runtime source of truth; no hardcoded hex outside the token block.

### Strategy

**Restrained** — warm neutrals + one accent at ≤10% of surface area. Charts may carry committed brand color within a single card, but the page stays restrained.

### Light Theme (warm paper)

| Token | Hex | Role |
|-------|-----|------|
| `--color-bg` | `#FCFBF8` | Page canvas (warm paper) |
| `--color-surface` | `#FFFFFF` | Card, panel, sidebar |
| `--color-surface-hover` | `#F5F7FA` | Hover state, table header, tag bg |
| `--color-surface-raised` | `#FEFDFB` | Secondary button, popover |
| `--color-border` | `#C7D3E8` | 2px frames, input border |
| `--color-border-subtle` | `#E6EBF1` | Hairlines (card border, table rows) |
| `--color-hairline` | `#F5F7FA` | Extra-light divider |
| `--color-text-primary` | `#0B1220` | Headings, values, nav |
| `--color-text-secondary` | `#475467` | Labels, descriptions |
| `--color-text-tertiary` | `#96A0B0` | Placeholder, disabled, axes |
| `--color-brand` | `#4F8BFF` | Primary accent, primary button |
| `--color-brand-hover` | `#3D7FF0` | Brand hover |
| `--color-brand-subtle` | `#EEF4FF` | Active nav bg, light tint |
| `--color-brand-line` | `#A8C8FC` | Light blue line |
| `--color-kicker` | `#2E6BE0` | Kicker text, ghost button |
| `--color-success` | `#22C55E` | Healthy / connected |
| `--color-warning` | `#F59E0B` | Near threshold, rank 1 |
| `--color-danger` | `#EF4444` | Error, over limit |
| `--color-bg-blur` | `rgba(252,251,248,.80)` | Top bar translucent fill |
| `--color-success-subtle` | `rgba(34,197,94,.12)` | Success tint |
| `--color-neutral-subtle` | `rgba(150,160,176,.16)` | Neutral tint |
| `--color-dot` | `rgba(79,139,255,.20)` | Card dot-matrix decoration |
| `--color-on-brand` | `#FFFFFF` | Text on brand fills |

### Dark Theme (Bifrost docs palette)

Dark colors follow `docs.getbifrost.ai`: near-black canvas `#090D0D`, brand green `#07C983`, body text `#9EA0A0`, emphasized text `#EEEFF0`. Surfaces and borders are derived from that base; layout and border widths are unchanged.

| Token | Hex | Role |
|-------|-----|------|
| `--color-bg` | `#090D0D` | Page canvas |
| `--color-surface` | `#161919` | Card, panel, sidebar |
| `--color-surface-hover` | `#1F2222` | Hover state |
| `--color-surface-raised` | `#222525` | Secondary button, popover |
| `--color-border` | `#2A2D2D` | 2px frames, input border |
| `--color-border-subtle` | `#1E2121` | Hairlines |
| `--color-hairline` | `#191C1C` | Extra-light divider |
| `--color-text-primary` | `#EEEFF0` | Headings, values, nav (emphasized text) |
| `--color-text-secondary` | `#9EA0A0` | Labels, descriptions (body text) |
| `--color-text-tertiary` | `#707172` | Placeholder, disabled, axes |
| `--color-brand` | `#07C983` | Primary accent, buttons, share bar |
| `--color-brand-hover` | `#06B877` | Brand hover |
| `--color-brand-subtle` | `rgba(7,201,131,.12)` | Active nav bg |
| `--color-brand-line` | `#0E7A55` | Hard-shadow mapping |
| `--color-kicker` | `#07C983` | Kicker text, ghost button |
| `--color-on-brand` | `#08110E` | Text on brand fills (must be dark) |
| `--color-success` | `#34D399` | Healthy / connected |
| `--color-warning` | `#FBBF24` | Near threshold, rank 1 |
| `--color-danger` | `#F87171` | Error, over limit |
| `--color-bg-blur` | `rgba(9,13,13,.80)` | Top bar translucent fill |
| `--color-success-subtle` | `rgba(52,211,153,.15)` | Success tint |
| `--color-neutral-subtle` | `rgba(158,160,160,.18)` | Neutral tint |
| `--color-dot` | `rgba(7,201,131,.18)` | Card dot-matrix decoration |

### Chart palette (dark / light orders)

| # | Dark | Light |
|---|------|-------|
| 1 (brand) | `#07C983` | `#4F8BFF` |
| 2 | `#60A5FA` | `#22C55E` |
| 3 (warning) | `#FBBF24` | `#F59E0B` |
| 4 (danger) | `#F87171` | `#EF4444` |
| 5 (purple) | `#A78BFA` | `#8B5CF6` |
| 6 (pink) | `#F472B6` | `#E879A8` |
| 7 | `#34D399` | `#60A5FA` |

Area fills at 15% opacity. Bars are square (`borderRadius: 0`) with no gradient.

---

## Typography

### Font stacks

```css
--font-display: 'Lora', Georgia, 'Times New Roman', serif;
--font-sans:    'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
--font-mono:    'Roboto Mono', 'JetBrains Mono', 'Fira Code', 'SF Mono', ui-monospace, monospace;
```

- **Lora** — page titles, section titles, card titles, and stat-card hero numbers only.
- **Inter** — everything else (body, labels, nav, buttons).
- **Roboto Mono** — kickers, notes, table headers, data values, secondary buttons.

### Scale

| Token | Size | Weight | Tracking | Font | Use |
|-------|------|--------|----------|------|-----|
| Kicker | 11px | 500 | 0.14em uppercase | Mono | Blue eyebrow labels |
| Note | 11px | 500 | 0.04em | Mono | Quiet metadata |
| Page title | 18px | 500 | tight | Lora | Top bar H1 |
| Section title | 16px | 500 | tight | Lora | Settings H2 |
| Card title | 14px | 500 | tight | Lora | Card H3 |
| Stat value | 28px | 500 | tight | Lora | Stat card number |
| Body | 14px | 400 | — | Inter | Body, tables, nav |
| Small | 12px | 400 | — | Inter | Auxiliary, trends |
| Stat label | 11px | 500 | 0.08em | Inter | Stat card label |
| Table head | 10px | 500 | 0.12em uppercase | Mono | Headers, segmented buttons |
| Button | 13px | 500 | — | Inter | Button label (secondary: Mono) |

### Numbers

Stat-card hero numbers use **Lora**. All other numbers (tables, detail lists, tooltips, share percentages) use `--font-mono` with `font-variant-numeric: tabular-nums`.

### Line length

Body containers capped at 75ch. Data tables exempt (120ch+).

---

## Spacing

| Token | Rem | Px | Use |
|-------|-----|----|-----|
| `--space-1` | 0.25rem | 4 | Tight inner padding |
| `--space-2` | 0.5rem | 8 | Icon gaps |
| `--space-3` | 0.75rem | 12 | Segmented/button padding |
| `--space-4` | 1rem | 16 | Card grid gap, mobile padding |
| `--space-5` | 1.25rem | 20 | Card padding |
| `--space-6` | 1.5rem | 24 | Desktop content padding, page section gap |
| `--space-8` | 2rem | 32 | Section spacing |

### Grid

Content area padding: 16px (mobile) / 24px (`lg`). Card grid gap: 16px. Page section gap: 24px.

---

## Border Radius

**All rectangular UI is square** — Tailwind `borderRadius` sm/md/lg/xl are mapped to `0px`.

| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | 0px | Tags, buttons, inputs |
| `--radius-md` | 0px | Buttons, inputs, segmented control |
| `--radius-lg` | 0px | Cards, panels |
| `--radius-xl` | 0px | Panels |

Only inherently circular elements (status dots, switch track/thumb, donut rings) are round.

---

## Shadows

### Dark theme

No shadows at all. Elevation via surface lightness: `--color-surface` → `--color-surface-hover` → `--color-surface-raised`.

### Light theme

| Elevation | Shadow |
|-----------|--------|
| Card (default) | none (hairline border only) |
| Raised / popover | `0 1px 10px rgba(11,18,32,.06)` |
| Modal | `0 8px 24px rgba(11,18,32,.10), 0 1px 3px rgba(11,18,32,.06)` |
| Emphasis (both themes) | hard shadow `4px 4px 0` brand (`--shadow-hard`) |

### Focus ring

```
0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand)
```

Two-tier ring: a surface-colored gap, then a brand ring. Used on all interactive elements.

---

## Components

Every interactive component defines: default, hover, focus, active, disabled, loading.

### Card

| Class | Spec |
|-------|------|
| `.card` | `--color-surface` bg, 1px `--color-border-subtle`, square, no shadow |
| `.card-raised` | `--color-surface-raised` bg, hairline, light shadow (light theme only) |
| `.card-panel` | 2px `--color-border` frame, square |
| `.card-dots` | Card + top-right dot-matrix decoration (see Decoration) |

### Sidebar

- Width: 260px, fixed; `--color-surface` bg; right hairline
- Brand block: 64px — 32px brand-colored square with `--color-on-brand` `D`, Lora wordmark, 10px mono caption `USAGE & COST`, pixel-grid corner motif clipped
- `MENU` kicker, then nav items with 16px lucide icon + label + right-aligned two-digit mono index (`01`–`05`)
- Active item: `--color-brand-subtle` bg, `--color-kicker` text, weight 500
- Hover item: `--color-surface-hover`
- Footer: `STATUS` kicker + status dot + mono note
- No side-stripe borders

### TopBar

- Height: 64px, `sticky top-0`, `z-10`
- Background: `--color-bg-blur` + `backdrop-filter: blur(16px)` — the only permitted glass surface
- Bottom border: 1px `--color-border-subtle`
- Pixel-grid corner motif at top-right, clipped
- Left: 10px kicker + Lora 18px page title
- Right: time-range `.input` select + auto-refresh ghost button + primary refresh button

### StatCard

- `.card .card-dots`, padding 20px
- 16px semantic-colored lucide icon + 11px label (0.08em tracking)
- Value: 28px Lora 500, `tracking-tight`
- Optional trend: 12px, success/danger with arrow
- Optional `details` sublist: hairline top border, mono tabular values
- Optional `status`: 6px dot + 12px text
- No icon color block, no gradient, no side stripe

### ChartCard

- `.card .card-dots`
- Header: `px-5 pt-4 pb-3`, hairline bottom; 10px kicker + 14px Lora title; optional actions slot
- Chart area: 4px inset, default height 320px
- Empty state: centered `暂无数据` in `--color-text-tertiary`

### KeyRanking

- `.card .card-dots`, padding 20px, full width
- Kicker + Lora title; two segmented groups (range, metric)
- Segmented control: 1px `--color-border` frame, square, no inner padding; buttons 5px 10px, 11px mono 500, 0.06em; active = solid `--color-brand` + `--color-on-brand`; disabled = tertiary text
- Table: 10px mono uppercase headers (0.12em), active metric column in `--color-kicker`
- Rows: hairline separators, hover `--color-surface-hover`
- Share bar: 96×6px square, track `--color-border-subtle`, fill `--color-chart-1`
- Rank: 1st `--color-warning`, 2nd–3rd primary bold, rest secondary
- Share denominator: total of all keys in the same range + metric

### DataTable

- `.card` (no dots), header `px-5 pt-4 pb-3` with optional kicker + Lora title
- 10px mono uppercase headers, hairline bottom
- Rows: hairline separators, hover `--color-surface-hover`, cell padding `12px 20px`
- Empty state: centered text

### Button

| Variant | Background | Text | Border | Hover |
|---------|-----------|------|--------|-------|
| Primary `.btn-primary` | `--color-brand` | `--color-on-brand` | 2px brand | `--color-brand-hover` |
| Secondary `.btn-secondary` | `--color-surface-raised` | `--color-text-primary` | 2px `--color-border` | `--color-surface-hover` |
| Ghost `.btn-ghost` | transparent | `--color-kicker` | none | `--color-brand-subtle` bg |
| Danger `.btn-danger` | `--color-danger` | white | 2px danger | brightness 94% |

All: square, padding `7px 14px`, 13px / 500. Secondary uses Roboto Mono. Focus: two-tier ring. Disabled: 50% opacity.

### Tag

- 1px `--color-border`, square, padding `2px 8px`, 11px Roboto Mono 500, 0.06em
- Neutral: `--color-surface-hover` bg, `--color-text-secondary` text
- Semantic: 12–15% semantic tint + semantic text

### Input / Select

- Background `--color-surface`, 1px `--color-border`, square, padding `8px 12px`
- Text 13px `--color-text-primary`; placeholder tertiary
- Focus: brand border + two-tier focus ring
- Disabled: tertiary text, subtle border

### Switch (toggle)

- Track: 36×20px, `--color-border` bg; active `--color-brand` (pill shape is an allowed circle exception)
- Thumb: 16px white circle
- Transition: 200ms ease, translate transform only

### StatusIndicator

- Dot: 8px semantic circle
- Label: 12px `--color-text-secondary`
- Gap: 8px

### Kicker / Note

- `.kicker`: 11px Roboto Mono 500, 0.14em, uppercase, `--color-kicker`
- `.note`: 11px Roboto Mono 500, 0.04em, `--color-text-tertiary`

---

## Decoration

| Element | Class | Spec | Where |
|---------|-------|------|-------|
| Pixel-grid corner | `.corner-motif` | 144×144 SVG data-URI squares at low opacity; light: blue `#4F8BFF` + orange `#F0876B`; dark: brand green `#07C983` + deep green `#0E7A55` (35% opacity) | Sidebar brand block, top bar right |
| Card dot matrix | `.card-dots` | Top-right 42%×44%, 1px dots on an 11px grid (`radial-gradient`), mask `to top right, transparent → #000 82%`; `z-index:-1` under content | All cards on dashboard / daily / weekly |
| Hard shadow | `--shadow-hard` | `4px 4px 0` brand (brand-line in dark) | At most one emphasis surface per page |

Decoration is static: no animation, no hover behavior, never above content, never on Settings or Scheduler Logs cards.

---

## Motion

### Durations

- Micro-interactions (hover, focus, toggle): 150ms
- State changes (panel show/hide, skeleton→content): 200ms
- Route fade: 150ms

### Curves

- Entrance/exit (panels): `cubic-bezier(.22,1,.36,1)`
- Micro-interactions: `ease-out`

### Rules

- Never animate CSS layout properties (width, height, top, left, margin, padding)
- No orchestrated page-load sequences
- Motion conveys state only; decorations never animate
- `prefers-reduced-motion: reduce` → all transitions and animations to 0ms

### Skeleton loading

- Background `--color-surface-hover`, gradient shimmer via pseudo-element
- 1.5s, infinite, linear; square shapes matching content blocks

---

## Charts (ECharts theme)

Central `useChartTheme` composable resolves colors from CSS custom properties, so both themes stay in sync automatically.

| Property | Value |
|----------|-------|
| background | transparent |
| tooltip bg | `--color-surface-raised` |
| tooltip border | `--color-border`, 1px |
| tooltip text | `--color-text-primary`, 12px |
| axis line | `--color-border-subtle` |
| axis label | `--color-text-tertiary`, 11px |
| split line | `--color-border-subtle`, dashed |
| grid | `{ top: 24, right: 24, bottom: 32, left: 64 }` |
| area fill | series color at 15% |
| bars | square corners, max width 32px |

Series colors: `--color-chart-1` … `--color-chart-7` in order. No gradient fills.

---

## Layout

### Page shell

```
+---------------------------+----------------------------------------+
|                           |  TopBar (64px, translucent + blur)      |
|   Sidebar (260px)         +----------------------------------------+
|                           |                                        |
|   [D] DeepSeek Monitor    |  KICKER                                 |
|       USAGE & COST        |  Page title (Lora)    range · refresh   |
|                           |                                        |
|   MENU                    |  +------+ +------+ +------+ +------+   |
|   01 实时监测 (active)     |  | Stat | | Stat | | Stat | | Stat |   |
|   02 每日报告             |  +------+ +------+ +------+ +------+   |
|   03 每周报告             |                                        |
|   04 调度日志             |  +----------------------------------+   |
|   05 设置                 |  | ChartCard (kicker + Lora title)   |   |
|                           |  +----------------------------------+   |
|   STATUS                  |                                        |
|   ● 已连接 · 1 Key        |                                        |
+---------------------------+----------------------------------------+
```

### Responsive breakpoints

| Breakpoint | Layout |
|------------|--------|
| ≥1400px | 4-column stat grid, 2-column chart grid |
| 960–1399px | 2-column stat grid, 1–2 column charts |
| 640–959px | Single column, sidebar collapsed (hamburger) |
| <640px | Single column, 16px content padding |

---

## Theme switching

- Tokens on `:root` (light) and `.dark` (dark).
- First visit with no stored theme follows `prefers-color-scheme`.
- Manual choice writes `localStorage.theme` and toggles `class="dark"` on `<html>`.
- `?theme=dark` forces dark for preview/screenshots without persisting.

---

## Bans

- **No side-stripe borders** (`border-left`/`border-right` >1px as accent)
- **No rounded rectangles** — square corners everywhere; only inherently circular elements are round
- **No gradient text**
- **No glassmorphism outside the top bar** — any other large `backdrop-filter` is banned
- **No stacked soft shadows** — cards use hairlines; dark theme has no shadows
- **No hero-metric template** with gradients/glow; Lora stat numbers are allowed
- **No display fonts outside titles and stat numbers** — Lora never in buttons, labels, tables, tooltips
- **No identical card grids** — vary content, don't repeat icon+heading+body
- **No modal as first thought**
- **No decorative motion** — including animated dot matrices or pixel motifs
- **Dots must stay behind content** and must not reduce readability
- **No inconsistent component vocabulary**
- **No reinventing standard affordances** — standard scrollbars, form controls, modals

---

## Implementation

All tokens are CSS custom properties defined in `frontend/src/style.css`:

```css
:root { /* light theme */ }
.dark { /* dark theme */ }
```

Tailwind `theme.extend` maps semantic names (`bg`, `surface`, `text-*`, `brand`, `chart-*`, `kicker`, `translucent`, …) directly to these variables. Component classes (`.card`, `.btn-*`, `.input`, `.tag`, `.kicker`, `.note`, `.segmented`, `.corner-motif`, `.card-dots`) live in the same file under `@layer components`.

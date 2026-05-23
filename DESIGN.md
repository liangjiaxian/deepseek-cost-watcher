# DeepSeek Monitor — Design System

## Theme Philosophy

Two themes, one intent: get the user to the number. Neither theme is a default; the user chooses based on context.

**Dark** is for flow — prolonged sessions, low-light environments, operational monitoring. The surface recedes; the data advances. Chroma is restrained; contrast comes from value, not saturation.

**Light** is for context — daytime review, shared screens, morning standups. Warm neutrals keep it approachable without sacrificing seriousness. Brand presence is lighter; data still leads.

Both themes share the same typography, spacing scale, component vocabulary, and interaction patterns. Only color changes.

---

## Color

OKLCH throughout. No `#000` or `#fff`. Neutrals are tinted toward brand hue at very low chroma (`oklch(… 0.006 260)`).

### Strategy

**Restrained** — tinted neutrals + one accent at ≤10% of surface area. The dashboard earns committed moments per-surface: a chart's accent color may carry 30% of that card's area, but the page as a whole stays restrained.

### Dark Theme

| Token | OKLCH | Hex | Role |
|-------|-------|-----|------|
| `--bg` | `oklch(0.10 0.012 260)` | `#0F1118` | Page canvas |
| `--surface` | `oklch(0.15 0.014 260)` | `#1A1D28` | Card, panel, sidebar |
| `--surface-hover` | `oklch(0.18 0.016 258)` | `#222536` | Hovered card, dropdown |
| `--surface-raised` | `oklch(0.20 0.018 256)` | `#292D3E` | Modal, popover, tooltip bg |
| `--border` | `oklch(0.23 0.015 258)` | `#2E3242` | Card borders, dividers |
| `--border-subtle` | `oklch(0.18 0.010 260)` | `#252838` | Lighter dividers (table rows) |
| `--text-primary` | `oklch(0.92 0.008 260)` | `#EFF3F7` | Headings, values, nav labels |
| `--text-secondary` | `oklch(0.65 0.018 255)` | `#94A3B8` | Labels, descriptions, meta |
| `--text-tertiary` | `oklch(0.45 0.020 255)` | `#64748B` | Placeholder, disabled |
| `--brand` | `oklch(0.55 0.18 260)` | `#4F8CFF` | Primary accent, buttons, links |
| `--brand-hover` | `oklch(0.50 0.20 258)` | `#3A73E0` | Brand hover |
| `--brand-subtle` | `oklch(0.22 0.08 260)` | `#1E3A6E` | Brand bg tint (badges, pills) |
| `--success` | `oklch(0.65 0.18 165)` | `#34D399` | Healthy / connected |
| `--warning` | `oklch(0.75 0.16 85)` | `#FBBF24` | Near threshold |
| `--danger` | `oklch(0.65 0.20 25)` | `#F87171` | Error, over limit |
| `--chart-1` | `oklch(0.55 0.18 260)` | `#4F8CFF` | Chart series 1 (brand) |
| `--chart-2` | `oklch(0.65 0.18 165)` | `#34D399` | Chart series 2 |
| `--chart-3` | `oklch(0.75 0.16 85)` | `#FBBF24` | Chart series 3 |
| `--chart-4` | `oklch(0.65 0.20 25)` | `#F87171` | Chart series 4 |
| `--chart-5` | `oklch(0.55 0.18 290)` | `#A78BFA` | Chart series 5 |
| `--chart-6` | `oklch(0.60 0.18 340)` | `#F472B6` | Chart series 6 |
| `--chart-7` | `oklch(0.60 0.15 220)` | `#60A5FA` | Chart series 7 |

### Light Theme

Same structural tokens. Warm neutrals with lower contrast ratios than dark (ambient light compensates).

| Token | OKLCH | Hex | Role |
|-------|-------|-----|------|
| `--bg` | `oklch(0.97 0.006 260)` | `#F6F8FB` | Page canvas |
| `--surface` | `oklch(0.94 0.008 260)` | `#EEF1F5` | Card, panel, sidebar |
| `--surface-hover` | `oklch(0.91 0.010 258)` | `#E5E9EF` | Hovered card, dropdown |
| `--surface-raised` | `oklch(0.99 0.004 260)` | `#FCFDFD` | Modal, popover, tooltip bg |
| `--border` | `oklch(0.85 0.012 258)` | `#D5DAE2` | Card borders, dividers |
| `--border-subtle` | `oklch(0.90 0.008 260)` | `#E2E6ED` | Lighter dividers (table rows) |
| `--text-primary` | `oklch(0.18 0.015 260)` | `#1E2233` | Headings, values, nav labels |
| `--text-secondary` | `oklch(0.48 0.018 258)` | `#5F6B80` | Labels, descriptions, meta |
| `--text-tertiary` | `oklch(0.65 0.015 258)` | `#909DAE` | Placeholder, disabled |
| `--brand` | `oklch(0.50 0.19 260)` | `#3B82F6` | Primary accent, buttons, links |
| `--brand-hover` | `oklch(0.45 0.21 258)` | `#2563EB` | Brand hover |
| `--brand-subtle` | `oklch(0.85 0.08 260)` | `#DBE8FF` | Brand bg tint (badges, pills) |
| `--success` | `oklch(0.55 0.18 165)` | `#22B572` | Healthy / connected |
| `--warning` | `oklch(0.70 0.16 85)` | `#E5A000` | Near threshold |
| `--danger` | `oklch(0.55 0.20 25)` | `#DC4C4C` | Error, over limit |
| `--chart-1` | `oklch(0.50 0.19 260)` | `#3B82F6` | Chart series 1 |
| `--chart-2` | `oklch(0.55 0.18 165)` | `#22B572` | Chart series 2 |
| `--chart-3` | `oklch(0.70 0.16 85)` | `#E5A000` | Chart series 3 |
| `--chart-4` | `oklch(0.55 0.20 25)` | `#DC4C4C` | Chart series 4 |
| `--chart-5` | `oklch(0.50 0.18 290)` | `#8B5CF6` | Chart series 5 |
| `--chart-6` | `oklch(0.55 0.18 340)` | `#E879A8` | Chart series 6 |
| `--chart-7` | `oklch(0.55 0.15 220)` | `#60A5FA` | Chart series 7 |

### Brand saturation delta

Light theme reduces brand saturation slightly from dark (0.19 vs 0.18 chroma) to avoid visual shout on a bright canvas. Dark theme raises brand lightness (0.55 L) to glow against the dark surface.

### Chart area opacity

Area fills at 15% of series color for both themes. Line strokes at 80% opacity.

---

## Typography

### Font stack

```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', ui-monospace, monospace;
```

One family. No display/body pairing. Inter carries everything: headings, labels, body, data.

### Scale

Fixed rem scale. No fluid or clamp-sized headings. Ratio: 1.2 between steps.

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| `--text-h1` | 1.75rem (28px) | 700 | 2.25rem | -0.015em | Page title (each view) |
| `--text-h2` | 1.375rem (22px) | 600 | 1.875rem | — | Section heading |
| `--text-h3` | 1.125rem (18px) | 600 | 1.625rem | — | Card title |
| `--text-body` | 0.875rem (14px) | 400 | 1.375rem | — | Body, table cells |
| `--text-small` | 0.75rem (12px) | 400 | 1.125rem | — | Auxiliary, tags, meta |
| `--text-number-lg` | 2rem (32px) | 700 | 1 | — | Primary stat value |
| `--text-number-md` | 1.5rem (24px) | 700 | 1 | — | Secondary stat value |
| `--text-nav` | 0.9375rem (15px) | 500 | 1.25rem | — | Navigation items |
| `--text-button` | 0.875rem (14px) | 500 | 1 | — | Button labels |
| `--text-label` | 0.8125rem (13px) | 500 | 1.125rem | 0.01em | Form labels, table header |

### Numbers

All numeric values use `--font-mono`. Alignment: tabular figures enabled via `font-variant-numeric: tabular-nums`.

### Line length

Body containers capped at 75ch. Data tables exempt (can run 120ch+).

---

## Spacing

Rhythm-based, not uniform. Same padding everywhere is monotony.

| Token | Rem | Px | Use |
|-------|-----|----|-----|
| `--space-1` | 0.25rem | 4 | Tight inner padding (tags, badges) |
| `--space-2` | 0.5rem | 8 | Tight spacing, icon gaps |
| `--space-3` | 0.75rem | 12 | Button padding, small card inset |
| `--space-4` | 1rem | 16 | Card padding, section gap |
| `--space-5` | 1.25rem | 20 | StatCard inner padding |
| `--space-6` | 1.5rem | 24 | Content area padding, card grid gap |
| `--space-8` | 2rem | 32 | Section spacing, modal padding |
| `--space-10` | 2.5rem | 40 | Page section spacing |

### Grid

Content area: 24px padding (`--space-6`). Card grid: responsive columns with 24px gap.

---

## Border Radius

| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | 4px | Tags, status indicators |
| `--radius-md` | 6px | Buttons, inputs, selects |
| `--radius-lg` | 8px | Cards, modals, panels |
| `--radius-xl` | 12px | Large modals (optional) |

---

## Shadows

Dark theme uses luminescent borders, not shadows. Light theme uses subtle box-shadow.

### Dark theme
No box-shadows. Elevation via surface lightness: `--surface` → `--surface-hover` → `--surface-raised`.

### Light theme

| Elevation | Shadow |
|-----------|--------|
| Card (default) | `0 1px 2px oklch(0 0 0 / 0.04)` |
| Raised (hover) | `0 2px 8px oklch(0 0 0 / 0.06)` |
| Modal / popover | `0 8px 24px oklch(0 0 0 / 0.10)` |

---

## Components

Every interactive component defines: default, hover, focus, active, disabled, loading.

### Sidebar

- Width: 260px, fixed
- Background: `--surface`
- Active item: `--brand-subtle` bg + `--brand` left inset (not side-stripe border — see bans)
- Hover item: `--surface-hover` bg
- Icons: lucide, 20px, `--text-secondary` default, `--text-primary` active
- Logo area: 48px height, app name in `--text-nav` weight
- Bottom: version number (`--text-small`, `--text-tertiary`)

### TopBar

- Height: 56px
- Background: `--bg` (not `--surface` — it blends with content, not cards)
- Border-bottom: `--border-subtle`
- Right section: time range select + refresh toggle + refresh button, all `--space-3` gap

### StatCard

- Background: `--surface`
- Border: `--border`, 1px
- Border-radius: `--radius-lg`
- Padding: `--space-5`
- Icon block: 40px, rounded `--radius-md`, background at 15% of semantic color
- Value: `--text-number-lg` or `--text-number-md`, `--font-mono`, `--text-primary`
- Label: `--text-small`, `--text-secondary`
- Trend: semantic color, `--text-small`, arrow glyph + percentage
- No side-stripe border (banned). No big number + small label hero-metric template without context.

### ChartCard

- Same base as StatCard
- Title: `--text-h3`, `--text-primary`
- Optional dimension toggle: segmented button row, `--text-small`
- Chart takes remaining height; minimum 240px
- Empty state: centered icon + body text + optional action

### DataTable

- Background: transparent (inherits parent surface)
- Header: `--text-label`, `--text-secondary`, `--border-subtle` bottom border
- Row: hover turns `--surface-hover`; alternating rows via `--border-subtle` between them (not stripe colors)
- Cell padding: `--space-2` `--space-3`
- Empty state: centered illustration + body text

### Button

| Variant | Background | Text | Hover | Focus |
|---------|-----------|------|-------|-------|
| Primary | `--brand` | `#fff` | `--brand-hover` | ring `--brand` |
| Secondary | `--surface` | `--text-primary` | `--surface-hover` | ring `--border` |
| Ghost | transparent | `--text-secondary` | `--surface-hover` | — |
| Danger | `--danger` | `#fff` | 10% darker | ring `--danger` |

All: `--radius-md`, padding `--space-3` `--space-4`, `--text-button`, transition 150ms ease.

### Tag

`--radius-sm`, padding `--space-1` `--space-2`, `--text-small`.

| Semantic | Background | Text |
|----------|-----------|------|
| Brand | `--brand-subtle` | `--brand` |
| Success | 15% success | `--success` |
| Warning | 15% warning | `--warning` |
| Danger | 15% danger | `--danger` |
| Neutral | `--surface-hover` | `--text-secondary` |

### Input / Select

- Background: `--surface`
- Border: `--border`, 1px
- Border-radius: `--radius-md`
- Padding: `--space-2` `--space-3`
- Text: `--text-body`, `--text-primary`
- Placeholder: `--text-tertiary`
- Focus: `--brand` border, ring `--brand` at 20% opacity
- Disabled: `--text-tertiary`, `--border-subtle`

### Switch (toggle)

- Track: 36px wide, 20px tall, `--border` bg
- Track active: `--brand` bg
- Thumb: 16px circle, white, raised using elevation
- Transition: 200ms ease, translate transform only (never animate layout properties)

### StatusIndicator

- Dot: 8px circle, semantic color
- Label: `--text-small`, `--text-secondary`
- Gap: `--space-2`

---

## Motion

### Durations

- Micro-interactions (hover, focus, toggle): 150ms
- State changes (panel show/hide, skeleton→content): 200ms
- Page transitions (route change): 250ms

### Curves

- Entrance/exit: `cubic-bezier(0.16, 1, 0.3, 1)` — exponential ease-out
- Micro-interactions: `cubic-bezier(0.4, 0, 0.2, 1)` — standard ease

### Rules

- Never animate CSS layout properties (width, height, top, left, margin, padding)
- No orchestrated page-load sequences. Content appears; don't make users watch it load.
- Motion conveys state only: hover feedback, toggle activation, loading pulse. Nothing decorative.
- `prefers-reduced-motion: reduce` → all transitions to 0ms, all animations to forwards-fill end state

### Skeleton loading

- Background: `--surface-hover`, shimmer animation via pseudo-element gradient sweep
- Duration: 1.5s, infinite, linear
- Shape matches the content block (card outline for charts, line blocks for text)

---

## Charts (ECharts theme)

Shared config applied in a central `useChartTheme` composable, not repeated per view.

### Dark theme

| Property | Value |
|----------|-------|
| background | transparent |
| tooltip bg | `--surface-raised` |
| tooltip border | `--border` |
| text color | `--text-secondary` |
| axis line | `--border-subtle` |
| axis label | `--text-tertiary`, 11px |
| split line | `--border-subtle`, dashed |
| grid | `{ top: 20, right: 24, bottom: 28, left: 56 }` |

### Light theme

| Property | Value |
|----------|-------|
| background | transparent |
| tooltip bg | `--surface-raised` (white) |
| tooltip border | `--border` |
| text color | `--text-secondary` |
| axis line | `--border-subtle` |
| axis label | `--text-tertiary`, 11px |
| split line | `--border-subtle`, dashed |
| grid | same as dark |

### Series colors

`--chart-1` through `--chart-7` in order. Area fill: 15% opacity of series color. No gradient fills on areas.

---

## Layout

### Page shell

```
+---------------------------+----------------------------------------+
|                           |  TopBar (56px)                          |
|   Sidebar (260px)         +----------------------------------------+
|                           |                                        |
|   Logo                    |  Content area (padding: 24px)          |
|                           |                                        |
|   Nav items               |  +------+ +------+ +------+ +------+  |
|                           |  | Stat | | Stat | | Stat | | Stat |  |
|   • Dashboard             |  +------+ +------+ +------+ +------+  |
|   • Daily Report          |                                        |
|   • Weekly Report         |  +----------------------------------+  |
|   • Scheduler Logs        |  | ChartCard (area chart)           |  |
|   • Settings              |  +----------------------------------+  |
|                           |                                        |
|   Version + Status        |  +-----------------+ +---------------+ |
|                           |  | Donut chart     | | Bar chart     | |
|                           |  +-----------------+ +---------------+ |
+---------------------------+----------------------------------------+
```

### Responsive breakpoints

| Breakpoint | Layout |
|------------|--------|
| ≥1400px | 4-column stat grid, 2-column chart grid |
| 960–1399px | 2-column stat grid, single column charts |
| 640–959px | Single column, sidebar collapsed (hamburger) |
| <640px | Single column, condensed padding (16px) |

---

## Dark theme bans (shared + product)

- **No side-stripe borders** (`border-left`/`border-right` >1px as accent) — use full border, bg tint, or icon
- **No gradient text** — solid color, emphasis via weight or size
- **No glassmorphism as default** — purposeful or absent
- **No identical card grids** — vary content, don't repeat icon+heading+body
- **No modal as first thought** — exhaust inline / progressive alternatives
- **No decorative motion** — every animation conveys state
- **No inconsistent component vocabulary** — same button shape everywhere
- **No display fonts in UI** — Inter carries everything
- **No reinventing standard affordances** — standard scrollbars, standard form controls, standard modals when necessary

---

## Light theme considerations

- Background warmth (`oklch 0.006 260` chroma tinted toward brand) prevents the sterile white-lab look
- Surface elevation uses lightness, not shadows, for cards; shadows only for modals and popovers
- Brand accent lowered from dark theme saturation to avoid visual shout on bright canvas
- Chart area fills at same 15% opacity; lines at 80%
- Text contrast exceeds WCAG AA: primary 7.5:1, secondary 5.5:1, tertiary 3.5:1 (not used for body copy)

---

## Implementation

All tokens defined as CSS custom properties on `:root` and `.dark`:

```css
:root { /* light theme */ }
.dark { /* dark theme */ }
```

Tailwind config maps directly to these custom properties. No hardcoded hex values outside the token definition.

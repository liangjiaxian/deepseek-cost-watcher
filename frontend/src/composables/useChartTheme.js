const CHART_COLORS = [
  '--color-chart-1',
  '--color-chart-2',
  '--color-chart-3',
  '--color-chart-4',
  '--color-chart-5',
  '--color-chart-6',
  '--color-chart-7',
]

function getCSSVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim()
}

function hexToRgba(hex, alpha) {
  if (!hex) return `rgba(128, 128, 128, ${alpha})`
  const h = hex.replace('#', '')
  const r = parseInt(h.substring(0, 2), 16)
  const g = parseInt(h.substring(2, 4), 16)
  const b = parseInt(h.substring(4, 6), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

function formatAxisNum(v) {
  if (Math.abs(v) >= 1e8) return (v / 1e8).toFixed(1) + '亿'
  if (Math.abs(v) >= 1e4) return (v / 1e4).toFixed(1) + '万'
  return v.toLocaleString('zh-CN')
}

export function useChartTheme() {
  function resolveColor(name) {
    return getCSSVar(name)
  }

  function baseTooltip() {
    return {
      trigger: 'axis',
      backgroundColor: resolveColor('--color-surface-raised'),
      borderColor: resolveColor('--color-border'),
      borderWidth: 1,
      textStyle: { color: resolveColor('--color-text-primary'), fontSize: 12 },
    }
  }

  function baseGrid(overrides = {}) {
    return { top: 24, right: 24, bottom: 32, left: 64, ...overrides }
  }

  function categoryAxis(data, overrides = {}) {
    return {
      type: 'category',
      data,
      axisLine: { lineStyle: { color: resolveColor('--color-border-subtle') } },
      axisLabel: { color: resolveColor('--color-text-tertiary'), fontSize: 11 },
      splitLine: { show: false },
      ...overrides,
    }
  }

  function valueAxis(overrides = {}) {
    return {
      type: 'value',
      splitLine: { lineStyle: { color: resolveColor('--color-border-subtle'), type: 'dashed' } },
      axisLabel: {
        color: resolveColor('--color-text-tertiary'),
        fontSize: 11,
        formatter: formatAxisNum,
      },
      nameTextStyle: { color: resolveColor('--color-text-tertiary'), fontSize: 11 },
      ...overrides,
    }
  }

  function areaSeries(data, colorIndex = 0, overrides = {}) {
    const color = resolveColor(CHART_COLORS[colorIndex])
    return {
      type: 'line',
      data,
      smooth: true,
      showSymbol: true,
      symbolSize: 5,
      itemStyle: { color },
      areaStyle: { color: hexToRgba(color, 0.15) },
      ...overrides,
    }
  }

  function barSeries(data, colorIndex = 0, overrides = {}) {
    const color = resolveColor(CHART_COLORS[colorIndex])
    return {
      type: 'bar',
      data,
      itemStyle: { color, borderRadius: [0, 0, 0, 0] },
      barMaxWidth: 32,
      ...overrides,
    }
  }

  function donutSeries(data, overrides = {}) {
    return {
      type: 'pie',
      radius: ['38%', '62%'],
      center: ['50%', '43%'],
      data: data.map((d, i) => ({
        ...d,
        itemStyle: { color: resolveColor(CHART_COLORS[i % CHART_COLORS.length]), ...d.itemStyle },
      })),
      label: { show: false },
      labelLine: { show: false },
      ...overrides,
    }
  }

  function formatLegendValue(v) {
    if (v >= 100) return `¥${v.toFixed(0)}`
    if (v >= 1) return `¥${v.toFixed(1)}`
    return `¥${v.toFixed(2)}`
  }

  // Horizontal legend below the donut: swatch + model + amount + share.
  function donutLegend(data, overrides = {}) {
    const total = data.reduce((s, d) => s + (Number(d.value) || 0), 0)
    return {
      bottom: 2,
      left: 'center',
      type: data.length > 4 ? 'scroll' : 'plain',
      icon: 'rect',
      itemWidth: 8,
      itemHeight: 8,
      itemGap: 14,
      textStyle: {
        color: resolveColor('--color-text-secondary'),
        fontSize: 11,
        fontFamily: 'Roboto Mono',
      },
      formatter: (name) => {
        const item = data.find(d => d.name === name)
        if (!item) return name
        const pct = total > 0 ? ((Number(item.value) / total) * 100).toFixed(0) : '0'
        return `${name}  ${formatLegendValue(Number(item.value))} · ${pct}%`
      },
      ...overrides,
    }
  }

  function pieTooltip() {
    return {
      trigger: 'item',
      backgroundColor: resolveColor('--color-surface-raised'),
      borderColor: resolveColor('--color-border'),
      borderWidth: 1,
      textStyle: { color: resolveColor('--color-text-primary'), fontSize: 12 },
    }
  }

  function yBounds(range) {
    const r = range.max - range.min
    return {
      min: r === 0 ? range.min - 1 : range.min - r * 0.15,
      max: r === 0 ? range.max + 1 : range.max + r * 0.15,
    }
  }

  return {
    CHART_COLORS,
    resolveColor,
    baseTooltip,
    baseGrid,
    categoryAxis,
    valueAxis,
    areaSeries,
    barSeries,
    donutSeries,
    donutLegend,
    pieTooltip,
    yBounds,
  }
}

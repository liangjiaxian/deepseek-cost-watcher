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
      itemStyle: { color, borderRadius: [4, 4, 0, 0] },
      barMaxWidth: 32,
      ...overrides,
    }
  }

  function donutSeries(data, overrides = {}) {
    return {
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '45%'],
      data: data.map((d, i) => ({
        ...d,
        itemStyle: { color: resolveColor(CHART_COLORS[i % CHART_COLORS.length]), ...d.itemStyle },
      })),
      label: { color: resolveColor('--color-text-secondary'), fontSize: 11 },
      labelLine: { lineStyle: { color: resolveColor('--color-border') } },
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
    pieTooltip,
    yBounds,
  }
}

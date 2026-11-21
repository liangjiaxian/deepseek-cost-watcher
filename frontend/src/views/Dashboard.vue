<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <StatCard
        :icon="Wallet" label="账户余额" :value="store.balance" color="var(--color-warning)"
        format="currency" :details="balanceDetails" :status="balanceStatus"
      />
      <StatCard :icon="Gem" label="本月消费" :value="monthTotalCost" color="var(--color-brand)" format="currency" />
      <StatCard :icon="Activity" label="今日消费" :value="todayCost" color="var(--color-success)" format="currency" />
      <StatCard :icon="Zap" label="今日请求数" :value="todayRequests" color="var(--color-chart-5)" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">
      <ChartCard kicker="Balance Trend" title="余额趋势" :option="balanceTrendOption" :has-data="!!balancePoints.length" class="xl:col-span-2" height="360px" />
      <ChartCard kicker="Distribution" title="模型消费分布 (CNY)" :option="distOption" :has-data="!!costModelTotals.length" height="360px" />
    </div>

    <KeyRanking kicker="Ranking" title="Key 使用与费用排行" :windows="rankingWindows" />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { useUsageStore } from '../stores/usage'
import { useAppStore } from '../stores/app'
import { useChartTheme } from '../composables/useChartTheme'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import KeyRanking from '../components/KeyRanking.vue'
import { APP_TIME_ZONE, beijingTodayISO, parseUtc } from '../utils/time'
import { Gem, Activity, Zap, Wallet } from 'lucide-vue-next'

const store = useUsageStore()
const appStore = useAppStore()
const { baseTooltip, baseGrid, categoryAxis, valueAxis, areaSeries, donutSeries, donutLegend, pieTooltip, yBounds, resolveColor } = useChartTheme()

const costDays = computed(() => store.usageCost?.days ?? [])
const costDayData = computed(() => costDays.value.map(d => {
  const total = d.data.reduce((s, m) => s + m.usage.reduce((a, u) => a + u.amount, 0), 0)
  return { date: d.date.slice(5), total }
}))
const monthTotalCost = computed(() => costDayData.value.reduce((s, d) => s + d.total, 0))
const todayStr = computed(() => beijingTodayISO())
const todayCost = computed(() => {
  const day = costDays.value.find(d => d.date === todayStr.value)
  if (!day) return 0
  return day.data.reduce((s, m) => s + m.usage.reduce((a, u) => a + u.amount, 0), 0)
})

const todayItems = computed(() => store.keyRankings?.today?.items ?? [])
const todayRequests = computed(() => todayItems.value.reduce((s, r) => s + r.request_count, 0))

const money = (v) => `¥${Number(v ?? 0).toFixed(2)}`
const balanceLatest = computed(() => store.balanceLatest)
const balanceDetails = computed(() => {
  const b = balanceLatest.value
  if (!b || b.granted_balance == null || b.topped_up_balance == null) return null
  return [
    { label: '赠金', value: money(b.granted_balance) },
    { label: '充值', value: money(b.topped_up_balance) },
  ]
})
const balanceStatus = computed(() => {
  const b = balanceLatest.value
  if (!b || b.is_available == null) return null
  return b.is_available
    ? { ok: true, text: '可用于调用' }
    : { ok: false, text: '余额不可用' }
})

const rankingWindows = computed(() => {
  const sets = store.keyRankings
  if (!sets) return []
  const build = (key, label, set) => ({
    key, label,
    items: set?.items ?? [],
    costAvailable: !!set?.cost_available,
  })
  return [
    build('today', '今日', sets.today),
    build('last_30_days', '近 30 天', sets.last_30_days),
    build('year', '今年', sets.year),
  ]
})

const costModelTotals = computed(() => {
  const map = {}
  for (const d of costDays.value) {
    for (const m of d.data) {
      const total = m.usage.reduce((a, u) => a + u.amount, 0)
      map[m.model] = (map[m.model] || 0) + total
    }
  }
  return Object.entries(map).map(([model, cost]) => ({ model, cost }))
})

const balancePoints = computed(() => store.usageCost?.days ? store.balanceTrend?.points ?? [] : [])

const balanceTrendOption = computed(() => ({
  tooltip: {
    ...baseTooltip(),
    formatter: (params) => {
      const p = params[0]
      const point = balancePoints.value[p.dataIndex]
      let text = `${p.axisValue}<br/>¥${p.value?.toFixed(2)}`
      if (point && (point.granted_balance != null || point.topped_up_balance != null)) {
        text += `<br/><span style="opacity:.7">赠金 ¥${(point.granted_balance ?? 0).toFixed(2)} · 充值 ¥${(point.topped_up_balance ?? 0).toFixed(2)}</span>`
      }
      return text
    },
  },
  grid: baseGrid({ right: 30 }),
  xAxis: categoryAxis(
    store.balanceTrend?.points?.map(p => {
      const d = parseUtc(p.time)
      return d ? d.toLocaleDateString('zh-CN', { timeZone: APP_TIME_ZONE, month: '2-digit', day: '2-digit', hour: '2-digit' }) : '--'
    }) ?? []
  ),
  yAxis: valueAxis({ name: 'CNY', min: (v) => yBounds(v).min, max: (v) => yBounds(v).max }),
  series: [areaSeries(
    store.balanceTrend?.points?.map(p => p.balance) ?? [],
    0
  )],
}))

const distOption = computed(() => {
  const data = costModelTotals.value
    .map(d => ({ name: d.model, value: d.cost }))
    .filter(d => d.value >= 0.005)
  return {
    tooltip: {
      ...pieTooltip(),
      formatter: ({ name, value, percent }) => `${name}<br/>¥${value?.toFixed(4)} (${percent}%)`,
    },
    legend: donutLegend(data),
    series: [donutSeries(data)],
    // Model count lives in the donut center.
    title: data.length ? {
      text: `${data.length}`,
      left: 'center',
      top: '43%',
      textVerticalAlign: 'middle',
      textStyle: {
        color: resolveColor('--color-text-primary'),
        fontSize: 20,
        fontWeight: 'bold',
        fontFamily: 'Roboto Mono',
      },
    } : undefined,
  }
})

function loadAll() {
  store.fetchUsageCost(undefined, undefined, true)
  store.fetchBalanceTrend('7d')
  store.fetchBalanceLatest()
  store.fetchKeyRankings()
}

let timer = null

onMounted(() => {
  loadAll()
  if (appStore.autoRefresh) {
    timer = setInterval(loadAll, appStore.refreshInterval)
  }
})

watch(() => appStore.autoRefresh, (val) => {
  if (timer) clearInterval(timer)
  if (val) timer = setInterval(loadAll, appStore.refreshInterval)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

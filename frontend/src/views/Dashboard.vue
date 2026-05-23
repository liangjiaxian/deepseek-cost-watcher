<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <StatCard :icon="Wallet" label="账户余额" :value="store.balance" color="var(--color-warning)" format="currency" />
      <StatCard :icon="Gem" label="本月消费" :value="monthTotalCost" color="var(--color-brand)" format="currency" />
      <StatCard :icon="Activity" label="今日消费" :value="todayCost" color="var(--color-success)" format="currency" />
      <StatCard :icon="Layers" label="消费天数" :value="costDaysCount" color="var(--color-chart-5)" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">
      <ChartCard title="余额趋势" :option="balanceTrendOption" :has-data="!!balancePoints.length" class="xl:col-span-2" height="360px" />
      <ChartCard title="模型消费分布 (CNY)" :option="distOption" :has-data="!!costModelTotals.length" height="360px" />
    </div>

    <ChartCard title="本月每日消费 (CNY)" :option="costOption" :has-data="!!costDayData.length" height="360px" />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { useUsageStore } from '../stores/usage'
import { useAppStore } from '../stores/app'
import { useChartTheme } from '../composables/useChartTheme'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import { Gem, Activity, Layers, Wallet } from 'lucide-vue-next'

const store = useUsageStore()
const appStore = useAppStore()
const { baseTooltip, baseGrid, categoryAxis, valueAxis, areaSeries, barSeries, donutSeries, pieTooltip, yBounds } = useChartTheme()

const costDays = computed(() => store.usageCost?.days ?? [])
const costDayData = computed(() => costDays.value.map(d => {
  const total = d.data.reduce((s, m) => s + m.usage.reduce((a, u) => a + u.amount, 0), 0)
  return { date: d.date.slice(5), total }
}))
const monthTotalCost = computed(() => costDayData.value.reduce((s, d) => s + d.total, 0))
const todayStr = computed(() => new Date().toISOString().slice(0, 10))
const todayCost = computed(() => {
  const day = costDays.value.find(d => d.date === todayStr.value)
  if (!day) return 0
  return day.data.reduce((s, m) => s + m.usage.reduce((a, u) => a + u.amount, 0), 0)
})
const costDaysCount = computed(() => costDays.value.length)

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
      return `${p.axisValue}<br/>¥${p.value?.toFixed(2)}`
    },
  },
  grid: baseGrid({ right: 30 }),
  xAxis: categoryAxis(
    store.balanceTrend?.points?.map(p => {
      const d = new Date(p.time)
      return d.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit' })
    }) ?? []
  ),
  yAxis: valueAxis({ name: 'CNY', min: (v) => yBounds(v).min, max: (v) => yBounds(v).max }),
  series: [areaSeries(
    store.balanceTrend?.points?.map(p => p.balance) ?? [],
    2
  )],
}))

const distOption = computed(() => ({
  tooltip: {
    ...pieTooltip(),
    formatter: ({ name, value, percent }) => `${name}<br/>¥${value?.toFixed(4)} (${percent}%)`,
  },
  series: [donutSeries(
    costModelTotals.value.map(d => ({ name: d.model, value: d.cost }))
  )],
  graphic: costModelTotals.value.length ? {
    type: 'text',
    left: 'center',
    top: '42%',
    style: {
      text: `${costModelTotals.value.length}`,
      fill: 'var(--color-text-primary)',
      fontSize: 20,
      fontWeight: 'bold',
      fontFamily: 'JetBrains Mono',
    },
  } : undefined,
}))

const costOption = computed(() => ({
  tooltip: {
    ...baseTooltip(),
    formatter: (params) => {
      const p = params[0]
      return `${p.name}日<br/>¥${p.value?.toFixed(4)}`
    },
  },
  grid: baseGrid(),
  xAxis: categoryAxis(costDayData.value.map(d => d.date)),
  yAxis: valueAxis({ name: 'CNY', min: (v) => yBounds(v).min, max: (v) => yBounds(v).max }),
  series: [barSeries(costDayData.value.map(d => d.total), 0)],
}))

let timer = null

onMounted(() => {
  store.fetchUsageCost(undefined, undefined, true)
  store.fetchBalanceTrend('7d')
  if (appStore.autoRefresh) {
    timer = setInterval(() => {
      store.fetchUsageCost(undefined, undefined, true)
      store.fetchBalanceTrend('7d')
    }, appStore.refreshInterval)
  }
})

watch(() => appStore.autoRefresh, (val) => {
  if (timer) clearInterval(timer)
  if (val) {
    timer = setInterval(() => {
      store.fetchUsageCost(undefined, undefined, true)
      store.fetchBalanceTrend('7d')
    }, appStore.refreshInterval)
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

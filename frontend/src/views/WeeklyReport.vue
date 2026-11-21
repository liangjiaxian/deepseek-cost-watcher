<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center gap-4">
      <input type="week" v-model="weekStr" class="input text-sm" @change="loadData" />
      <span class="text-xs text-text-secondary">
        消费 ¥{{ costData?.total_cost?.toFixed(4) }} · 请求 {{ weekRequests.toLocaleString() }} · {{ costData?.active_models ?? 0 }} 个模型
      </span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <StatCard :icon="Sigma" label="本周消费" :value="costData?.total_cost" color="var(--color-brand)" format="currency" />
      <StatCard :icon="BarChart3" label="日均消费" :value="costData?.daily_avg_cost" color="var(--color-success)" format="currency" />
      <StatCard
        :icon="TrendingDown" label="余额变动" :value="costData?.balance_change"
        :color="(costData?.balance_change || 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)'"
        format="currency"
      />
      <StatCard :icon="Zap" label="本周请求数" :value="weekRequests" color="var(--color-chart-5)" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">
      <ChartCard kicker="Daily Trend" title="每日消费趋势" :option="dailyOption" :has-data="!!dailyBreakdown.length" height="360px" class="xl:col-span-2" />
      <ChartCard kicker="Distribution" title="模型消费分布" :option="modelOption" :has-data="!!modelBreakdown.length" height="360px" />
    </div>

    <KeyRanking kicker="Weekly Ranking" title="本周 Key 使用与费用排行" :windows="rankingWindows" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUsageStore } from '../stores/usage'
import { useChartTheme } from '../composables/useChartTheme'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import KeyRanking from '../components/KeyRanking.vue'
import { beijingISOWeek } from '../utils/time'
import { Sigma, BarChart3, TrendingDown, Zap } from 'lucide-vue-next'

const store = useUsageStore()
const { baseTooltip, baseGrid, categoryAxis, valueAxis, barSeries, donutSeries, donutLegend, pieTooltip, yBounds, resolveColor } = useChartTheme()

const { year, week } = beijingISOWeek()
const weekStr = ref(`${year}-W${String(week).padStart(2, '0')}`)

const costData = computed(() => store.weeklyCost)
const dailyBreakdown = computed(() => costData.value?.daily_breakdown ?? [])
const modelBreakdown = computed(() => costData.value?.model_breakdown ?? [])

const weeklyItems = computed(() => store.weeklyKeyRankings?.items ?? [])
const weekRequests = computed(() => weeklyItems.value.reduce((s, r) => s + r.request_count, 0))

const rankingWindows = computed(() => [{
  key: 'week',
  label: weekStr.value,
  items: weeklyItems.value,
  costAvailable: !!store.weeklyKeyRankings?.cost_available,
}])

const dailyOption = computed(() => ({
  tooltip: {
    ...baseTooltip(),
    formatter: (params) => {
      const p = params[0]
      return `${p.axisValue}<br/>¥${p.value?.toFixed(4)}`
    },
  },
  grid: baseGrid(),
  xAxis: categoryAxis(dailyBreakdown.value.map(d => d.date.slice(5))),
  yAxis: valueAxis({ name: 'CNY', min: (v) => yBounds(v).min, max: (v) => yBounds(v).max }),
  series: [{
    ...barSeries(dailyBreakdown.value.map(d => d.total_cost), 0),
    barMaxWidth: 48,
    label: { show: true, position: 'top', color: resolveColor('--color-text-secondary'), fontSize: 11, formatter: (p) => `¥${p.value?.toFixed(4)}` },
  }],
}))

const modelOption = computed(() => {
  const data = modelBreakdown.value
    .map(d => ({ name: d.model, value: d.cost }))
    .filter(d => d.value >= 0.005)
  return {
    tooltip: {
      ...pieTooltip(),
      formatter: ({ name, value, percent }) => `${name}<br/>¥${value?.toFixed(4)} (${percent}%)`,
    },
    legend: donutLegend(data),
    series: [donutSeries(data)],
    // Active model count lives in the donut center instead of a stat card.
    title: data.length ? {
      text: `${costData.value?.active_models ?? data.length}`,
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

function loadData() {
  const m = weekStr.value.match(/(\d+)-W(\d+)/)
  if (m) { store.fetchWeeklyCost(parseInt(m[1]), parseInt(m[2])); store.fetchWeeklyKeyRankings(parseInt(m[1]), parseInt(m[2])) }
}

onMounted(() => loadData())
</script>

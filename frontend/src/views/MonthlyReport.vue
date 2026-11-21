<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center gap-4">
      <input type="month" v-model="monthStr" class="input text-sm" @change="loadData" />
      <span class="text-xs text-text-secondary">
        消费 ¥{{ report?.total_cost?.toFixed(4) }} · 请求 {{ monthRequests.toLocaleString() }} · {{ report?.active_models ?? 0 }} 个模型
      </span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <StatCard :icon="Sigma" label="本月消费" :value="report?.total_cost" color="var(--color-brand)" format="currency" />
      <StatCard :icon="BarChart3" label="日均消费" :value="report?.daily_avg_cost" color="var(--color-success)" format="currency" />
      <StatCard
        :icon="TrendingDown" label="余额变动" :value="report?.balance_change"
        :color="(report?.balance_change || 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)'"
        format="currency"
      />
      <StatCard :icon="Zap" label="本月请求数" :value="monthRequests" color="var(--color-chart-5)" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">
      <ChartCard kicker="Monthly Trend" title="消费趋势" :option="dailyOption" :has-data="!!dailyBreakdown.length" height="360px" class="xl:col-span-2" />
      <ChartCard kicker="Distribution" title="模型消费分布" :option="modelOption" :has-data="!!modelBreakdown.length" height="360px" />
    </div>

    <KeyRanking kicker="Monthly Ranking" title="本月 Key 使用与费用排行" :windows="rankingWindows" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUsageStore } from '../stores/usage'
import { useChartTheme } from '../composables/useChartTheme'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import KeyRanking from '../components/KeyRanking.vue'
import { Sigma, BarChart3, TrendingDown, Zap } from 'lucide-vue-next'

const store = useUsageStore()
const { baseTooltip, baseGrid, categoryAxis, valueAxis, barSeries, donutSeries, donutLegend, pieTooltip, yBounds, resolveColor } = useChartTheme()

const now = new Date()
const monthStr = ref(`${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`)

const report = computed(() => store.monthlyCost)
const dailyBreakdown = computed(() => report.value?.daily_breakdown ?? [])
const modelBreakdown = computed(() => report.value?.model_breakdown ?? [])

const monthlyItems = computed(() => store.monthlyKeyRankings?.items ?? [])
const monthRequests = computed(() => monthlyItems.value.reduce((s, r) => s + r.request_count, 0))

const rankingWindows = computed(() => [{
  key: 'month',
  label: monthStr.value,
  items: monthlyItems.value,
  costAvailable: !!store.monthlyKeyRankings?.cost_available,
}])

const dailyOption = computed(() => ({
  tooltip: {
    ...baseTooltip(),
    formatter: (params) => {
      const p = params[0]
      return `${p.axisValue}<br/>¥${p.value?.toFixed(4)}`
    },
  },
  grid: baseGrid({ right: 30 }),
  xAxis: categoryAxis(dailyBreakdown.value.map(d => d.date.slice(5))),
  yAxis: valueAxis({ name: 'CNY', min: (v) => yBounds(v).min, max: (v) => yBounds(v).max }),
  series: [{
    ...barSeries(dailyBreakdown.value.map(d => d.total_cost), 0),
    barMaxWidth: 16,
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
      text: `${report.value?.active_models ?? data.length}`,
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
  const m = monthStr.value.match(/(\d+)-(\d+)/)
  if (m) {
    store.fetchMonthlyCost(parseInt(m[1]), parseInt(m[2]))
    store.fetchMonthlyKeyRankings(parseInt(m[1]), parseInt(m[2]))
  }
}

onMounted(() => loadData())
</script>

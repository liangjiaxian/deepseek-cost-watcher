<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center gap-4">
      <input type="week" v-model="weekStr" class="input text-sm" @change="loadData" />
      <span v-if="costData" class="text-xs text-text-secondary">
        消费 ¥{{ costData.total_cost?.toFixed(4) }} · {{ costData.active_models }} 个模型
      </span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <StatCard :icon="Sigma" label="本周消费" :value="costData?.total_cost" color="var(--color-brand)" format="currency" />
      <StatCard :icon="BarChart3" label="日均消费" :value="costData?.daily_avg_cost" color="var(--color-success)" format="currency" />
      <StatCard :icon="TrendingDown" label="余额变动" :value="costData?.balance_change" :color="(costData?.balance_change || 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)'" format="currency" />
      <StatCard :icon="Cpu" label="活跃模型" :value="costData?.active_models" color="var(--color-chart-5)" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <ChartCard title="每日消费趋势" :option="dailyOption" :has-data="!!dailyBreakdown.length" height="360px" />
      <ChartCard title="模型消费分布" :option="modelOption" :has-data="!!modelBreakdown.length" height="360px" />
    </div>
    <KeyRanking title="本周用户使用量排行榜" :items="store.weeklyKeyRankings" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUsageStore } from '../stores/usage'
import { useChartTheme } from '../composables/useChartTheme'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import KeyRanking from '../components/KeyRanking.vue'
import { Sigma, BarChart3, TrendingDown, Cpu } from 'lucide-vue-next'

const store = useUsageStore()
const { baseTooltip, baseGrid, categoryAxis, valueAxis, barSeries, donutSeries, pieTooltip, yBounds } = useChartTheme()

const now = new Date()
const weekStart = new Date(now)
weekStart.setDate(now.getDate() - ((now.getDay() + 6) % 7))
const year = weekStart.getFullYear()
const weekNum = Math.ceil(((weekStart - new Date(year, 0, 1)) / 86400000 + new Date(year, 0, 1).getDay() + 1) / 7)
const weekStr = ref(`${year}-W${String(weekNum).padStart(2, '0')}`)

const costData = computed(() => store.weeklyCost)
const dailyBreakdown = computed(() => costData.value?.daily_breakdown ?? [])
const modelBreakdown = computed(() => costData.value?.model_breakdown ?? [])

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
    label: { show: true, position: 'top', color: 'var(--color-text-secondary)', fontSize: 11, formatter: (p) => `¥${p.value?.toFixed(4)}` },
  }],
}))

const modelOption = computed(() => ({
  tooltip: {
    ...pieTooltip(),
    formatter: ({ name, value, percent }) => `${name}<br/>¥${value?.toFixed(4)} (${percent}%)`,
  },
  series: [donutSeries(
    modelBreakdown.value.map(d => ({ name: d.model, value: d.cost }))
  )],
}))

function loadData() {
  const m = weekStr.value.match(/(\d+)-W(\d+)/)
  if (m) { store.fetchWeeklyCost(parseInt(m[1]), parseInt(m[2])); store.fetchWeeklyKeyRankings(parseInt(m[1]), parseInt(m[2])) }
}

onMounted(() => loadData())
</script>

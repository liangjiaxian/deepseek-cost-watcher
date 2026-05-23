<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center gap-4">
      <input type="date" v-model="dateStr" class="input text-sm" @change="loadData" />
      <span v-if="bal" class="text-xs text-text-secondary">
        ¥{{ bal.balance_end }} · 变动 {{ bal.balance_change >= 0 ? '+' : '' }}{{ bal.balance_change }}
      </span>
      <span v-else-if="dayCost" class="text-xs text-text-secondary">
        {{ dayModels.length }} 个模型 · 消费 ¥{{ dayTotal.toFixed(4) }}
      </span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <StatCard :icon="Wallet" label="期初余额" :value="bal?.balance_start" color="var(--color-brand)" format="currency" />
      <StatCard :icon="Wallet" label="期末余额" :value="bal?.balance_end" color="var(--color-success)" format="currency" />
      <StatCard :icon="TrendingDown" label="余额变动" :value="bal?.balance_change" :color="(bal?.balance_change || 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)'" format="currency" />
      <StatCard :icon="Cpu" label="活跃模型" :value="dayModels.length" color="var(--color-chart-5)" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <ChartCard title="余额变化趋势" :option="balanceOption" :has-data="!!balancePoints.length" height="360px" />
      <ChartCard title="模型消费分布 (CNY)" :option="costDistOption" :has-data="!!dayModels.length" height="360px" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <ChartCard title="消费类型明细" :option="costTypeOption" :has-data="!!dayModels.length" height="360px" />
      <ChartCard title="本月每日消费" :option="monthCostOption" :has-data="!!costDayData.length" height="360px" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUsageStore } from '../stores/usage'
import { useChartTheme } from '../composables/useChartTheme'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import { Wallet, TrendingDown, Cpu } from 'lucide-vue-next'

const store = useUsageStore()
const { baseTooltip, baseGrid, categoryAxis, valueAxis, areaSeries, barSeries, donutSeries, pieTooltip, yBounds } = useChartTheme()
const dateStr = ref(new Date().toISOString().slice(0, 10))

const bal = computed(() => store.dailyBalance)
const balancePoints = computed(() => bal.value?.points ?? [])
const costDays = computed(() => store.usageCost?.days ?? [])
const costDayData = computed(() => costDays.value.map(d => {
  const total = d.data.reduce((s, m) => s + m.usage.reduce((a, u) => a + u.amount, 0), 0)
  return { date: d.date.slice(5), total }
}))
const dayCost = computed(() => costDays.value.find(d => d.date === dateStr.value) || null)
const dayModels = computed(() => dayCost.value?.data ?? [])
const dayTotal = computed(() => dayModels.value.reduce((s, m) => s + m.usage.reduce((a, u) => a + u.amount, 0), 0))

const balanceOption = computed(() => ({
  tooltip: {
    ...baseTooltip(),
    formatter: (params) => {
      const p = params[0]
      return `${p.axisValue}<br/>¥${p.value?.toFixed(2)}`
    },
  },
  grid: baseGrid({ right: 30 }),
  xAxis: categoryAxis(
    balancePoints.value.map(p => {
      const d = new Date(p.time)
      return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    })
  ),
  yAxis: valueAxis({ name: 'CNY', min: (v) => yBounds(v).min, max: (v) => yBounds(v).max }),
  series: [areaSeries(balancePoints.value.map(p => p.balance), 1)],
}))

const costDistOption = computed(() => ({
  tooltip: {
    ...pieTooltip(),
    formatter: ({ name, value, percent }) => `${name}<br/>¥${value?.toFixed(4)} (${percent}%)`,
  },
  series: [donutSeries(
    dayModels.value.map(d => {
      const total = d.usage.reduce((a, u) => a + u.amount, 0)
      return { name: d.model, value: total }
    })
  )],
}))

const costTypeOption = computed(() => {
  const typeMap = {}
  for (const m of dayModels.value) {
    for (const u of m.usage) {
      typeMap[u.type] = (typeMap[u.type] || 0) + u.amount
    }
  }
  const typeLabels = {
    PROMPT_TOKEN: '输入 Token',
    PROMPT_CACHE_HIT_TOKEN: '缓存命中',
    PROMPT_CACHE_MISS_TOKEN: '缓存未命中',
    RESPONSE_TOKEN: '输出 Token',
    REQUEST: '请求数',
  }
  const entries = Object.entries(typeMap).filter(([, v]) => v > 0)
  return {
    tooltip: {
      ...baseTooltip(),
    },
    grid: baseGrid({ left: 80, right: 80 }),
    xAxis: valueAxis({ name: 'CNY', min: (v) => yBounds(v).min, max: (v) => yBounds(v).max }),
    yAxis: {
      type: 'category',
      data: entries.map(([k]) => typeLabels[k] || k).reverse(),
      axisLine: { lineStyle: { color: 'var(--color-border)' } },
      axisLabel: { color: 'var(--color-text-secondary)', fontSize: 11 },
    },
    series: [{
      type: 'bar',
      data: entries.map(([, v]) => v).reverse(),
      itemStyle: { color: 'var(--color-brand)', borderRadius: [0, 4, 4, 0] },
      barMaxHeight: 28,
      label: {
        show: true, position: 'right', color: 'var(--color-text-secondary)', fontSize: 11,
        formatter: (p) => `¥${p.value?.toFixed(4)}`,
      },
    }],
  }
})

const monthCostOption = computed(() => ({
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

function loadData() {
  store.fetchDailyBalance(dateStr.value)
  store.fetchUsageCost(undefined, undefined, true)
}

onMounted(() => loadData())
</script>

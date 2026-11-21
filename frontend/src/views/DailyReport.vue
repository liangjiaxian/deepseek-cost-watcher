<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center gap-4">
      <input type="date" v-model="dateStr" class="input text-sm" @change="loadData" />
      <span class="text-xs text-text-secondary">
        消费 ¥{{ dayTotal.toFixed(4) }} · 请求 {{ dayRequests.toLocaleString() }} · {{ dailyItems.length }} 个 Key
      </span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <StatCard :icon="Gem" label="当日消费" :value="dayTotal" color="var(--color-brand)" format="currency" />
      <StatCard :icon="Zap" label="当日请求数" :value="dayRequests" color="var(--color-chart-5)" />
      <StatCard
        :icon="TrendingDown" label="余额变动" :value="bal?.balance_change"
        :color="(bal?.balance_change || 0) >= 0 ? 'var(--color-success)' : 'var(--color-danger)'"
        format="currency"
      />
      <StatCard :icon="Cpu" label="活跃模型" :value="dayModels.length" color="var(--color-success)" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <ChartCard kicker="Balance Trend" title="余额变化趋势" height="360px" :option="balanceOption" :has-data="!!balancePoints.length">
        <template #actions>
          <span v-if="bal?.balance_start != null" class="font-mono text-xs text-text-secondary">
            期初 ¥{{ bal.balance_start.toFixed(2) }} → 期末 ¥{{ bal.balance_end?.toFixed(2) }}
          </span>
        </template>
      </ChartCard>
      <ChartCard kicker="Distribution" title="模型消费分布 (CNY)" :option="costDistOption" :has-data="!!dayModels.length" height="360px" />
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <ChartCard kicker="Cost by Type" title="消费类型明细" :option="costTypeOption" :has-data="!!dayModels.length" height="360px" />
      <ChartCard kicker="Daily Cost" title="本月每日消费" :option="monthCostOption" :has-data="!!costDayData.length" height="360px" />
    </div>

    <KeyRanking kicker="Daily Ranking" title="当日 Key 使用与费用排行" :windows="rankingWindows" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUsageStore } from '../stores/usage'
import { useChartTheme } from '../composables/useChartTheme'
import StatCard from '../components/StatCard.vue'
import ChartCard from '../components/ChartCard.vue'
import KeyRanking from '../components/KeyRanking.vue'
import { Gem, Zap, TrendingDown, Cpu } from 'lucide-vue-next'

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

const dailyItems = computed(() => store.dailyKeyRankings?.items ?? [])
const dayRequests = computed(() => dailyItems.value.reduce((s, r) => s + r.request_count, 0))

const rankingWindows = computed(() => [{
  key: 'day',
  label: dateStr.value,
  items: dailyItems.value,
  costAvailable: !!store.dailyKeyRankings?.cost_available,
}])

const balanceOption = computed(() => ({
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
  store.fetchDailyKeyRankings(dateStr.value)
}

onMounted(() => loadData())
</script>

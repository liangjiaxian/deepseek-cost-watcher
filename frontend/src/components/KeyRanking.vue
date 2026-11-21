<template>
  <section class="card p-5">
    <div class="flex flex-wrap items-center justify-between gap-3 pb-4">
      <div class="min-w-0">
        <div class="kicker text-[10px] mb-1">{{ kicker }}</div>
        <div class="flex items-baseline gap-2">
          <h3 class="font-display text-sm font-medium tracking-tight text-text-primary">{{ title }}</h3>
          <span v-if="activeMetric.key === 'cost' && !activeWindow.costAvailable" class="note">
            费用数据采集中
          </span>
        </div>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <div v-if="windows.length > 1" class="segmented" role="group" aria-label="时间范围">
          <button
            v-for="w in windows" :key="w.key" type="button"
            class="seg-btn" :class="{ active: w.key === activeWindowKey }"
            @click="activeWindowKey = w.key"
          >{{ w.label }}</button>
        </div>
        <div class="segmented" role="group" aria-label="排序指标">
          <button
            v-for="m in metrics" :key="m.key" type="button"
            class="seg-btn" :class="{ active: m.key === activeMetricKey, disabled: m.key === 'cost' && !activeWindow.costAvailable }"
            :disabled="m.key === 'cost' && !activeWindow.costAvailable"
            @click="selectMetric(m.key)"
          >{{ m.label }}</button>
        </div>
      </div>
    </div>

    <div v-if="ranked.length" class="-mx-2 overflow-x-auto">
      <table class="w-full min-w-[560px] text-sm">
        <thead>
          <tr class="border-b border-border-subtle">
            <th class="w-10 py-2 pl-2 text-left font-mono text-[10px] font-medium uppercase tracking-[0.12em] text-text-secondary">#</th>
            <th class="py-2 text-left font-mono text-[10px] font-medium uppercase tracking-[0.12em] text-text-secondary">Key</th>
            <th
              v-for="m in metrics" :key="m.key"
              class="py-2 text-right font-mono text-[10px] font-medium uppercase tracking-[0.12em]"
              :class="m.key === activeMetricKey ? 'text-kicker' : 'text-text-secondary'"
            >{{ m.header }}</th>
            <th class="w-44 py-2 pr-2 text-right font-mono text-[10px] font-medium uppercase tracking-[0.12em] text-text-secondary">占比</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in ranked" :key="row.tracking_id"
            class="border-b border-border-subtle last:border-0 hover:bg-surface-hover"
          >
            <td class="py-2.5 pl-2 font-mono text-sm font-bold" :class="rankClass(index + 1)">{{ index + 1 }}</td>
            <td class="py-2.5 pr-4">
              <div class="truncate text-sm text-text-primary">{{ row.name }}</div>
              <div class="truncate font-mono text-xs text-text-tertiary">{{ row.sensitive_id }}</div>
            </td>
            <td
              v-for="m in metrics" :key="m.key"
              class="py-2.5 text-right font-mono tabular-nums"
              :class="m.key === activeMetricKey ? 'text-text-primary font-semibold' : 'text-text-secondary'"
            >{{ m.key === 'cost' && !activeWindow.costAvailable ? '—' : m.format(m.get(row)) }}</td>
            <td class="py-2.5 pr-2">
              <div class="flex items-center justify-end gap-2">
                <div class="h-1.5 w-24 overflow-hidden bg-border-subtle">
                  <div class="h-full bg-chart-1" :style="{ width: share(row) + '%' }"></div>
                </div>
                <span class="w-9 text-right font-mono tabular-nums text-xs text-text-secondary">{{ share(row).toFixed(0) }}%</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="py-10 text-center text-sm text-text-secondary">暂无使用数据</p>
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  title: String,
  // Small mono uppercase label above the title (Bifrost kicker)
  kicker: { type: String, default: 'Key Ranking' },
  // [{ key, label, items: [], costAvailable: bool }] — one entry hides the range switch
  windows: { type: Array, default: () => [] },
})

const metrics = [
  { key: 'cost', label: '费用', header: '费用 (¥)', get: (r) => r.cost, format: (v) => `¥${Number(v).toFixed(4)}` },
  { key: 'requests', label: '请求数', header: '请求数', get: (r) => r.request_count, format: (v) => Number(v).toLocaleString() },
  { key: 'tokens', label: 'Token', header: 'Token', get: (r) => r.total_tokens, format: (v) => Number(v).toLocaleString() },
]

const activeWindowKey = ref(props.windows[0]?.key)
// Cost leads; falls back to requests until the cost backfill has run.
const activeMetricKey = ref('cost')

const activeWindow = computed(() =>
  props.windows.find((w) => w.key === activeWindowKey.value) ?? props.windows[0] ?? { items: [], costAvailable: false }
)
const activeMetric = computed(() => metrics.find((m) => m.key === activeMetricKey.value) ?? metrics[0])

const ranked = computed(() => {
  const items = [...(activeWindow.value.items ?? [])]
  items.sort((a, b) => activeMetric.value.get(b) - activeMetric.value.get(a) || b.total_tokens - a.total_tokens)
  return items
})

// Share of the selected metric's total across all keys in the active window
// (today / last 30 days / year), so rows sum to ~100% instead of always
// topping out at the #1 row.
const totalValue = computed(() =>
  ranked.value.reduce((sum, r) => sum + (Number(activeMetric.value.get(r)) || 0), 0)
)

function share(row) {
  if (!totalValue.value) return 0
  return ((Number(activeMetric.value.get(row)) || 0) / totalValue.value) * 100
}

function rankClass(rank) {
  if (rank === 1) return 'text-warning'
  if (rank <= 3) return 'text-text-primary'
  return 'text-text-secondary'
}

watch(
  () => props.windows,
  (wins) => {
    if (!wins.some((w) => w.key === activeWindowKey.value)) activeWindowKey.value = wins[0]?.key
  },
  { deep: true }
)

// Never rank by a metric that has no data for this window; once cost data
// arrives, restore the cost-first default (unless the user picked a metric).
let autoCostFallback = false

function selectMetric(key) {
  autoCostFallback = false
  activeMetricKey.value = key
}

watch(
  () => activeWindow.value.costAvailable,
  (available) => {
    if (!available && activeMetricKey.value === 'cost') {
      activeMetricKey.value = 'requests'
      autoCostFallback = true
    } else if (available && autoCostFallback && activeMetricKey.value === 'requests') {
      activeMetricKey.value = 'cost'
      autoCostFallback = false
    }
  },
  { immediate: true }
)
</script>


<template>
  <div class="card p-5">
    <div class="flex items-start justify-between gap-2">
      <div
        class="w-10 h-10 rounded-md flex items-center justify-center shrink-0"
        :style="{ backgroundColor: color + '18', color }"
      >
        <component :is="icon" :size="20" />
      </div>
      <div v-if="trend !== undefined && trend !== null" class="flex items-center gap-0.5 text-xs font-medium whitespace-nowrap"
        :class="trend >= 0 ? 'text-success' : 'text-danger'">
        <TrendingUp v-if="trend >= 0" :size="14" />
        <TrendingDown v-else :size="14" />
        {{ trend >= 0 ? '+' : '' }}{{ trend }}%
      </div>
    </div>
    <div class="mt-3">
      <div class="text-2xl font-bold font-display tracking-tight text-text-primary truncate leading-none">{{ formattedValue }}</div>
      <div class="text-xs text-text-secondary mt-1">{{ label }}</div>

      <!-- Optional breakdown, e.g. granted vs topped-up balance -->
      <dl v-if="details?.length" class="mt-3 space-y-1 border-t border-surface-border pt-2">
        <div v-for="d in details" :key="d.label" class="flex items-center justify-between gap-2 text-xs">
          <dt class="text-text-secondary truncate">{{ d.label }}</dt>
          <dd class="font-mono tabular-nums text-text-primary whitespace-nowrap">{{ d.value }}</dd>
        </div>
      </dl>

      <!-- Optional state line, e.g. whether the balance can serve API calls -->
      <div
        v-if="status"
        class="mt-2 flex items-center gap-1.5 text-xs"
        :class="status.ok ? 'text-success' : 'text-danger'"
      >
        <span class="w-1.5 h-1.5 rounded-full shrink-0" :class="status.ok ? 'bg-success' : 'bg-danger'"></span>
        <span class="truncate">{{ status.text }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'

const props = defineProps({
  icon: { type: Object, required: true },
  label: { type: String, required: true },
  value: { type: [Number, String], default: 0 },
  color: { type: String, default: '#4F8CFF' },
  trend: { type: Number, default: null },
  format: { type: String, default: 'number' },
  // [{ label, value }] rendered as a bordered sub-list under the label
  details: { type: Array, default: null },
  // { ok: Boolean, text: String } rendered as a status dot + label
  status: { type: Object, default: null },
})

const formattedValue = computed(() => {
  if (typeof props.value === 'string') return props.value
  if (props.value == null) return '--'
  if (props.format === 'currency') {
    return `¥${Number(props.value).toFixed(2)}`
  }
  return Number(props.value).toLocaleString()
})
</script>

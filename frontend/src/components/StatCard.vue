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

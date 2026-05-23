<template>
  <div class="flex items-center gap-2 text-xs" :class="textColor">
    <span class="w-2 h-2 rounded-full" :class="dotColor"></span>
    <span class="text-text-secondary">{{ label }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, default: 'ok' },
  labels: { type: Object, default: () => ({ ok: '正常', warning: '警告', error: '异常' }) },
})

const dotColor = computed(() => {
  if (props.status === 'ok') return 'bg-success'
  if (props.status === 'warning') return 'bg-warning'
  return 'bg-danger'
})

const textColor = computed(() => {
  if (props.status === 'ok') return 'text-success'
  if (props.status === 'warning') return 'text-warning'
  return 'text-danger'
})

const label = computed(() => props.labels[props.status] || props.status)
</script>

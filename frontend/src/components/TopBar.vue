<template>
  <header class="h-16 flex items-center justify-between px-4 lg:px-6 border-b border-surface-border bg-bg shrink-0">
    <div class="flex items-center gap-3">
      <button class="btn-ghost p-1.5 md:hidden" @click="$emit('toggle-sidebar')">
        <Menu :size="20" />
      </button>
      <h1 class="text-lg font-semibold text-text-primary">{{ pageTitle }}</h1>
    </div>
    <div class="flex items-center gap-3">
      <select
        v-model="store.timeRange"
        @change="onRangeChange"
        class="input text-xs py-1.5 w-28 lg:w-32"
      >
        <option v-for="opt in store.timeRangeOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <button
        class="btn-ghost flex items-center gap-1.5 text-xs whitespace-nowrap"
        :class="{ 'text-brand': store.autoRefresh }"
        @click="store.toggleAutoRefresh()"
      >
        <span class="w-2 h-2 rounded-full" :class="store.autoRefresh ? 'bg-success' : 'bg-text-tertiary'"></span>
        <span class="hidden sm:inline">{{ store.autoRefresh ? '自动刷新' : '已暂停' }}</span>
      </button>
      <button class="btn-primary text-xs flex items-center gap-1.5 whitespace-nowrap" @click="$emit('refresh')" :disabled="loading">
        <RefreshCw :size="14" :class="{ 'animate-spin': loading }" />
        <span class="hidden sm:inline">刷新</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '../stores/app'
import { RefreshCw, Menu } from 'lucide-vue-next'

defineProps({ loading: Boolean })
defineEmits(['refresh', 'toggle-sidebar'])

const route = useRoute()
const store = useAppStore()

const pageTitles = {
  '/dashboard': '实时监测',
  '/daily': '每日报告',
  '/weekly': '每周报告',
  '/scheduler-logs': '调度日志',
  '/settings': '设置',
}
const pageTitle = computed(() => pageTitles[route.path] || '')

function onRangeChange() {
  store.setTimeRange(store.timeRange)
}
</script>

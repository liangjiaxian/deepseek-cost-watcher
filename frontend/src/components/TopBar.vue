<template>
  <header
    class="h-16 flex items-center justify-between px-4 lg:px-6 border-b border-border-subtle bg-translucent backdrop-blur-[16px] shrink-0 sticky top-0 z-10 overflow-hidden"
  >
    <span class="corner-motif right-0 top-0" aria-hidden="true"></span>
    <div class="relative flex items-center gap-3 min-w-0">
      <button class="btn-ghost p-1.5 md:hidden" @click="$emit('toggle-sidebar')">
        <Menu :size="20" />
      </button>
      <div class="min-w-0">
        <div class="kicker text-[10px] truncate">{{ pageKicker }}</div>
        <h1 class="font-display font-medium text-lg leading-tight tracking-tight text-text-primary truncate">{{ pageTitle }}</h1>
      </div>
    </div>
    <div class="relative flex items-center gap-3">
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

const pages = {
  '/dashboard': { kicker: 'Monitor', title: '实时监测' },
  '/daily': { kicker: 'Daily Report', title: '每日报告' },
  '/weekly': { kicker: 'Weekly Report', title: '每周报告' },
  '/monthly': { kicker: 'Monthly Report', title: '每月报告' },
  '/scheduler-logs': { kicker: 'Scheduler Log', title: '调度日志' },
  '/settings': { kicker: 'Settings', title: '设置' },
}
const pageTitle = computed(() => pages[route.path]?.title || '')
const pageKicker = computed(() => pages[route.path]?.kicker || '')

function onRangeChange() {
  store.setTimeRange(store.timeRange)
}
</script>

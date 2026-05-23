<template>
  <aside
    class="w-[260px] min-w-[260px] bg-surface border-r border-surface-border flex flex-col fixed md:static z-30 h-full transition-transform duration-200"
    :class="mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
  >
    <div class="h-16 flex items-center gap-3 px-6 border-b border-surface-border shrink-0">
      <div class="w-8 h-8 rounded-lg bg-brand flex items-center justify-center text-white font-bold text-sm">D</div>
      <span class="font-semibold text-base text-text-primary">DeepSeek Monitor</span>
    </div>
    <nav class="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
      <router-link
        v-for="item in navItems" :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors duration-150"
        :class="$route.path === item.path
          ? 'bg-brand-subtle text-brand font-medium'
          : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'"
        @click="$emit('close')"
      >
        <component :is="item.icon" :size="18" />
        {{ item.label }}
      </router-link>
    </nav>
    <div class="px-6 py-4 border-t border-surface-border shrink-0">
      <div class="flex items-center gap-2 text-xs text-text-secondary">
        <div class="w-2 h-2 rounded-full" :class="statusClass"></div>
        {{ statusText }}
      </div>
    </div>
  </aside>
  <div
    v-if="mobileOpen"
    class="fixed inset-0 bg-black/30 z-20 md:hidden"
    @click="$emit('close')"
  />
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from '../stores/settings'
import {
  LayoutDashboard, CalendarDays, CalendarCheck, Settings, Clock,
} from 'lucide-vue-next'

defineProps({ mobileOpen: Boolean })
defineEmits(['close'])

const route = useRoute()
const store = useSettingsStore()

const navItems = [
  { path: '/dashboard', label: '实时监测', icon: LayoutDashboard },
  { path: '/daily', label: '每日报告', icon: CalendarDays },
  { path: '/weekly', label: '每周报告', icon: CalendarCheck },
  { path: '/scheduler-logs', label: '调度日志', icon: Clock },
  { path: '/settings', label: '设置', icon: Settings },
]

const statusClass = computed(() => {
  const s = store.status
  if (!s) return 'bg-text-tertiary'
  if (s.status === 'ok') return 'bg-success'
  if (s.status === 'no_key') return 'bg-warning'
  return 'bg-danger'
})

const statusText = computed(() => {
  const s = store.status
  if (!s) return '检测中...'
  if (s.status === 'ok') return `已连接 · ${s.keys_configured} Key`
  if (s.status === 'no_key') return '未配置 API Key'
  return '连接异常'
})

onMounted(() => store.fetchStatus())
</script>

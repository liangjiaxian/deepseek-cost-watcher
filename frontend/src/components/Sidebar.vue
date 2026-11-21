<template>
  <aside
    class="w-[260px] min-w-[260px] bg-surface border-r border-border-subtle flex flex-col fixed md:static z-30 h-full transition-transform duration-200"
    :class="mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
  >
    <!-- Brand block: serif wordmark + mono kicker, Bifrost pixel corner behind -->
    <div class="relative h-16 flex items-center gap-3 px-6 border-b border-border-subtle shrink-0 overflow-hidden">
      <span class="corner-motif -right-10 -top-12" aria-hidden="true"></span>
      <div class="relative w-8 h-8 bg-brand flex items-center justify-center text-on-brand font-bold text-sm">D</div>
      <div class="relative min-w-0">
        <div class="font-display font-medium text-base leading-tight tracking-tight text-text-primary truncate">DeepSeek Monitor</div>
        <div class="note mt-0.5 text-[10px] tracking-[0.14em] uppercase truncate">Usage &amp; Cost</div>
      </div>
    </div>

    <nav class="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
      <div class="kicker px-3 pb-2 text-text-secondary">Menu</div>
      <router-link
        v-for="(item, index) in navItems" :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-3 py-2.5 text-sm transition-colors duration-150"
        :class="$route.path === item.path
          ? 'bg-brand-subtle text-kicker font-medium'
          : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'"
        @click="$emit('close')"
      >
        <component :is="item.icon" :size="16" class="shrink-0" />
        <span class="flex-1">{{ item.label }}</span>
        <span
          class="font-mono text-[10px] font-medium"
          :class="$route.path === item.path ? 'text-kicker' : 'text-text-tertiary'"
        >{{ String(index + 1).padStart(2, '0') }}</span>
      </router-link>
    </nav>

    <div class="px-6 py-4 border-t border-border-subtle shrink-0">
      <div class="kicker mb-1.5 text-text-secondary">Status</div>
      <div class="flex items-center gap-2 text-xs text-text-secondary">
        <div class="w-2 h-2 rounded-full" :class="statusClass"></div>
        <span class="note">{{ statusText }}</span>
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

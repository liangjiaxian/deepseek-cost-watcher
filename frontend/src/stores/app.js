import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const currentRoute = ref('Dashboard')
  const autoRefresh = ref(true)
  const refreshInterval = ref(10000)
  const timeRange = ref('24h')
  // index.html resolves the effective theme before mount (stored → system → URL),
  // so read the applied class instead of assuming a default.
  const theme = ref(document.documentElement.classList.contains('dark') ? 'dark' : 'light')

  const isDark = computed(() => theme.value === 'dark')

  const timeRangeOptions = [
    { label: '最近 1 小时', value: '1h' },
    { label: '最近 6 小时', value: '6h' },
    { label: '最近 24 小时', value: '24h' },
    { label: '最近 7 天', value: '7d' },
  ]

  function setRoute(name) { currentRoute.value = name }
  function toggleAutoRefresh() { autoRefresh.value = !autoRefresh.value }
  function setTimeRange(range) { timeRange.value = range }

  function setTheme(t) {
    theme.value = t
    localStorage.setItem('theme', t)
    if (t === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  function toggleTheme() {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  return {
    currentRoute, autoRefresh, refreshInterval, timeRange, theme, isDark,
    timeRangeOptions, setRoute, toggleAutoRefresh, setTimeRange,
    setTheme, toggleTheme,
  }
})

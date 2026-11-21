import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const currentRoute = ref('Dashboard')
  const autoRefresh = ref(true)
  const refreshInterval = ref(10000)
  // index.html resolves the effective theme before mount (stored → system → URL),
  // so read the applied class instead of assuming a default.
  const theme = ref(document.documentElement.classList.contains('dark') ? 'dark' : 'light')

  const isDark = computed(() => theme.value === 'dark')

  function setRoute(name) { currentRoute.value = name }
  function toggleAutoRefresh() { autoRefresh.value = !autoRefresh.value }

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
    currentRoute, autoRefresh, refreshInterval, theme, isDark,
    setRoute, toggleAutoRefresh,
    setTheme, toggleTheme,
  }
})

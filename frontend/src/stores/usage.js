import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getBalanceTrend, getUsageCost,
  getDailyBalance, getWeeklyCost, getKeyRankings, getDailyKeyRankings, getWeeklyKeyRankings,
} from '../api'

export const useUsageStore = defineStore('usage', () => {
  const balanceTrend = ref(null)
  const usageCost = ref(null)
  const dailyBalance = ref(null)
  const weeklyCost = ref(null)
  const keyRankings = ref(null)
  const dailyKeyRankings = ref([])
  const weeklyKeyRankings = ref([])
  const loading = ref(false)
  const error = ref(null)

  const balance = computed(() => {
    if (!balanceTrend.value?.points?.length) return null
    const pts = balanceTrend.value.points
    return pts[pts.length - 1].balance
  })

  async function fetchBalanceTrend(range) {
    try {
      const res = await getBalanceTrend(range)
      balanceTrend.value = res.data
    } catch (e) { error.value = e.message }
  }

  async function fetchUsageCost(year, month, refresh = false) {
    try {
      const res = await getUsageCost(year, month, refresh)
      usageCost.value = res.data
    } catch (e) { error.value = e.message }
  }

  async function fetchWeeklyCost(year, week) {
    try {
      const res = await getWeeklyCost(year, week)
      weeklyCost.value = res.data
    } catch (e) { error.value = e.message }
  }

  async function fetchDailyBalance(date) {
    try {
      const res = await getDailyBalance(date)
      dailyBalance.value = res.data
    } catch (e) { error.value = e.message }
  }
  async function fetchKeyRankings() { try { keyRankings.value = (await getKeyRankings()).data } catch (e) { error.value = e.message } }
  async function fetchDailyKeyRankings(date) { try { dailyKeyRankings.value = (await getDailyKeyRankings(date)).data } catch (e) { error.value = e.message } }
  async function fetchWeeklyKeyRankings(year, week) { try { weeklyKeyRankings.value = (await getWeeklyKeyRankings(year, week)).data } catch (e) { error.value = e.message } }

  async function refreshAll() {
    loading.value = true
    error.value = null
    await Promise.allSettled([
      fetchBalanceTrend('7d'),
      fetchUsageCost(undefined, undefined, true),
    ])
    loading.value = false
  }

  return {
    balanceTrend, usageCost, dailyBalance, weeklyCost, keyRankings, dailyKeyRankings, weeklyKeyRankings,
    loading, error,
    balance,
    fetchBalanceTrend, fetchUsageCost,
    fetchDailyBalance, fetchWeeklyCost, fetchKeyRankings, fetchDailyKeyRankings, fetchWeeklyKeyRankings, refreshAll,
  }
})

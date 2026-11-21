import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getBalanceTrend, getBalanceLatest, getUsageCost,
  getDailyBalance, getWeeklyCost, getKeyRankings, getDailyKeyRankings, getWeeklyKeyRankings,
} from '../api'

const EMPTY_RANKING = { items: [], cost_available: false }

export const useUsageStore = defineStore('usage', () => {
  const balanceTrend = ref(null)
  const balanceLatest = ref(null)
  const usageCost = ref(null)
  const dailyBalance = ref(null)
  const weeklyCost = ref(null)
  const keyRankings = ref(null)
  const dailyKeyRankings = ref({ ...EMPTY_RANKING })
  const weeklyKeyRankings = ref({ ...EMPTY_RANKING })
  const loading = ref(false)
  const error = ref(null)

  const balance = computed(() => {
    // Prefer the latest snapshot: it carries the grant/top-up split.
    if (balanceLatest.value?.balance != null) return balanceLatest.value.balance
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

  async function fetchBalanceLatest() {
    try {
      const res = await getBalanceLatest()
      balanceLatest.value = res.data
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
  async function fetchDailyKeyRankings(date) {
    try {
      dailyKeyRankings.value = (await getDailyKeyRankings(date)).data || { ...EMPTY_RANKING }
    } catch (e) { error.value = e.message }
  }
  async function fetchWeeklyKeyRankings(year, week) {
    try {
      weeklyKeyRankings.value = (await getWeeklyKeyRankings(year, week)).data || { ...EMPTY_RANKING }
    } catch (e) { error.value = e.message }
  }

  async function refreshAll() {
    loading.value = true
    error.value = null
    await Promise.allSettled([
      fetchBalanceTrend('7d'),
      fetchBalanceLatest(),
      fetchUsageCost(undefined, undefined, true),
    ])
    loading.value = false
  }

  return {
    balanceTrend, balanceLatest, usageCost, dailyBalance, weeklyCost, keyRankings, dailyKeyRankings, weeklyKeyRankings,
    loading, error,
    balance,
    fetchBalanceTrend, fetchBalanceLatest, fetchUsageCost,
    fetchDailyBalance, fetchWeeklyCost, fetchKeyRankings, fetchDailyKeyRankings, fetchWeeklyKeyRankings, refreshAll,
  }
})

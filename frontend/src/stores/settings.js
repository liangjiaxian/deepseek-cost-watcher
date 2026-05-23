import { defineStore } from 'pinia'
import { ref } from 'vue'
import { listKeys, addKey, deleteKey, testKey, getStatus, getPlatformTokenStatus, savePlatformToken, testPlatformToken } from '../api'

export const useSettingsStore = defineStore('settings', () => {
  const keys = ref([])
  const status = ref(null)
  const loading = ref(false)
  const platformTokenConfigured = ref(false)
  const platformTokenUpdatedAt = ref(null)

  async function fetchKeys() {
    try {
      const res = await listKeys()
      keys.value = res.data ?? []
    } catch (e) { console.error(e) }
  }

  async function addNewKey(name, keyValue) {
    const res = await addKey(name, keyValue)
    await fetchKeys()
    return res.data
  }

  async function removeKey(id) {
    await deleteKey(id)
    await fetchKeys()
  }

  async function checkKey(keyValue) {
    const res = await testKey(keyValue)
    return res.data
  }

  async function fetchStatus() {
    try {
      const res = await getStatus()
      status.value = res.data
    } catch (e) { status.value = { status: 'error', deepseek_connected: false } }
  }

  async function fetchPlatformTokenStatus() {
    try {
      const res = await getPlatformTokenStatus()
      platformTokenConfigured.value = res.data?.configured ?? false
      platformTokenUpdatedAt.value = res.data?.updated_at ?? null
    } catch (e) { console.error(e) }
  }

  async function savePlatform(token) {
    await savePlatformToken(token)
    platformTokenConfigured.value = true
    platformTokenUpdatedAt.value = new Date().toISOString()
  }

  async function checkPlatformToken(token) {
    const res = await testPlatformToken(token)
    return res.data
  }

  return { keys, status, loading, platformTokenConfigured, platformTokenUpdatedAt,
    fetchKeys, addNewKey, removeKey, checkKey, fetchStatus,
    fetchPlatformTokenStatus, savePlatform, checkPlatformToken }
})

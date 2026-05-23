import axios from 'axios'

const client = axios.create({
  baseURL: '/',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.detail || err.message
    console.error('[API Error]', msg)
    return Promise.reject(err)
  }
)

export function getBalanceTrend(range = '7d') {
  return client.get('/api/v1/usage/balance/trend', { params: { range } })
}

export function getUsageCost(year, month, refresh = false) {
  return client.get('/api/v1/usage/cost', { params: { year, month, refresh } })
}

export function getWeeklyCost(year, week) {
  return client.get('/api/v1/usage/cost/weekly', { params: { year, week } })
}

export function getDailyBalance(date) {
  return client.get('/api/v1/usage/balance/daily', { params: { date } })
}

export function getModels() {
  return client.get('/api/v1/models')
}

export function getStatus() {
  return client.get('/api/v1/status')
}

export function listKeys() {
  return client.get('/api/v1/settings/keys')
}

export function addKey(name, keyValue) {
  return client.post('/api/v1/settings/keys', { name, key_value: keyValue })
}

export function deleteKey(id) {
  return client.delete(`/api/v1/settings/keys/${id}`)
}

export function testKey(keyValue) {
  return client.post('/api/v1/settings/keys/test', { key_value: keyValue })
}

export function getConfig() {
  return client.get('/api/v1/settings/config')
}

export function updateConfig(configKey, configValue) {
  return client.put('/api/v1/settings/config', { config_key: configKey, config_value: configValue })
}

export function getPlatformTokenStatus() {
  return client.get('/api/v1/settings/platform-token')
}

export function savePlatformToken(token) {
  return client.put('/api/v1/settings/platform-token', { token })
}

export function testPlatformToken(token) {
  return client.post('/api/v1/settings/platform-token/test', { token })
}

export default client

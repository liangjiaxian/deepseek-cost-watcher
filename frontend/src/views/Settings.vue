<template>
  <div class="max-w-2xl space-y-8">
    <section>
      <h2 class="text-base font-semibold text-text-primary mb-4">主题</h2>
      <div class="card p-5 space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-sm text-text-primary">界面主题</span>
            <p class="text-xs text-text-secondary mt-0.5">深色用于沉浸监控，浅色用于日间协作</p>
          </div>
          <div class="flex items-center gap-1 bg-surface-hover rounded-md p-0.5">
            <button
              class="px-3 py-1.5 text-xs rounded-md transition-colors"
              :class="appStore.isDark ? 'btn-ghost' : 'bg-surface text-text-primary font-medium'"
              @click="appStore.setTheme('light')"
            >
              <Sun :size="14" class="inline mr-1" />浅色
            </button>
            <button
              class="px-3 py-1.5 text-xs rounded-md transition-colors"
              :class="!appStore.isDark ? 'btn-ghost' : 'bg-surface text-text-primary font-medium'"
              @click="appStore.setTheme('dark')"
            >
              <Moon :size="14" class="inline mr-1" />深色
            </button>
          </div>
        </div>
      </div>
    </section>

    <section>
      <h2 class="text-base font-semibold text-text-primary mb-4">API Key 管理</h2>
      <div class="card p-5 space-y-4">
        <div class="flex flex-col sm:flex-row gap-3">
          <input v-model="newKeyName" placeholder="名称（如：个人Key）" class="input flex-1" />
          <input v-model="newKeyValue" type="password" placeholder="sk-..." class="input flex-[2]" />
          <button class="btn-primary text-sm whitespace-nowrap" @click="addKeyHandler" :disabled="!newKeyName || !newKeyValue">
            添加
          </button>
        </div>
        <div v-if="testResult" class="text-xs flex items-center gap-2"
          :class="testResult.success ? 'text-success' : 'text-danger'">
          <span class="w-1.5 h-1.5 rounded-full" :class="testResult.success ? 'bg-success' : 'bg-danger'"></span>
          {{ testResult.message }}<span v-if="testResult.balance != null"> · 余额: ¥{{ testResult.balance }}</span>
        </div>
        <div v-if="store.keys.length" class="space-y-2">
          <div v-for="k in store.keys" :key="k.id"
            class="flex items-center justify-between px-3 py-2.5 rounded-md bg-surface-hover/50 text-sm">
            <div class="flex items-center gap-3">
              <span class="font-medium text-text-primary">{{ k.name }}</span>
              <span class="text-text-tertiary font-mono text-xs">{{ k.key_prefix }}...</span>
              <span class="tag"
                :class="k.is_active ? 'bg-success/10 text-success' : 'bg-text-tertiary/10 text-text-tertiary'">
                {{ k.is_active ? '激活' : '禁用' }}
              </span>
            </div>
            <button class="text-danger/70 hover:text-danger text-xs" @click="removeKeyHandler(k.id)">删除</button>
          </div>
        </div>
        <div v-else class="text-sm text-text-tertiary text-center py-4">
          暂无 API Key，请添加
        </div>
      </div>
    </section>

    <section>
      <h2 class="text-base font-semibold text-text-primary mb-4">平台 Token（用于获取消费明细）</h2>
      <div class="card p-5 space-y-4">
        <p class="text-xs text-text-secondary">
          从 <code class="text-brand">platform.deepseek.com/usage</code> 的浏览器开发者工具 → 网络 → 请求头中拷贝 <code class="text-brand">Authorization: Bearer ...</code> 的值粘贴到下方。
          此 Token 通常有效期数小时至数天，过期后需重新拷贝。
        </p>
        <div class="flex flex-col sm:flex-row gap-3">
          <input v-model="platformToken" type="password" placeholder="Bearer 值..." class="input flex-1" />
          <button class="btn-primary text-sm whitespace-nowrap" @click="testPlatformTokenHandler" :disabled="!platformToken || testingPlatform">
            {{ testingPlatform ? '验证中...' : '验证' }}
          </button>
          <button class="btn-primary text-sm whitespace-nowrap" @click="savePlatformTokenHandler" :disabled="!platformToken || !platformTestOk">
            保存
          </button>
        </div>
        <div v-if="platformTestMsg" class="text-xs flex items-center gap-2"
          :class="platformTestOk ? 'text-success' : 'text-danger'">
          <span class="w-1.5 h-1.5 rounded-full" :class="platformTestOk ? 'bg-success' : 'bg-danger'"></span>
          {{ platformTestMsg }}
        </div>
        <div class="text-xs text-text-secondary space-y-1">
          <div class="flex justify-between">
            <span>状态</span>
            <span :class="store.platformTokenConfigured ? 'text-success' : 'text-text-tertiary'">
              {{ store.platformTokenConfigured ? '已配置' : '未配置' }}
            </span>
          </div>
          <div v-if="store.platformTokenUpdatedAt" class="flex justify-between">
            <span>上次更新</span>
            <span class="font-mono">{{ formatTime(store.platformTokenUpdatedAt) }}</span>
          </div>
        </div>
      </div>
    </section>

    <section>
      <h2 class="text-base font-semibold text-text-primary mb-4">系统配置</h2>
      <div class="card p-5 space-y-4">
        <div class="flex items-center justify-between">
          <span class="text-sm text-text-primary">自动刷新</span>
          <button
            class="w-9 h-5 rounded-full transition-colors relative"
            :class="appStore.autoRefresh ? 'bg-brand' : 'bg-surface-border'"
            @click="appStore.toggleAutoRefresh()"
          >
            <span class="absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white transition-transform"
              :class="appStore.autoRefresh ? 'translate-x-4' : 'translate-x-0'"></span>
          </button>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-text-primary">刷新间隔</span>
          <select v-model="intervalLabel" class="input text-xs w-32" @change="onIntervalChange">
            <option value="10000">10 秒</option>
            <option value="30000">30 秒</option>
            <option value="60000">60 秒</option>
          </select>
        </div>
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="text-sm text-text-primary">后台轮询间隔</span>
          <div class="flex items-center gap-2 flex-wrap">
            <select v-model="pollInterval" class="input text-xs w-28">
              <option value="1">1 分钟</option>
              <option value="5">5 分钟</option>
              <option value="10">10 分钟</option>
              <option value="30">30 分钟</option>
            </select>
            <button class="btn-primary text-xs" @click="savePollInterval" :disabled="saving">{{ saving ? '保存中...' : '保存' }}</button>
            <button class="btn-ghost text-xs flex items-center gap-1" @click="triggerNow">
              <Play :size="12" />
              触发余额
            </button>
            <button class="btn-ghost text-xs flex items-center gap-1" @click="triggerCostNow">
              <Play :size="12" />
              触发消耗
            </button>
            <span v-if="triggerMsg" class="text-xs font-mono" :class="triggerMsgColor">{{ triggerMsg }}</span>
            <span v-if="costTriggerMsg" class="text-xs font-mono" :class="costTriggerMsgColor">{{ costTriggerMsg }}</span>
          </div>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm text-text-primary">数据保留天数</span>
          <input type="number" v-model="retentionDays" class="input text-xs w-20 text-center" min="1" max="365" />
        </div>
      </div>
    </section>

    <section>
      <h2 class="text-base font-semibold text-text-primary mb-4">服务状态</h2>
      <div class="card p-5 space-y-3">
        <div class="flex items-center gap-3 text-sm">
          <span class="w-2.5 h-2.5 rounded-full"
            :class="store.status?.deepseek_connected ? 'bg-success' : store.status?.keys_configured ? 'bg-danger' : 'bg-text-tertiary'">
          </span>
          <span class="text-text-primary">
            <template v-if="store.status?.deepseek_connected">DeepSeek API 已连接</template>
            <template v-else-if="store.status?.keys_configured">DeepSeek API 连接失败</template>
            <template v-else>未配置 API Key</template>
          </span>
          <span class="text-text-secondary text-xs">已配置 {{ store.status?.keys_configured ?? 0 }} 个 Key</span>
        </div>
        <div v-if="store.status?.scheduler" class="text-xs text-text-secondary space-y-1 border-t border-surface-border pt-3">
          <div class="flex justify-between">
            <span>轮询间隔</span>
            <span class="font-mono">{{ store.status.scheduler.interval_minutes }} 分钟</span>
          </div>
          <div class="flex justify-between">
            <span>下次执行</span>
            <span class="font-mono">{{ formatTime(store.status.scheduler.next_run_time) }}</span>
          </div>
          <div v-if="store.status.scheduler_last_run" class="flex justify-between">
            <span>上次执行</span>
            <span class="font-mono">{{ formatTime(store.status.scheduler_last_run) }}</span>
          </div>
          <div v-if="store.status.scheduler_last_status" class="flex justify-between">
            <span>上次状态</span>
            <span class="font-mono" :class="statusColor(store.status.scheduler_last_status)">{{ statusLabel(store.status.scheduler_last_status) }}</span>
          </div>
          <div v-if="store.status.scheduler_last_message" class="text-text-tertiary pt-1">
            {{ store.status.scheduler_last_message }}
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'
import { useAppStore } from '../stores/app'
import { useUsageStore } from '../stores/usage'
import { getConfig, updateConfig } from '../api'
import client from '../api'
import { Play, Sun, Moon } from 'lucide-vue-next'

const store = useSettingsStore()
const appStore = useAppStore()
const usageStore = useUsageStore()

const newKeyName = ref('')
const newKeyValue = ref('')
const testResult = ref(null)
const intervalLabel = ref(String(appStore.refreshInterval))
const retentionDays = ref(90)
const pollInterval = ref('30')
const saving = ref(false)
const triggerMsg = ref('')
const triggerMsgColor = ref('')
const costTriggerMsg = ref('')
const costTriggerMsgColor = ref('')
const platformToken = ref('')
const platformTestMsg = ref('')
const platformTestOk = ref(false)
const testingPlatform = ref(false)

async function loadConfig() {
  try {
    const res = await getConfig()
    const configs = res.data ?? []
    const found = configs.find(c => c.config_key === 'poll_interval')
    if (found) pollInterval.value = found.config_value
  } catch (e) {
    console.error('Failed to load config', e)
  }
}

async function addKeyHandler() {
  if (!newKeyName.value || !newKeyValue.value) return
  testResult.value = null
  const result = await store.checkKey(newKeyValue.value)
  testResult.value = result
  if (result.success) {
    await store.addNewKey(newKeyName.value, newKeyValue.value)
    newKeyName.value = ''
    newKeyValue.value = ''
    store.fetchStatus()
  }
}

async function removeKeyHandler(id) {
  await store.removeKey(id)
  store.fetchStatus()
}

function onIntervalChange() {
  appStore.refreshInterval = parseInt(intervalLabel.value)
}

async function savePollInterval() {
  saving.value = true
  try {
    await updateConfig('poll_interval', pollInterval.value)
  } catch (e) {
    console.error('Failed to update poll interval', e)
  } finally {
    saving.value = false
  }
}

async function triggerNow() {
  triggerMsg.value = ''
  try {
    await client.post('/api/v1/scheduler/trigger')
    triggerMsg.value = '✓ 已触发'
    triggerMsgColor.value = 'text-success'
    store.fetchStatus()
  } catch (e) {
    triggerMsg.value = '× 触发失败'
    triggerMsgColor.value = 'text-danger'
    console.error('Failed to trigger scheduler', e)
  }
  setTimeout(() => { triggerMsg.value = '' }, 5000)
}

async function triggerCostNow() {
  costTriggerMsg.value = ''
  try {
    await client.post('/api/v1/scheduler/trigger-cost')
    costTriggerMsg.value = '✓ 已触发'
    costTriggerMsgColor.value = 'text-success'
    store.fetchStatus()
  } catch (e) {
    costTriggerMsg.value = '× 触发失败'
    costTriggerMsgColor.value = 'text-danger'
    console.error('Failed to trigger cost poll', e)
  }
  setTimeout(() => { costTriggerMsg.value = '' }, 5000)
}

async function testPlatformTokenHandler() {
  if (!platformToken.value) return
  testingPlatform.value = true
  platformTestMsg.value = ''
  platformTestOk.value = false
  const result = await store.checkPlatformToken(platformToken.value)
  testingPlatform.value = false
  if (result?.success) {
    platformTestOk.value = true
    platformTestMsg.value = '✓ Token 有效'
  } else {
    platformTestMsg.value = `× ${result?.message || '验证失败'}`
  }
}

async function savePlatformTokenHandler() {
  if (!platformTestOk.value) return
  await store.savePlatform(platformToken.value)
  platformToken.value = ''
  platformTestMsg.value = '✓ 已保存'
}

function formatTime(val) {
  if (!val) return '--'
  try {
    const d = new Date(val)
    return d.toLocaleString('zh-CN', { hour12: false })
  } catch {
    return val
  }
}

function statusColor(status) {
  if (status === 'success') return 'text-success'
  if (status === 'error') return 'text-danger'
  return 'text-text-tertiary'
}

function statusLabel(status) {
  if (status === 'success') return '成功'
  if (status === 'error') return '失败'
  if (status === 'skipped') return '跳过'
  return status
}

onMounted(() => {
  store.fetchKeys()
  store.fetchStatus()
  store.fetchPlatformTokenStatus()
  loadConfig()
})
</script>

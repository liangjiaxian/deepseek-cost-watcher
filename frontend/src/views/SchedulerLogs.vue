<template>
  <div class="max-w-3xl space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-base font-semibold text-text-primary">调度执行记录</h2>
      <button class="btn-primary text-xs flex items-center gap-1.5" @click="loadLogs">
        <RefreshCw :size="14" />
        刷新
      </button>
    </div>

    <DataTable
      title="最近 10 次执行"
      :columns="columns"
      :rows="logs"
    >
      <template #cell-status="{ value }">
        <span class="inline-flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full" :class="statusDot(value)"></span>
          <span :class="statusText(value)">{{ statusLabel(value) }}</span>
        </span>
      </template>
      <template #cell-started_at="{ value }">
        <span class="font-mono text-xs text-text-primary">{{ formatTime(value) }}</span>
      </template>
      <template #cell-finished_at="{ value }">
        <span v-if="value" class="font-mono text-xs text-text-primary">{{ formatTime(value) }}</span>
        <span v-else class="text-text-tertiary">--</span>
      </template>
      <template #cell-duration="{ row }">
        <span class="font-mono text-xs text-text-primary">{{ calcDuration(row) }}</span>
      </template>
      <template #cell-message="{ value }">
        <span class="text-xs" :class="value ? 'text-text-secondary' : 'text-text-tertiary'">{{ value || '--' }}</span>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RefreshCw } from 'lucide-vue-next'
import DataTable from '../components/DataTable.vue'
import client from '../api'

const logs = ref([])

const columns = [
  { key: 'status', label: '状态' },
  { key: 'started_at', label: '开始时间' },
  { key: 'finished_at', label: '结束时间' },
  { key: 'duration', label: '耗时' },
  { key: 'message', label: '详情' },
]

async function loadLogs() {
  try {
    const res = await client.get('/api/v1/scheduler/logs?limit=10')
    logs.value = res.data ?? []
  } catch (e) {
    console.error('Failed to load scheduler logs', e)
  }
}

function statusDot(status) {
  if (status === 'success') return 'bg-success'
  if (status === 'error') return 'bg-danger'
  if (status === 'running') return 'bg-warning animate-pulse'
  return 'bg-text-tertiary'
}

function statusText(status) {
  if (status === 'success') return 'text-success'
  if (status === 'error') return 'text-danger'
  if (status === 'running') return 'text-warning'
  return 'text-text-tertiary'
}

function statusLabel(status) {
  if (status === 'success') return '成功'
  if (status === 'error') return '失败'
  if (status === 'skipped') return '跳过'
  if (status === 'running') return '运行中'
  return status
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

function calcDuration(row) {
  if (!row.started_at) return '--'
  const start = new Date(row.started_at)
  const end = row.finished_at ? new Date(row.finished_at) : new Date()
  const ms = end - start
  if (ms < 1000) return `${ms}ms`
  return `${(ms / 1000).toFixed(1)}s`
}

onMounted(() => loadLogs())
</script>

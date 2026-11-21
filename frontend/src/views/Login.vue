<template>
  <div class="relative min-h-screen bg-bg flex items-center justify-center p-4 overflow-hidden">
    <span class="corner-motif left-0 top-0" aria-hidden="true"></span>
    <span class="corner-motif right-0 bottom-0" aria-hidden="true"></span>

    <div class="card card-dots relative w-full max-w-[420px] p-8">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 bg-brand flex items-center justify-center text-on-brand font-bold">D</div>
        <div class="min-w-0">
          <div class="font-display font-medium text-base leading-tight tracking-tight text-text-primary truncate">DeepSeek Monitor</div>
          <div class="note mt-0.5 text-[10px] tracking-[0.14em] uppercase truncate">Usage &amp; Cost</div>
        </div>
      </div>

      <div class="mt-8">
        <div class="kicker text-[10px] mb-1">Secure Access</div>
        <h1 class="font-display text-[26px] leading-tight tracking-tight text-text-primary">输入访问密钥</h1>
      </div>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <label class="block">
          <span class="text-[11px] font-medium tracking-[0.08em] text-text-secondary">访问密钥</span>
          <div class="relative mt-1.5">
            <input
              ref="inputEl"
              v-model="keyInput"
              :type="showKey ? 'text' : 'password'"
              class="input w-full pr-10 font-mono"
              placeholder="请输入访问密钥"
              autocomplete="current-password"
              :disabled="submitting"
              @input="error = ''"
            />
            <button
              type="button"
              class="absolute inset-y-0 right-0 flex items-center px-3 text-text-tertiary hover:text-text-primary"
              tabindex="-1"
              :aria-label="showKey ? '隐藏密钥' : '显示密钥'"
              @click="showKey = !showKey"
            >
              <EyeOff v-if="showKey" :size="15" />
              <Eye v-else :size="15" />
            </button>
          </div>
        </label>

        <p v-if="error" class="text-xs text-danger">{{ error }}</p>

        <button
          type="submit"
          class="btn-primary w-full flex items-center justify-center gap-2"
          :disabled="!keyInput.trim() || submitting"
        >
          进入面板
          <ArrowRight :size="15" />
        </button>
      </form>

      <div class="mt-6 pt-4 border-t border-border-subtle flex items-center justify-between">
        <span class="note">LOCAL DASHBOARD</span>
        <span class="note">v0.1.0</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowRight, Eye, EyeOff } from 'lucide-vue-next'
import { login } from '../api'
import { isAuthenticated, setSession } from '../auth'

const route = useRoute()
const router = useRouter()

const keyInput = ref('')
const showKey = ref(false)
const error = ref('')
const submitting = ref(false)
const inputEl = ref(null)

const messages = {
  not_configured: '后端未配置 ACCESS_KEY，请联系部署者',
  invalid: '访问密钥不正确，请重试',
}

function targetPath() {
  const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : ''
  const safe = redirect.startsWith('/') && !redirect.startsWith('//') && redirect !== '/login'
  return safe ? redirect : '/dashboard'
}

async function submit() {
  if (submitting.value || !keyInput.value.trim()) return
  error.value = ''
  submitting.value = true
  try {
    const res = await login(keyInput.value.trim())
    const data = res?.data || {}
    if (!data.token) {
      error.value = '登录响应异常，请重试'
      return
    }
    const expiresAt = data.expires_at ? data.expires_at * 1000 : Date.now() + 72 * 60 * 60 * 1000
    setSession(data.token, expiresAt)
    router.replace(targetPath())
  } catch (err) {
    const status = err.response?.status
    if (status === 401) error.value = messages.invalid
    else if (status === 503) error.value = messages.not_configured
    else error.value = err.response?.data?.detail || '无法连接后端服务，请稍后重试'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  if (isAuthenticated()) {
    router.replace(targetPath())
  } else {
    inputEl.value?.focus()
  }
})
</script>

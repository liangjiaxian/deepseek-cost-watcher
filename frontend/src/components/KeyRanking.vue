<template>
  <section class="card p-4">
    <h3 class="text-sm font-semibold text-text-primary mb-4">{{ title }}</h3>
    <div v-if="items?.length" class="space-y-2">
      <div v-for="item in items" :key="item.tracking_id" class="flex items-center gap-3 rounded-lg px-2 py-2" :class="item.rank <= 3 ? 'bg-surface-hover' : ''">
        <span class="w-7 text-center font-bold" :class="item.rank === 1 ? 'text-yellow-400 text-lg' : item.rank === 2 ? 'text-slate-300 text-lg' : item.rank === 3 ? 'text-amber-600 text-lg' : 'text-text-secondary'">{{ item.rank }}</span>
        <div class="min-w-0 flex-1"><div class="truncate text-sm text-text-primary">{{ item.name }}</div><div class="truncate text-xs text-text-secondary">{{ item.sensitive_id }}</div></div>
        <div class="text-right"><div class="font-mono text-sm text-text-primary">{{ Number(item.total_tokens).toLocaleString() }}</div><div class="text-xs text-text-secondary">{{ item.request_count }} requests</div></div>
      </div>
    </div>
    <p v-else class="py-8 text-center text-sm text-text-secondary">暂无使用数据</p>
  </section>
</template>
<script setup>
defineProps({ title: String, items: { type: Array, default: () => [] } })
</script>

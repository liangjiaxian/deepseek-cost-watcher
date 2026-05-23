<template>
  <div class="card overflow-hidden">
    <div v-if="title" class="px-5 pt-4 pb-2 border-b border-surface-border">
      <h3 class="text-sm font-medium text-text-primary">{{ title }}</h3>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-text-secondary text-xs tracking-wider">
            <th v-for="col in columns" :key="col.key" class="text-left px-5 py-3 font-medium border-b border-border-subtle">
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in rows" :key="i"
            class="border-t border-border-subtle hover:bg-surface-hover transition-colors"
          >
            <td v-for="col in columns" :key="col.key" class="px-5 py-3 text-text-primary">
              <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
                {{ col.format ? col.format(row[col.key], row) : row[col.key] }}
              </slot>
            </td>
          </tr>
          <tr v-if="!rows.length">
            <td :colspan="columns.length" class="px-5 py-8 text-center text-text-tertiary text-sm">
              暂无数据
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  columns: { type: Array, default: () => [] },
  rows: { type: Array, default: () => [] },
})
</script>

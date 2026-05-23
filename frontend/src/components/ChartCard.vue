<template>
  <div class="card">
    <div v-if="title" class="flex items-center justify-between px-5 pt-4 pb-2">
      <h3 class="text-sm font-medium text-text-primary">{{ title }}</h3>
      <div v-if="$slots.actions" class="flex items-center gap-2">
        <slot name="actions" />
      </div>
    </div>
    <div class="p-1" :style="{ height }">
      <v-chart v-if="hasData" :option="option" autoresize />
      <div v-else class="flex items-center justify-center h-full text-text-tertiary text-sm">
        暂无数据
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  height: { type: String, default: '320px' },
  option: { type: Object, default: () => ({}) },
  hasData: { type: Boolean, default: false },
})
</script>

<script>
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  GridComponent, TooltipComponent, LegendComponent,
  TitleComponent, DatasetComponent,
} from 'echarts/components'

use([
  CanvasRenderer, LineChart, BarChart, PieChart,
  GridComponent, TooltipComponent, LegendComponent,
  TitleComponent, DatasetComponent,
])

export default { components: { VChart } }
</script>

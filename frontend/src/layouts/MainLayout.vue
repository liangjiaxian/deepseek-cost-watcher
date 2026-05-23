<template>
  <div class="flex h-screen overflow-hidden bg-bg">
    <Sidebar :mobile-open="sidebarOpen" @close="sidebarOpen = false" />
    <div class="flex-1 flex flex-col overflow-hidden md:ml-0">
      <TopBar :loading="usageStore.loading" @refresh="handleRefresh" @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main class="flex-1 overflow-y-auto p-4 lg:p-6">
        <router-view :key="refreshKey" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUsageStore } from '../stores/usage'
import { useAppStore } from '../stores/app'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'

const usageStore = useUsageStore()
const appStore = useAppStore()
const route = useRoute()
const refreshKey = ref(0)
const sidebarOpen = ref(false)

async function handleRefresh() {
  await usageStore.refreshAll()
  refreshKey.value++
}
</script>

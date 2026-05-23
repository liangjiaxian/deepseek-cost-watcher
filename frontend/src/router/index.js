import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('../views/Dashboard.vue'),
      },
    ],
  },
  {
    path: '/daily',
    name: 'Daily',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('../views/DailyReport.vue'),
      },
    ],
  },
  {
    path: '/weekly',
    name: 'Weekly',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('../views/WeeklyReport.vue'),
      },
    ],
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('../views/Settings.vue'),
      },
    ],
  },
  {
    path: '/scheduler-logs',
    name: 'SchedulerLogs',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('../views/SchedulerLogs.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

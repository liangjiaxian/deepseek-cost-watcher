import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../auth'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
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
    path: '/monthly',
    name: 'Monthly',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('../views/MonthlyReport.vue'),
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

router.beforeEach((to) => {
  if (to.name === 'Login') {
    return isAuthenticated() ? '/dashboard' : true
  }
  if (!isAuthenticated()) {
    return {
      name: 'Login',
      query: to.fullPath && to.fullPath !== '/' ? { redirect: to.fullPath } : {},
    }
  }
  return true
})

export default router

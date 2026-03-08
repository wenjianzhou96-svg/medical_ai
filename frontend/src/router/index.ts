import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// 静态路由
const staticRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/home/HomePage.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/user/LoginPage.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/user/RegisterPage.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/user/ForgotPasswordPage.vue'),
    meta: { title: '找回密码' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/user/ProfilePage.vue'),
    meta: { title: '个人中心', requiresAuth: true }
  },
  {
    path: '/consultation',
    name: 'Consultation',
    component: () => import('@/views/consultation/ConsultationList.vue'),
    meta: { title: '问诊列表', requiresAuth: true }
  },
  {
    path: '/consultation/new',
    name: 'ConsultationNew',
    component: () => import('@/views/consultation/ConsultationList.vue'),
    meta: { title: '发起问诊', requiresAuth: true }
  },
  {
    path: '/consultation/:id',
    name: 'ConsultationDetail',
    component: () => import('@/views/consultation/ConsultationDetail.vue'),
    meta: { title: '问诊详情', requiresAuth: true }
  },
  {
    path: '/consultation/chat/:id',
    name: 'ConsultationChat',
    component: () => import('@/views/consultation/ConsultationChat.vue'),
    meta: { title: '问诊对话', requiresAuth: true }
  },
  {
    path: '/consultation/report/:id',
    name: 'ConsultationReport',
    component: () => import('@/views/consultation/ConsultationDetail.vue'),
    meta: { title: '问诊报告', requiresAuth: true }
  },
  {
    path: '/health',
    name: 'Health',
    component: () => import('@/views/health/HealthRecord.vue'),
    meta: { title: '健康档案', requiresAuth: true }
  },
  {
    path: '/health/vitals',
    name: 'VitalSigns',
    component: () => import('@/views/health/VitalSigns.vue'),
    meta: { title: '体征数据', requiresAuth: true }
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/knowledge/KnowledgeSearch.vue'),
    meta: { title: '知识库' }
  },
  {
    path: '/knowledge/drugs',
    name: 'Drugs',
    component: () => import('@/views/knowledge/DrugList.vue'),
    meta: { title: '药品查询' }
  },
  // 管理后台路由
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'users',
        name: 'UserManage',
        component: () => import('@/views/admin/UserManage.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'doctors',
        name: 'DoctorManage',
        component: () => import('@/views/admin/DoctorManage.vue'),
        meta: { title: '医生管理' }
      },
      {
        path: 'articles',
        name: 'ArticleManage',
        component: () => import('@/views/admin/ArticleManage.vue'),
        meta: { title: '文章管理' }
      },
      {
        path: 'consultations',
        name: 'ConsultationManage',
        component: () => import('@/views/admin/ConsultationManage.vue'),
        meta: { title: '问诊管理' }
      },
      {
        path: 'roles',
        name: 'RoleManage',
        component: () => import('@/views/admin/RoleManage.vue'),
        meta: { title: '角色管理' }
      },
      {
        path: 'permissions',
        name: 'PermissionManage',
        component: () => import('@/views/admin/PermissionManage.vue'),
        meta: { title: '权限管理' }
      }
    ]
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes: staticRoutes,
  scrollBehavior: () => ({ left: 0, top: 0 })
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const title = to.meta.title as string
  if (title) {
    document.title = `${title} - 医疗智能体系统`
  }
  
  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }
  
  next()
})

export default router

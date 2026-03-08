import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '@/api/request'
import type { UserInfo, LoginForm, RegisterForm } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)
  const roles = ref<string[]>([])

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => roles.value.includes('admin'))
  const isDoctor = computed(() => roles.value.includes('doctor'))

  // Actions
  async function login(form: LoginForm) {
    const res = await request.post<{ token: { access_token: string; refresh_token: string; expires_in: number }; user: UserInfo }>('/auth/login', form)
    // 提取access_token存储
    token.value = res.token.access_token
    userInfo.value = res.user
    localStorage.setItem('token', res.token.access_token)
    localStorage.setItem('refresh_token', res.token.refresh_token)
    return res
  }

  async function register(form: RegisterForm) {
    const res = await request.post<{ token: { access_token: string; refresh_token: string; expires_in: number }; user: UserInfo }>('/auth/register', form)
    // 提取access_token存储
    token.value = res.token.access_token
    userInfo.value = res.user
    localStorage.setItem('token', res.token.access_token)
    localStorage.setItem('refresh_token', res.token.refresh_token)
    return res
  }

  async function logout() {
    await request.post('/auth/logout')
    token.value = ''
    userInfo.value = null
    roles.value = []
    localStorage.removeItem('token')
  }

  async function getUserInfo() {
    if (!token.value) return null
    try {
      const res = await request.get<UserInfo>('/auth/me')
      userInfo.value = res
      return res
    } catch (error: any) {
      // 如果是401错误，不清除token，让调用方处理
      if (error.response?.status === 401) {
        return null
      }
      token.value = ''
      userInfo.value = null
      localStorage.removeItem('token')
      return null
    }
  }

  function initUser() {
    if (token.value) {
      getUserInfo()
    }
  }

  return {
    token,
    userInfo,
    roles,
    isLoggedIn,
    isAdmin,
    isDoctor,
    login,
    register,
    logout,
    getUserInfo,
    initUser
  }
})

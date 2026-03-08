/**
 * 用户管理 API
 */

import request from '@/api/request'
import type { UserInfo } from '@/types/user'

// 用户列表查询
export function getUserList(params: {
  page?: number
  page_size?: number
  username?: string
  phone?: string
  email?: string
  status?: number
}) {
  return request.get<{
    list: UserInfo[]
    total: number
    page: number
    page_size: number
  }>('/users', params)
}

// 获取用户详情
export function getUserDetail(userId: number) {
  return request.get<UserInfo>(`/users/${userId}`)
}

// 创建用户（管理员）
export function createUser(data: {
  username: string
  password: string
  phone?: string
  email?: string
  nickname?: string
  gender?: number
  avatar_url?: string
}) {
  return request.post<UserInfo>('/users', data)
}

// 更新用户
export function updateUser(userId: number, data: {
  phone?: string
  email?: string
  nickname?: string
  avatar_url?: string
  gender?: number
  birthday?: string
}) {
  return request.put<UserInfo>(`/users/${userId}`, data)
}

// 删除用户
export function deleteUser(userId: number) {
  return request.delete(`/users/${userId}`)
}

// 修改密码
export function changePassword(userId: number, data: {
  old_password: string
  new_password: string
}) {
  return request.post(`/users/${userId}/change-password`, data)
}

// 重置密码（管理员）
export function resetPassword(userId: number, newPassword: string) {
  return request.post(`/users/${userId}/reset-password`, { new_password: newPassword })
}

// 分配角色
export function assignRoles(userId: number, roleIds: number[]) {
  return request.post(`/users/${userId}/assign-roles`, { role_ids: roleIds })
}

// 启用用户
export function enableUser(userId: number) {
  return request.post(`/users/${userId}/enable`)
}

// 禁用用户
export function disableUser(userId: number) {
  return request.post(`/users/${userId}/disable`)
}

// 获取用户角色
export function getUserRoles(userId: number) {
  return request.get<{ list: any[] }>(`/users/${userId}/roles`)
}

// 获取用户权限
export function getUserPermissions(userId: number) {
  return request.get<{ list: string[] }>(`/users/${userId}/permissions`)
}

/**
 * 角色管理 API
 */

// 角色列表查询
export function getRoleList(params: {
  page?: number
  page_size?: number
  status?: number
}) {
  return request.get<{
    list: any[]
    total: number
    page: number
    page_size: number
  }>('/roles', params)
}

// 获取角色详情
export function getRoleDetail(roleId: number) {
  return request.get<any>(`/roles/${roleId}`)
}

// 创建角色
export function createRole(data: {
  role_name: string
  description?: string
  status?: number
}) {
  return request.post<any>('/roles', data)
}

// 更新角色
export function updateRole(roleId: number, data: {
  role_name?: string
  description?: string
  status?: number
}) {
  return request.put<any>(`/roles/${roleId}`, data)
}

// 删除角色
export function deleteRole(roleId: number) {
  return request.delete(`/roles/${roleId}`)
}

// 为角色分配权限
export function assignPermissions(roleId: number, permissionIds: number[]) {
  return request.post(`/roles/${roleId}/permissions`, { permission_ids: permissionIds })
}

// 获取角色下的用户列表
export function getRoleUsers(roleId: number, params?: {
  page?: number
  page_size?: number
}) {
  return request.get<{ list: any[]; total: number }>(`/roles/${roleId}/users`, params)
}

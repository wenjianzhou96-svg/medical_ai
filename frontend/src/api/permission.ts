/**
 * 权限管理 API
 */

// 权限列表查询
export function getPermissionList(params: {
  page?: number
  page_size?: number
  resource?: string
}) {
  return request.get<{
    list: any[]
    total: number
    page: number
    page_size: number
  }>('/permissions', params)
}

// 获取权限详情
export function getPermissionDetail(permissionId: number) {
  return request.get<any>(`/permissions/${permissionId}`)
}

// 创建权限
export function createPermission(data: {
  permission_name: string
  resource: string
  action: string
  description?: string
}) {
  return request.post<any>('/permissions', data)
}

// 更新权限
export function updatePermission(permissionId: number, data: {
  permission_name?: string
  resource?: string
  action?: string
  description?: string
}) {
  return request.put<any>(`/permissions/${permissionId}`, data)
}

// 删除权限
export function deletePermission(permissionId: number) {
  return request.delete(`/permissions/${permissionId}`)
}

// 获取资源列表
export function getResourceList() {
  return request.get<{ list: any[] }>('/permissions/resources/list')
}

// 获取操作类型列表
export function getActionList() {
  return request.get<{ list: any[] }>('/permissions/actions/list')
}

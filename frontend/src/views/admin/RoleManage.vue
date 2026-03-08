<template>
  <div class="role-manage-page">
    <div class="page-header">
      <h2>角色管理</h2>
      <div class="header-actions">
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="handleSearch">
          <el-option label="全部" :value="undefined" />
          <el-option label="正常" :value="1" />
          <el-option label="禁用" :value="0" />
        </el-select>
        <el-button type="primary" :icon="Plus" @click="handleAdd">新增角色</el-button>
      </div>
    </div>

    <el-table v-loading="loading" :data="roles" stripe style="width: 100%">
      <el-table-column prop="role_id" label="角色ID" width="100" />
      <el-table-column prop="role_name" label="角色名称" width="150" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="user_count" label="用户数" width="100" />
      <el-table-column prop="permission_count" label="权限数" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
            {{ row.status === 1 ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="primary" size="small" @click="handleAssignPermission(row)">分配权限</el-button>
          <el-button link type="primary" size="small" @click="handleViewUsers(row)">查看用户</el-button>
          <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :total="total"
      layout="total, sizes, prev, pager, next, jumper"
      style="margin-top: 20px; justify-content: center"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
    />

    <!-- 新增/编辑角色弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" destroy-on-close>
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="角色名称" prop="role_name">
          <el-input v-model="formData.role_name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">正常</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 分配权限弹窗 -->
    <el-dialog v-model="permissionDialogVisible" title="分配权限" width="600px" destroy-on-close>
      <div v-if="currentRole">
        <p>角色：<strong>{{ currentRole.role_name }}</strong></p>
        <el-checkbox-group v-model="selectedPermissions">
          <div v-for="resource in permissionGroups" :key="resource.value" class="permission-group">
            <div class="group-title">{{ resource.label }}</div>
            <div class="group-items">
              <el-checkbox v-for="perm in resource.permissions" :key="perm.permission_id" :label="perm.permission_id">
                {{ perm.permission_name }}
              </el-checkbox>
            </div>
          </div>
        </el-checkbox-group>
      </div>
      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitPermission" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看用户弹窗 -->
    <el-dialog v-model="usersDialogVisible" title="角色用户列表" width="700px" destroy-on-close>
      <div v-if="currentRole">
        <p>角色：<strong>{{ currentRole.role_name }}</strong></p>
        <el-table :data="roleUsers" stripe>
          <el-table-column prop="user_id" label="用户ID" width="80" />
          <el-table-column prop="username" label="用户名" width="120" />
          <el-table-column prop="phone" label="手机号" width="130" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="status" label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
                {{ row.status === 1 ? '正常' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getRoleList, createRole, updateRole, deleteRole, assignPermissions, getRoleUsers } from '@/api/role'
import { getPermissionList } from '@/api/permission'

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const roles = ref<any[]>([])
const statusFilter = ref<number | undefined>(undefined)

// 弹窗相关
const dialogVisible = ref(false)
const dialogTitle = ref('')
const submitLoading = ref(false)
const formRef = ref<FormInstance>()
const currentRole = ref<any>(null)

const formData = reactive({
  role_id: undefined as number | undefined,
  role_name: '',
  description: '',
  status: 1
})

const formRules: FormRules = {
  role_name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '角色名称长度为2-50个字符', trigger: 'blur' }
  ]
}

// 权限分配弹窗
const permissionDialogVisible = ref(false)
const selectedPermissions = ref<number[]>([])
const allPermissions = ref<any[]>([])
const permissionGroups = ref<any[]>([])

// 查看用户弹窗
const usersDialogVisible = ref(false)
const roleUsers = ref<any[]>([])

// 加载角色列表
const loadRoles = async () => {
  loading.value = true
  try {
    const res = await getRoleList({
      page: currentPage.value,
      page_size: pageSize.value,
      status: statusFilter.value
    })
    roles.value = res.list
    total.value = res.total
  } catch (error) {
    console.error('加载角色列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载权限列表
const loadPermissions = async () => {
  try {
    const res = await getPermissionList({ page_size: 200 })
    allPermissions.value = res.list
    // 按资源分组
    const groups: any = {}
    res.list.forEach((perm: any) => {
      if (!groups[perm.resource]) {
        groups[perm.resource] = {
          value: perm.resource,
          label: getResourceLabel(perm.resource),
          permissions: []
        }
      }
      groups[perm.resource].permissions.push(perm)
    })
    permissionGroups.value = Object.values(groups)
  } catch (error) {
    console.error('加载权限列表失败:', error)
  }
}

const getResourceLabel = (resource: string) => {
  const labels: Record<string, string> = {
    user: '用户管理',
    role: '角色管理',
    permission: '权限管理',
    consultation: '问诊管理',
    health: '健康管理',
    article: '文章管理',
    comment: '评论管理',
    doctor: '医生管理',
    knowledge: '知识库管理',
    notification: '通知管理',
    system: '系统管理'
  }
  return labels[resource] || resource
}

const handleSearch = () => {
  currentPage.value = 1
  loadRoles()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadRoles()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadRoles()
}

const handleAdd = () => {
  formData.role_id = undefined
  formData.role_name = ''
  formData.description = ''
  formData.status = 1
  dialogTitle.value = '新增角色'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  formData.role_id = row.role_id
  formData.role_name = row.role_name
  formData.description = row.description || ''
  formData.status = row.status
  dialogTitle.value = '编辑角色'
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  
  submitLoading.value = true
  try {
    if (formData.role_id) {
      await updateRole(formData.role_id, {
        role_name: formData.role_name,
        description: formData.description,
        status: formData.status
      })
      ElMessage.success('角色更新成功')
    } else {
      await createRole({
        role_name: formData.role_name,
        description: formData.description,
        status: formData.status
      })
      ElMessage.success('角色创建成功')
    }
    dialogVisible.value = false
    loadRoles()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除角色 "${row.role_name}" 吗？`, '提示', {
      type: 'warning'
    })
    await deleteRole(row.role_id)
    ElMessage.success('删除成功')
    loadRoles()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const handleAssignPermission = async (row: any) => {
  currentRole.value = row
  await loadPermissions()
  // 获取当前角色的权限
  selectedPermissions.value = row.permissions?.map((p: any) => p.permission_id) || []
  permissionDialogVisible.value = true
}

const handleSubmitPermission = async () => {
  if (!currentRole.value) return
  submitLoading.value = true
  try {
    await assignPermissions(currentRole.value.role_id, selectedPermissions.value)
    ElMessage.success('权限分配成功')
    permissionDialogVisible.value = false
    loadRoles()
  } catch (error: any) {
    ElMessage.error(error.message || '权限分配失败')
  } finally {
    submitLoading.value = false
  }
}

const handleViewUsers = async (row: any) => {
  currentRole.value = row
  try {
    const res = await getRoleUsers(row.role_id)
    roleUsers.value = res.list
    usersDialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取用户列表失败')
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadRoles()
})
</script>

<style scoped lang="scss">
.role-manage-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
    }
    
    .header-actions {
      display: flex;
      gap: 10px;
    }
  }
  
  .permission-group {
    margin-bottom: 15px;
    
    .group-title {
      font-weight: bold;
      margin-bottom: 8px;
      padding: 5px 10px;
      background: #f5f7fa;
      border-radius: 4px;
    }
    
    .group-items {
      padding-left: 10px;
      
      .el-checkbox {
        margin-right: 15px;
        margin-bottom: 8px;
      }
    }
  }
}
</style>

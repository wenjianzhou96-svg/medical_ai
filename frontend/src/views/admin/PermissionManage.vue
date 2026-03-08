<template>
  <div class="permission-manage-page">
    <div class="page-header">
      <h2>权限管理</h2>
      <div class="header-actions">
        <el-select v-model="resourceFilter" placeholder="资源筛选" clearable @change="handleSearch">
          <el-option label="全部" :value="undefined" />
          <el-option v-for="res in resources" :key="res" :label="getResourceLabel(res)" :value="res" />
        </el-select>
        <el-button type="primary" :icon="Plus" @click="handleAdd">新增权限</el-button>
      </div>
    </div>

    <el-table v-loading="loading" :data="permissions" stripe style="width: 100%">
      <el-table-column prop="permission_id" label="权限ID" width="100" />
      <el-table-column prop="permission_name" label="权限名称" width="150" />
      <el-table-column prop="resource" label="资源" width="150">
        <template #default="{ row }">
          <el-tag>{{ getResourceLabel(row.resource) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="action" label="操作" width="150">
        <template #default="{ row }">
          <el-tag :type="getActionType(row.action)">{{ getActionLabel(row.action) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
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

    <!-- 新增/编辑权限弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" destroy-on-close>
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="权限名称" prop="permission_name">
          <el-input v-model="formData.permission_name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="资源" prop="resource">
          <el-select v-model="formData.resource" placeholder="请选择资源" filterable>
            <el-option v-for="res in resources" :key="res" :label="getResourceLabel(res)" :value="res" />
          </el-select>
        </el-form-item>
        <el-form-item label="操作" prop="action">
          <el-select v-model="formData.action" placeholder="请选择操作">
            <el-option v-for="act in actions" :key="act" :label="getActionLabel(act)" :value="act" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { 
  getPermissionList, 
  createPermission, 
  updatePermission, 
  deletePermission,
  getResourceList,
  getActionList
} from '@/api/permission'

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const permissions = ref<any[]>([])
const resources = ref<string[]>([])
const actions = ref<string[]>([])
const resourceFilter = ref<string | undefined>(undefined)

// 弹窗相关
const dialogVisible = ref(false)
const dialogTitle = ref('')
const submitLoading = ref(false)
const formRef = ref<FormInstance>()

const formData = reactive({
  permission_id: undefined as number | undefined,
  permission_name: '',
  resource: '',
  action: '',
  description: ''
})

const formRules: FormRules = {
  permission_name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' }
  ],
  resource: [
    { required: true, message: '请选择资源', trigger: 'change' }
  ],
  action: [
    { required: true, message: '请选择操作', trigger: 'change' }
  ]
}

// 资源标签映射
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

// 操作类型映射
const getActionLabel = (action: string) => {
  const labels: Record<string, string> = {
    create: '创建',
    read: '查看',
    update: '更新',
    delete: '删除',
    export: '导出',
    import: '导入'
  }
  return labels[action] || action
}

// 操作类型标签样式
const getActionType = (action: string) => {
  const types: Record<string, string> = {
    create: 'success',
    read: 'info',
    update: 'warning',
    delete: 'danger',
    export: '',
    import: ''
  }
  return types[action] || 'info'
}

// 加载权限列表
const loadPermissions = async () => {
  loading.value = true
  try {
    const res = await getPermissionList({
      page: currentPage.value,
      page_size: pageSize.value,
      resource: resourceFilter.value
    })
    permissions.value = res.list
    total.value = res.total
  } catch (error) {
    console.error('加载权限列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载资源和操作列表
const loadResourceAndActionLists = async () => {
  try {
    const [resRes, actRes] = await Promise.all([
      getResourceList(),
      getActionList()
    ])
    resources.value = resRes.list
    actions.value = actRes.list
  } catch (error) {
    console.error('加载资源/操作列表失败:', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadPermissions()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadPermissions()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadPermissions()
}

const handleAdd = () => {
  formData.permission_id = undefined
  formData.permission_name = ''
  formData.resource = ''
  formData.action = ''
  formData.description = ''
  dialogTitle.value = '新增权限'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  formData.permission_id = row.permission_id
  formData.permission_name = row.permission_name
  formData.resource = row.resource
  formData.action = row.action
  formData.description = row.description || ''
  dialogTitle.value = '编辑权限'
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  
  submitLoading.value = true
  try {
    if (formData.permission_id) {
      await updatePermission(formData.permission_id, {
        permission_name: formData.permission_name,
        resource: formData.resource,
        action: formData.action,
        description: formData.description
      })
      ElMessage.success('权限更新成功')
    } else {
      await createPermission({
        permission_name: formData.permission_name,
        resource: formData.resource,
        action: formData.action,
        description: formData.description
      })
      ElMessage.success('权限创建成功')
    }
    dialogVisible.value = false
    loadPermissions()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除权限 "${row.permission_name}" 吗？`, '提示', {
      type: 'warning'
    })
    await deletePermission(row.permission_id)
    ElMessage.success('删除成功')
    loadPermissions()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
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
  loadPermissions()
  loadResourceAndActionLists()
})
</script>

<style scoped lang="scss">
.permission-manage-page {
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
}
</style>

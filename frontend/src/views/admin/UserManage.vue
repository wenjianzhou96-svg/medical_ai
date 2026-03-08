<template>
  <div class="user-manage-page">
    <div class="page-header">
      <h2>用户管理</h2>
      <div class="header-actions">
        <el-input
          v-model="keyword"
          placeholder="搜索用户名/手机号/邮箱"
          class="search-input"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="handleSearch">
          <el-option label="全部" :value="undefined" />
          <el-option label="正常" :value="1" />
          <el-option label="禁用" :value="0" />
        </el-select>
        <el-button type="primary" :icon="Plus" @click="handleAdd">新增用户</el-button>
      </div>
    </div>

    <el-table v-loading="loading" :data="users" stripe style="width: 100%">
      <el-table-column prop="user_id" label="用户ID" width="80" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="email" label="邮箱" width="180" />
      <el-table-column prop="nickname" label="昵称" width="120" />
      <el-table-column prop="gender" label="性别" width="80">
        <template #default="{ row }">
          <span v-if="row.gender === 0">女</span>
          <span v-else-if="row.gender === 1">男</span>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
            {{ row.status === 1 ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_login_at" label="最后登录" width="170">
        <template #default="{ row }">
          {{ row.last_login_at ? formatDate(row.last_login_at) : '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="170">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="primary" size="small" @click="handleAssignRole(row)">分配角色</el-button>
          <el-button link :type="row.status === 1 ? 'danger' : 'success'" size="small" @click="handleToggleStatus(row)">
            {{ row.status === 1 ? '禁用' : '启用' }}
          </el-button>
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

    <!-- 新增/编辑用户弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" destroy-on-close>
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" :disabled="isEdit" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="formData.password" type="password" show-password placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="formData.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="formData.gender" placeholder="请选择性别">
            <el-option label="女" :value="0" />
            <el-option label="男" :value="1" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 分配角色弹窗 -->
    <el-dialog v-model="roleDialogVisible" title="分配角色" width="500px" destroy-on-close>
      <el-form label-width="80px">
        <el-form-item label="用户">
          <span>{{ currentUser?.username }}</span>
        </el-form-item>
        <el-form-item label="角色">
          <el-checkbox-group v-model="selectedRoles">
            <el-checkbox v-for="role in allRoles" :key="role.role_id" :label="role.role_id">
              {{ role.role_name }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitRole" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getUserList, createUser, updateUser, deleteUser, assignRoles, enableUser, disableUser, getUserRoles } from '@/api/user'
import { getRoleList } from '@/api/role'

const keyword = ref('')
const statusFilter = ref<number | undefined>(undefined)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)
const users = ref<any[]>([])

// 弹窗相关
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const submitLoading = ref(false)
const formRef = ref<FormInstance>()
const currentUser = ref<any>(null)

const formData = reactive({
  user_id: undefined as number | undefined,
  username: '',
  password: '',
  phone: '',
  email: '',
  nickname: '',
  gender: undefined as number | undefined
})

const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度为3-50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 100, message: '密码长度为6-100个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 角色分配弹窗
const roleDialogVisible = ref(false)
const selectedRoles = ref<number[]>([])
const allRoles = ref<any[]>([])

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const res = await getUserList({
      page: currentPage.value,
      page_size: pageSize.value,
      username: keyword.value || undefined,
      status: statusFilter.value
    })
    users.value = res.list
    total.value = res.total
  } catch (error) {
    console.error('加载用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载角色列表
const loadRoles = async () => {
  try {
    const res = await getRoleList({ page_size: 100 })
    allRoles.value = res.list
  } catch (error) {
    console.error('加载角色列表失败:', error)
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadUsers()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadUsers()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  loadUsers()
}

const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增用户'
  Object.assign(formData, {
    user_id: undefined,
    username: '',
    password: '',
    phone: '',
    email: '',
    nickname: '',
    gender: undefined
  })
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  isEdit.value = true
  dialogTitle.value = '编辑用户'
  Object.assign(formData, {
    user_id: row.user_id,
    username: row.username,
    password: '',
    phone: row.phone || '',
    email: row.email || '',
    nickname: row.nickname || '',
    gender: row.gender
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate()
  
  submitLoading.value = true
  try {
    if (isEdit.value) {
      await updateUser(formData.user_id!, {
        phone: formData.phone || undefined,
        email: formData.email || undefined,
        nickname: formData.nickname || undefined,
        gender: formData.gender
      })
      ElMessage.success('用户更新成功')
    } else {
      await createUser({
        username: formData.username,
        password: formData.password,
        phone: formData.phone || undefined,
        email: formData.email || undefined,
        nickname: formData.nickname || undefined,
        gender: formData.gender
      })
      ElMessage.success('用户创建成功')
    }
    dialogVisible.value = false
    loadUsers()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除用户 "${row.username}" 吗？`, '提示', {
      type: 'warning'
    })
    await deleteUser(row.user_id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const handleToggleStatus = async (row: any) => {
  try {
    if (row.status === 1) {
      await disableUser(row.user_id)
      ElMessage.success('已禁用')
    } else {
      await enableUser(row.user_id)
      ElMessage.success('已启用')
    }
    loadUsers()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

const handleAssignRole = async (row: any) => {
  currentUser.value = row
  try {
    // 获取用户当前角色
    const res = await getUserRoles(row.user_id)
    selectedRoles.value = res.list.map((r: any) => r.role_id)
    // 加载所有角色
    await loadRoles()
    roleDialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取用户角色失败')
  }
}

const handleSubmitRole = async () => {
  if (!currentUser.value) return
  submitLoading.value = true
  try {
    await assignRoles(currentUser.value.user_id, selectedRoles.value)
    ElMessage.success('角色分配成功')
    roleDialogVisible.value = false
  } catch (error: any) {
    ElMessage.error(error.message || '角色分配失败')
  } finally {
    submitLoading.value = false
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
  loadUsers()
})
</script>

<style scoped lang="scss">
.user-manage-page {
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
      
      .search-input {
        width: 250px;
      }
    }
  }
}
</style>

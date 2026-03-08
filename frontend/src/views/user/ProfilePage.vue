<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- 左侧菜单 -->
      <div class="profile-sidebar">
        <div class="user-info-card">
          <el-avatar :size="80" :src="userInfo?.avatar_url">
            <el-icon :size="40"><User /></el-icon>
          </el-avatar>
          <h3>{{ userInfo?.username }}</h3>
          <p>{{ userInfo?.email || userInfo?.phone }}</p>
        </div>
        <el-menu :default-active="activeMenu" @select="handleMenuSelect">
          <el-menu-item index="info">
            <el-icon><User /></el-icon>
            <span>个人信息</span>
          </el-menu-item>
          <el-menu-item index="security">
            <el-icon><Lock /></el-icon>
            <span>账号安全</span>
          </el-menu-item>
          <el-menu-item index="consultations">
            <el-icon><ChatDotRound /></el-icon>
            <span>我的问诊</span>
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 右侧内容 -->
      <div class="profile-content">
        <!-- 个人信息 -->
        <div v-if="activeMenu === 'info'" class="content-section">
          <h2 class="section-title">个人信息</h2>
          <el-form :model="profileForm" label-width="100px" class="profile-form">
            <el-form-item label="头像">
              <el-avatar :size="80" :src="profileForm.avatar_url">
                <el-icon :size="40"><User /></el-icon>
              </el-avatar>
              <el-upload
                class="avatar-upload"
                action="/api/v1/users/avatar"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
              >
                <el-button size="small" type="primary">更换头像</el-button>
              </el-upload>
            </el-form-item>
            <el-form-item label="用户名">
              <el-input v-model="profileForm.username" disabled />
            </el-form-item>
            <el-form-item label="昵称">
              <el-input v-model="profileForm.nickname" placeholder="请输入昵称" />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="性别">
              <el-radio-group v-model="profileForm.gender">
                <el-radio :label="1">男</el-radio>
                <el-radio :label="0">女</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="生日">
              <el-date-picker
                v-model="profileForm.birthday"
                type="date"
                placeholder="选择生日"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="saveProfile">
                保存修改
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 账号安全 -->
        <div v-if="activeMenu === 'security'" class="content-section">
          <h2 class="section-title">账号安全</h2>
          <div class="security-items">
            <div class="security-item">
              <div class="security-item-left">
                <el-icon :size="24"><Lock /></el-icon>
                <div class="security-item-info">
                  <h4>登录密码</h4>
                  <p>定期修改密码可以提高账号安全性</p>
                </div>
              </div>
              <el-button @click="showChangePasswordDialog = true">修改密码</el-button>
            </div>
            <div class="security-item">
              <div class="security-item-left">
                <el-icon :size="24"><Phone /></el-icon>
                <div class="security-item-info">
                  <h4>手机号</h4>
                  <p>{{ userInfo?.phone ? `已绑定: ${userInfo.phone}` : '未绑定手机号' }}</p>
                </div>
              </div>
              <el-button type="primary" @click="showBindPhoneDialog = true">
                {{ userInfo?.phone ? '更换手机号' : '绑定手机号' }}
              </el-button>
            </div>
            <div class="security-item">
              <div class="security-item-left">
                <el-icon :size="24"><Message /></el-icon>
                <div class="security-item-info">
                  <h4>邮箱</h4>
                  <p>{{ userInfo?.email ? `已绑定: ${userInfo.email}` : '未绑定邮箱' }}</p>
                </div>
              </div>
              <el-button type="primary" @click="showBindEmailDialog = true">
                {{ userInfo?.email ? '更换邮箱' : '绑定邮箱' }}
              </el-button>
            </div>
          </div>
        </div>

        <!-- 我的问诊 -->
        <div v-if="activeMenu === 'consultations'" class="content-section">
          <h2 class="section-title">我的问诊</h2>
          <div class="consultations-list">
            <el-empty v-if="consultations.length === 0" description="暂无问诊记录" />
            <el-card v-for="consultation in consultations" :key="consultation.consultation_id" class="consultation-card">
              <div class="consultation-header">
                <span class="consultation-id">问诊编号: {{ consultation.consultation_id }}</span>
                <el-tag :type="getStatusType(consultation.status)">
                  {{ getStatusText(consultation.status) }}
                </el-tag>
              </div>
              <div class="consultation-content">
                <p><strong>症状描述:</strong> {{ consultation.symptoms || '暂无' }}</p>
                <p><strong>创建时间:</strong> {{ formatDate(consultation.created_at) }}</p>
              </div>
              <div class="consultation-actions">
                <el-button type="primary" size="small" @click="viewConsultation(consultation.consultation_id)">
                  查看详情
                </el-button>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="showChangePasswordDialog" title="修改密码" width="400px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="80px">
        <el-form-item label="原密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showChangePasswordDialog = false">取消</el-button>
        <el-button type="primary" :loading="changingPassword" @click="changePassword">确认修改</el-button>
      </template>
    </el-dialog>

    <!-- 绑定手机号对话框 -->
    <el-dialog v-model="showBindPhoneDialog" title="绑定手机号" width="400px">
      <el-form :model="phoneForm" :rules="phoneRules" ref="phoneFormRef" label-width="80px">
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="phoneForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <div class="code-input">
            <el-input v-model="phoneForm.code" placeholder="请输入验证码" />
            <el-button :disabled="phoneCountdown > 0" @click="sendPhoneCode">
              {{ phoneCountdown > 0 ? `${phoneCountdown}秒` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBindPhoneDialog = false">取消</el-button>
        <el-button type="primary" :loading="bindingPhone" @click="bindPhone">确认绑定</el-button>
      </template>
    </el-dialog>

    <!-- 绑定邮箱对话框 -->
    <el-dialog v-model="showBindEmailDialog" title="绑定邮箱" width="400px">
      <el-form :model="emailForm" :rules="emailRules" ref="emailFormRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="emailForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <div class="code-input">
            <el-input v-model="emailForm.code" placeholder="请输入验证码" />
            <el-button :disabled="emailCountdown > 0" @click="sendEmailCode">
              {{ emailCountdown > 0 ? `${emailCountdown}秒` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBindEmailDialog = false">取消</el-button>
        <el-button type="primary" :loading="bindingEmail" @click="bindEmail">确认绑定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance } from 'element-plus'
import { User, Lock, ChatDotRound, Phone, Message } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import request from '@/api/request'

const router = useRouter()
const userStore = useUserStore()

const activeMenu = ref('info')
const saving = ref(false)
const consultations = ref<any[]>([])

// 个人信息表单
const profileForm = reactive({
  username: '',
  nickname: '',
  phone: '',
  email: '',
  avatar_url: '',
  gender: 1 as 0 | 1,
  birthday: ''
})

// 修改密码
const showChangePasswordDialog = ref(false)
const changingPassword = ref(false)
const passwordFormRef = ref<FormInstance>()
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 绑定手机号
const showBindPhoneDialog = ref(false)
const bindingPhone = ref(false)
const phoneCountdown = ref(0)
let phoneTimer: ReturnType<typeof setInterval> | null = null
const phoneFormRef = ref<FormInstance>()
const phoneForm = reactive({
  phone: '',
  code: ''
})
const phoneRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

// 绑定邮箱
const showBindEmailDialog = ref(false)
const bindingEmail = ref(false)
const emailCountdown = ref(0)
let emailTimer: ReturnType<typeof setInterval> | null = null
const emailFormRef = ref<FormInstance>()
const emailForm = reactive({
  email: '',
  code: ''
})
const emailRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }
  ],
  code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

const userInfo = ref(userStore.userInfo)

onMounted(async () => {
  // 先检查本地 token 是否存在
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  // 如果用户信息为空，尝试从API获取
  if (!userStore.userInfo) {
    try {
      const info = await userStore.getUserInfo()
      if (!info) {
        ElMessage.warning('登录已过期，请重新登录')
        router.push('/login')
        return
      }
    } catch (error) {
      console.error('获取用户信息失败', error)
      ElMessage.error('获取用户信息失败，请重新登录')
      router.push('/login')
      return
    }
  }
  initUserInfo()
})

const initUserInfo = () => {
  if (userStore.userInfo) {
    profileForm.username = userStore.userInfo.username || ''
    profileForm.nickname = userStore.userInfo.nickname || ''
    profileForm.phone = userStore.userInfo.phone || ''
    profileForm.email = userStore.userInfo.email || ''
    profileForm.avatar_url = userStore.userInfo.avatar_url || ''
    userInfo.value = userStore.userInfo
  }
}

const fetchConsultations = async () => {
  try {
    const token = localStorage.getItem('token')
    console.log('【调试】Token 存在:', !!token)

    if (!token) {
      ElMessage.warning('请先登录')
      return
    }

    // 使用 fetch 明确带上 Authorization 头
    const response = await fetch('/api/v1/consultations', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      const data = await response.json().catch(() => null)
      console.error('获取问诊记录失败', response.status, data)
      consultations.value = []
      return
    }

    const res = await response.json()
    consultations.value = res || []
  } catch (error) {
    console.error('获取问诊记录失败', error)
    consultations.value = []
  }
}

const handleMenuSelect = (index: string) => {
  activeMenu.value = index
  if (index === 'consultations') {
    fetchConsultations()
  }
}

const saveProfile = async () => {
  saving.value = true
  try {
    await request.put(`/users/${userStore.userInfo?.user_id}`, profileForm)
    ElMessage.success('保存成功')
    userStore.getUserInfo()
  } catch (error: any) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    saving.value = false
  }
}

const handleAvatarSuccess = (response: any) => {
  profileForm.avatar_url = response.url || response.avatar_url
  ElMessage.success('头像上传成功')
}

const changePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return

    changingPassword.value = true
    try {
      await request.post('/auth/change-password', null, {
        params: {
          old_password: passwordForm.oldPassword,
          new_password: passwordForm.newPassword
        }
      })
      ElMessage.success('密码修改成功')
      showChangePasswordDialog.value = false
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
    } catch (error: any) {
      ElMessage.error(error.message || '修改失败')
    } finally {
      changingPassword.value = false
    }
  })
}

const sendPhoneCode = async () => {
  if (!phoneForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }

  try {
    await request.post('/auth/send-code', {
      phone: phoneForm.phone,
      type: 'bind_phone'
    })
    ElMessage.success('验证码已发送')
    phoneCountdown.value = 60
    phoneTimer = setInterval(() => {
      phoneCountdown.value--
      if (phoneCountdown.value <= 0 && phoneTimer) {
        clearInterval(phoneTimer)
      }
    }, 1000)
  } catch (error: any) {
    ElMessage.error(error.message || '发送失败')
  }
}

const bindPhone = async () => {
  if (!phoneFormRef.value) return

  await phoneFormRef.value.validate(async (valid) => {
    if (!valid) return

    bindingPhone.value = true
    try {
      await request.post('/users/bind-phone', {
        phone: phoneForm.phone,
        code: phoneForm.code
      })
      ElMessage.success('手机号绑定成功')
      showBindPhoneDialog.value = false
      userStore.getUserInfo()
    } catch (error: any) {
      ElMessage.error(error.message || '绑定失败')
    } finally {
      bindingPhone.value = false
    }
  })
}

const sendEmailCode = async () => {
  if (!emailForm.email) {
    ElMessage.warning('请先输入邮箱')
    return
  }

  try {
    await request.post('/auth/send-code', {
      email: emailForm.email,
      type: 'bind_email'
    })
    ElMessage.success('验证码已发送')
    emailCountdown.value = 60
    emailTimer = setInterval(() => {
      emailCountdown.value--
      if (emailCountdown.value <= 0 && emailTimer) {
        clearInterval(emailTimer)
      }
    }, 1000)
  } catch (error: any) {
    ElMessage.error(error.message || '发送失败')
  }
}

const bindEmail = async () => {
  if (!emailFormRef.value) return

  await emailFormRef.value.validate(async (valid) => {
    if (!valid) return

    bindingEmail.value = true
    try {
      await request.post('/users/bind-email', {
        email: emailForm.email,
        code: emailForm.code
      })
      ElMessage.success('邮箱绑定成功')
      showBindEmailDialog.value = false
      userStore.getUserInfo()
    } catch (error: any) {
      ElMessage.error(error.message || '绑定失败')
    } finally {
      bindingEmail.value = false
    }
  })
}

const getStatusType = (status: number) => {
  const types: Record<number, string> = {
    0: 'info',
    1: 'primary',
    2: 'success',
    3: 'warning',
    4: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: number) => {
  const texts: Record<number, string> = {
    0: '待开始',
    1: '进行中',
    2: '已完成',
    3: '已取消',
    4: '已关闭'
  }
  return texts[status] || '未知'
}

const formatDate = (date: string) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

const viewConsultation = (id: number) => {
  router.push(`/consultation/${id}`)
}
</script>

<style scoped lang="scss">
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 20px;
}

.profile-sidebar {
  width: 240px;
  background: white;
  border-radius: 8px;
  overflow: hidden;

  .user-info-card {
    padding: 30px 20px;
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;

    h3 {
      margin: 16px 0 8px;
      font-size: 18px;
    }

    p {
      font-size: 14px;
      opacity: 0.8;
    }
  }

  :deep(.el-menu) {
    border: none;
  }
}

.profile-content {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 30px;
}

.content-section {
  .section-title {
    font-size: 20px;
    font-weight: 500;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #eee;
  }
}

.profile-form {
  max-width: 500px;

  .avatar-upload {
    margin-left: 20px;
    display: inline-block;
  }
}

.security-items {
  .security-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid #eee;

    &:last-child {
      border-bottom: none;
    }

    .security-item-left {
      display: flex;
      align-items: center;
      gap: 16px;

      .el-icon {
        color: #409eff;
      }

      .security-item-info {
        h4 {
          font-size: 16px;
          margin-bottom: 4px;
        }

        p {
          font-size: 14px;
          color: #666;
        }
      }
    }
  }
}

.consultations-list {
  .consultation-card {
    margin-bottom: 16px;

    .consultation-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;

      .consultation-id {
        font-size: 14px;
        color: #666;
      }
    }

    .consultation-content {
      margin-bottom: 12px;

      p {
        margin-bottom: 8px;
        font-size: 14px;
        color: #666;
      }
    }

    .consultation-actions {
      text-align: right;
    }
  }
}

.code-input {
  display: flex;
  gap: 10px;

  :deep(.el-input) {
    flex: 1;
  }
}
</style>

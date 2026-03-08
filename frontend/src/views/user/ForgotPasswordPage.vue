<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
      <div class="forgot-password-header">
        <el-icon :size="64" color="#409eff"><FirstAidKit /></el-icon>
        <h1>找回密码</h1>
        <p>请通过手机号或邮箱找回密码</p>
      </div>

      <el-steps :active="currentStep" finish-status="success" align-center class="steps">
        <el-step title="验证身份" />
        <el-step title="重置密码" />
        <el-step title="完成" />
      </el-steps>

      <el-form ref="formRef" :model="form" :rules="rules" class="forgot-password-form">
        <!-- 步骤1: 验证身份 -->
        <template v-if="currentStep === 0">
          <el-form-item prop="accountType">
            <el-radio-group v-model="form.accountType">
              <el-radio label="phone">手机号找回</el-radio>
              <el-radio label="email">邮箱找回</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item prop="account">
            <el-input
              v-model="form.account"
              :placeholder="form.accountType === 'phone' ? '请输入手机号' : '请输入邮箱'"
              prefix-icon="User"
              size="large"
            />
          </el-form-item>

          <el-form-item prop="code">
            <div class="code-input">
              <el-input
                v-model="form.code"
                placeholder="请输入验证码"
                prefix-icon="Lock"
                size="large"
              />
              <el-button
                size="large"
                :disabled="countdown > 0"
                @click="sendCode"
              >
                {{ countdown > 0 ? `${countdown}秒后重发` : '获取验证码' }}
              </el-button>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="submit-button"
              @click="verifyCode"
            >
              验证
            </el-button>
          </el-form-item>
        </template>

        <!-- 步骤2: 重置密码 -->
        <template v-if="currentStep === 1">
          <el-form-item prop="newPassword">
            <el-input
              v-model="form.newPassword"
              type="password"
              placeholder="请输入新密码"
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请再次输入新密码"
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="submit-button"
              @click="resetPassword"
            >
              确认重置
            </el-button>
          </el-form-item>
        </template>

        <!-- 步骤3: 完成 -->
        <template v-if="currentStep === 2">
          <div class="success-tip">
            <el-icon :size="64" color="#67c23a"><CircleCheck /></el-icon>
            <h2>密码重置成功</h2>
            <p>您的密码已成功重置，请使用新密码登录</p>
            <el-button type="primary" size="large" @click="$router.push('/login')">
              立即登录
            </el-button>
          </div>
        </template>
      </el-form>

      <div class="forgot-password-footer" v-if="currentStep < 2">
        <span>想起密码了?</span>
        <el-link type="primary" underline="never" @click="$router.push('/login')">
          立即登录
        </el-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, FormInstance } from 'element-plus'
import { FirstAidKit, CircleCheck } from '@element-plus/icons-vue'
import request from '@/api/request'

const router = useRouter()

const formRef = ref<FormInstance>()
const loading = ref(false)
const currentStep = ref(0)
const countdown = ref(0)
let countdownTimer: ReturnType<typeof setInterval> | null = null

const form = reactive({
  accountType: 'phone',
  account: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (value !== form.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  account: [
    { required: true, message: '请输入手机号或邮箱', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码长度为6位', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const sendCode = async () => {
  if (!form.account) {
    ElMessage.warning('请先输入手机号或邮箱')
    return
  }

  loading.value = true
  try {
    await request.post('/auth/send-code', {
      phone: form.accountType === 'phone' ? form.account : null,
      email: form.accountType === 'email' ? form.account : null,
      type: 'reset_password'
    })
    ElMessage.success('验证码已发送')
    countdown.value = 60
    countdownTimer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0 && countdownTimer) {
        clearInterval(countdownTimer)
        countdownTimer = null
      }
    }, 1000)
  } catch (error: any) {
    ElMessage.error(error.message || '发送失败')
  } finally {
    loading.value = false
  }
}

const verifyCode = async () => {
  if (!formRef.value) return

  await formRef.value.validateField(['account', 'code'], async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await request.post('/auth/verify-code', {
        phone: form.accountType === 'phone' ? form.account : null,
        email: form.accountType === 'email' ? form.account : null,
        code: form.code
      })
      ElMessage.success('验证成功')
      currentStep.value = 1
    } catch (error: any) {
      ElMessage.error(error.message || '验证失败')
    } finally {
      loading.value = false
    }
  })
}

const resetPassword = async () => {
  if (!formRef.value) return

  await formRef.value.validateField(['newPassword', 'confirmPassword'], async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await request.post('/auth/reset-password', {
        phone: form.accountType === 'phone' ? form.account : null,
        email: form.accountType === 'email' ? form.account : null,
        code: form.code,
        new_password: form.newPassword
      })
      ElMessage.success('密码重置成功')
      currentStep.value = 2
    } catch (error: any) {
      ElMessage.error(error.message || '重置失败')
    } finally {
      loading.value = false
    }
  })
}

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped lang="scss">
.forgot-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.forgot-password-container {
  width: 480px;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 30px;

  h1 {
    font-size: 24px;
    color: #333;
    margin: 16px 0 8px;
  }

  p {
    color: #666;
    font-size: 14px;
  }
}

.steps {
  margin-bottom: 30px;
}

.forgot-password-form {
  .code-input {
    display: flex;
    gap: 10px;

    :deep(.el-input) {
      flex: 1;
    }
  }

  .submit-button {
    width: 100%;
  }
}

.success-tip {
  text-align: center;
  padding: 20px 0;

  h2 {
    font-size: 20px;
    color: #333;
    margin: 16px 0 8px;
  }

  p {
    color: #666;
    font-size: 14px;
    margin-bottom: 24px;
  }
}

.forgot-password-footer {
  text-align: center;
  margin-top: 20px;
  color: #666;

  span {
    margin-right: 8px;
  }
}
</style>

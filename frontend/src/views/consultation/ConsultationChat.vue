<template>
  <div class="consultation-chat-page">
    <div class="page-header">
      <el-button @click="goBack">返回</el-button>
      <h2>{{ consultation?.title || '问诊对话' }}</h2>
      <el-tag v-if="consultation" :type="getStatusType(consultation.status)">
        {{ getStatusText(consultation.status) }}
      </el-tag>
    </div>
    
    <div class="chat-container">
      <!-- 加载状态 -->
      <div v-if="loading && !consultation" class="loading-container">
        <el-skeleton :rows="10" animated />
        <div class="loading-text">正在加载问诊信息...</div>
      </div>
      
      <!-- 对话消息区域 -->
      <div class="messages-container" ref="messagesContainer" v-else>
        <!-- 欢迎消息 -->
        <div v-if="!messages || messages.length === 0" class="welcome-message">
          <div class="welcome-icon">🤖</div>
          <div class="welcome-text">
            <p>您好！我是医疗智能助手小医。</p>
            <p>请详细描述您的症状，我会为您提供初步的诊断建议。</p>
            <p>请注意：我的建议仅供参考，不能替代专业医生的诊断。</p>
          </div>
        </div>
        
        <!-- 消息列表 -->
        <div v-for="msg in messages" :key="msg.message_id" 
             class="message-item" 
             :class="msg.sender_type">
          <div class="message-avatar">
            <span v-if="msg.sender_type === 'user'">👤</span>
            <span v-else>🤖</span>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              {{ msg.content }}
            </div>
            <div class="message-time">
              {{ formatTime(msg.created_at) }}
            </div>
          </div>
        </div>
        
        <!-- AI正在输入提示 -->
        <div v-if="loading" class="message-item ai">
          <div class="message-avatar">🤖</div>
          <div class="message-content">
            <div class="message-bubble loading">
              <span class="loading-dots">
                <span></span><span></span><span></span>
              </span>
              AI正在思考中...
            </div>
          </div>
        </div>
        
        <!-- 紧急警告 -->
        <div v-if="isEmergency" class="emergency-warning">
          <el-alert type="warning" :closable="false" show-icon>
            <template #title>
              <span>⚠️ 检测到紧急症状</span>
            </template>
            <template #default>
              <p>根据您的描述，症状可能比较严重，建议您立即前往医院就诊！</p>
              <p>如有需要，请拨打急救电话：120</p>
            </template>
          </el-alert>
        </div>
        
        <!-- 追问建议 -->
        <div v-if="followUpQuestions && followUpQuestions.length > 0 && !loading" class="follow-up-questions">
          <p>您可以这样回复：</p>
          <div class="question-buttons">
            <el-button 
              v-for="(q, index) in followUpQuestions" 
              :key="index" 
              size="small" 
              type="primary" 
              plain
              @click="handleQuickReply(q)">
              {{ q }}
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="input-container" v-if="consultation && consultation.status === 0">
        <div class="input-wrapper">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="请描述您的症状..."
            :disabled="loading"
            @keydown.enter.ctrl="handleSendMessage"
            resize="none"
          />
          <el-button 
            type="primary" 
            :loading="loading" 
            :disabled="!inputMessage.trim()"
            @click="handleSendMessage"
            class="send-button">
            发送
          </el-button>
        </div>
        <div class="input-hint">
          <span>按 Ctrl + Enter 发送</span>
          <span v-if="consultation.status !== 0" class="status-hint">
            问诊已{{ getStatusText(consultation.status) }}
          </span>
        </div>
      </div>
      
      <!-- 问诊已结束 -->
      <div class="ended-actions" v-else-if="consultation && consultation.status !== 0">
        <el-button type="primary" @click="handleViewDetail">查看问诊详情</el-button>
        <el-button type="success" @click="handleGenerateReport" :loading="generating">生成报告</el-button>
        <el-button @click="handleNewConsultation">发起新问诊</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { consultationApi, type Consultation, type Message } from '@/api/consultation'

const router = useRouter()
const route = useRoute()

// 数据
const loading = ref(false)
const generating = ref(false)
const inputMessage = ref('')
const consultation = ref<Consultation | null>(null)
const messages = ref<Message[]>([])
const isEmergency = ref(false)
const followUpQuestions = ref<string[]>([])
const messagesContainer = ref<HTMLElement | null>(null)

// 状态映射
const getStatusType = (status: number): string => {
  const types: Record<number, string> = {
    0: 'info',
    1: 'success',
    2: 'info',
    3: 'warning'
  }
  return types[status] || 'info'
}

const getStatusText = (status: number): string => {
  const texts: Record<number, string> = {
    0: '进行中',
    1: '已完成',
    2: '已取消',
    3: '待审核'
  }
  return texts[status] || '未知'
}

// 格式化时间
const formatTime = (dateStr: string): string => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载问诊详情
const loadConsultation = async () => {
  const id = Number(route.params.id)
  if (isNaN(id)) {
    ElMessage.error('无效的问诊ID')
    router.push('/consultation')
    return
  }
  loading.value = true
  try {
    const res = await consultationApi.getDetail(id)
    // request.ts 响应拦截器已返回 response.data，res 就是数据本身
    consultation.value = res
    // 加载消息列表
    await loadMessages(id)
  } catch (error: any) {
    console.error('加载问诊详情失败:', error)
    // 根据错误类型给出友好提示
    if (error?.response?.status === 404) {
      ElMessage.error('问诊记录不存在')
    } else if (error?.response?.status === 403) {
      ElMessage.error('您无权查看此问诊记录')
    } else if (error?.code === 'ERR_NETWORK' || error?.message?.includes('Network Error')) {
      ElMessage.error('网络错误，请检查后端服务是否启动')
    } else {
      ElMessage.error('加载问诊详情失败，请稍后重试')
    }
    // 延迟跳转，让用户看到错误提示
    setTimeout(() => {
      router.push('/consultation')
    }, 1500)
  } finally {
    loading.value = false
  }
}

// 加载消息列表
const loadMessages = async (consultationId: number) => {
  try {
    const res = await consultationApi.getMessages(consultationId)
    // 确保 messages 是数组
    messages.value = Array.isArray(res) ? res : []
    scrollToBottom()
  } catch (error) {
    console.error('加载消息列表失败:', error)
    // 消息加载失败不影响主流程
    messages.value = []
  }
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 发送消息
const handleSendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value || !consultation.value) return
  
  const message = inputMessage.value.trim()
  inputMessage.value = ''
  loading.value = true
  
  try {
    const res = await consultationApi.sendMessage(consultation.value.consultation_id, {
      message
    })
    
    // request.ts 响应拦截器已返回 response.data，res 就是数据本身
    // res 的类型是 SendMessageResponse
    
    // 更新消息列表，确保是数组
    messages.value = Array.isArray(res.messages) ? res.messages : []
    
    // 更新紧急状态
    isEmergency.value = res.is_emergency
    
    // 更新追问问题
    followUpQuestions.value = res.follow_up_questions || []
    
    // 重新加载问诊详情（更新状态）
    const detailRes = await consultationApi.getDetail(consultation.value.consultation_id)
    consultation.value = detailRes
    
    // 滚动到底部
    scrollToBottom()
  } catch (error: any) {
    console.error('发送消息失败:', error)
    if (error?.response?.status === 403) {
      ElMessage.error('您无权操作此问诊')
    } else if (error?.response?.status === 400) {
      ElMessage.error(error?.response?.data?.detail || '问诊会话已结束')
    } else {
      ElMessage.error('发送消息失败，请重试')
    }
    inputMessage.value = message // 恢复输入
  } finally {
    loading.value = false
  }
}

// 快速回复
const handleQuickReply = (question: string) => {
  inputMessage.value = question
  handleSendMessage()
}

// 返回
const goBack = () => {
  router.push('/consultation')
}

// 查看详情
const handleViewDetail = () => {
  if (consultation.value) {
    router.push(`/consultation/${consultation.value.consultation_id}`)
  }
}

// 生成报告
const handleGenerateReport = async () => {
  if (!consultation.value) return
  
  generating.value = true
  try {
    await consultationApi.generateReport(consultation.value.consultation_id, {
      report_type: 'text'
    })
    ElMessage.success('报告生成成功')
    handleViewDetail()
  } catch (error) {
    console.error('生成报告失败:', error)
    ElMessage.error('生成报告失败')
  } finally {
    generating.value = false
  }
}

// 发起新问诊
const handleNewConsultation = () => {
  router.push('/consultation')
}

// 监听消息变化，自动滚动
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

// 页面加载
onMounted(() => {
  loadConsultation()
})
</script>

<style scoped lang="scss">
.consultation-chat-page {
  padding: 20px;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  
  .page-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
    flex-shrink: 0;
    
    h2 {
      margin: 0;
      flex: 1;
    }
  }
  
  .chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
  
  .loading-container {
    flex: 1;
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    
    .loading-text {
      color: #909399;
      font-size: 14px;
    }
  }
  
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    background-color: #f5f7fa;
    
    .welcome-message {
      display: flex;
      gap: 15px;
      padding: 20px;
      background-color: #fff;
      border-radius: 8px;
      margin-bottom: 20px;
      
      .welcome-icon {
        font-size: 40px;
      }
      
      .welcome-text {
        p {
          margin: 5px 0;
          line-height: 1.6;
        }
      }
    }
    
    .message-item {
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
      
      .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
      }
      
      .message-content {
        max-width: 70%;
        
        .message-bubble {
          padding: 12px 16px;
          border-radius: 8px;
          line-height: 1.6;
          white-space: pre-wrap;
          word-break: break-word;
          
          &.loading {
            color: #999;
            font-style: italic;
          }
        }
        
        .message-time {
          font-size: 12px;
          color: #999;
          margin-top: 5px;
        }
      }
      
      &.user {
        flex-direction: row-reverse;
        
        .message-avatar {
          background-color: #409eff;
        }
        
        .message-content {
          align-items: flex-end;
          
          .message-bubble {
            background-color: #409eff;
            color: #fff;
          }
        }
      }
      
      &.ai {
        .message-avatar {
          background-color: #67c23a;
        }
        
        .message-content {
          .message-bubble {
            background-color: #fff;
            border: 1px solid #e4e7ed;
          }
        }
      }
    }
    
    .emergency-warning {
      margin: 20px 0;
    }
    
    .follow-up-questions {
      margin-top: 20px;
      padding: 15px;
      background-color: #fff;
      border-radius: 8px;
      
      p {
        margin: 0 0 10px 0;
        color: #666;
      }
      
      .question-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }
    }
  }
  
  .loading-dots {
    display: inline-flex;
    margin-right: 8px;
    
    span {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: #999;
      margin: 0 2px;
      animation: loading 1.4s infinite ease-in-out both;
      
      &:nth-child(1) {
        animation-delay: -0.32s;
      }
      &:nth-child(2) {
        animation-delay: -0.16s;
      }
    }
  }
  
  @keyframes loading {
    0%, 80%, 100% {
      transform: scale(0);
    }
    40% {
      transform: scale(1);
    }
  }
  
  .input-container {
    padding: 20px;
    background-color: #fff;
    border-top: 1px solid #e4e7ed;
    
    .input-wrapper {
      display: flex;
      gap: 10px;
      
      .el-textarea {
        flex: 1;
      }
      
      .send-button {
        height: auto;
      }
    }
    
    .input-hint {
      display: flex;
      justify-content: space-between;
      margin-top: 10px;
      font-size: 12px;
      color: #999;
      
      .status-hint {
        color: #e6a23c;
      }
    }
  }
  
  .ended-actions {
    padding: 20px;
    background-color: #fff;
    border-top: 1px solid #e4e7ed;
    display: flex;
    justify-content: center;
    gap: 15px;
  }
}
</style>

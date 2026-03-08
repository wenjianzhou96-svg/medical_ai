<template>
  <div class="consultation-detail-page">
    <div class="page-header">
      <el-button @click="goBack">返回</el-button>
      <h2>问诊详情</h2>
      <el-button type="primary" @click="handleChat" v-if="consultation && consultation.status === 0">
        继续对话
      </el-button>
    </div>
    
    <div v-loading="loading">
      <el-card v-if="consultation">
        <!-- 基本信息 -->
        <el-descriptions :column="2" border>
          <el-descriptions-item label="问诊ID">{{ consultation.consultation_id }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(consultation.status)">{{ getStatusText(consultation.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="标题" :span="2">{{ consultation.title || '无标题' }}</el-descriptions-item>
          <el-descriptions-item label="症状描述" :span="2">
            <div class="symptoms-content">{{ consultation.symptoms || '暂无' }}</div>
          </el-descriptions-item>
          <el-descriptions-item label="严重程度">
            <el-tag v-if="consultation.severity_level !== null && consultation.severity_level !== undefined" 
                    :type="getSeverityType(consultation.severity_level)">
              {{ getSeverityText(consultation.severity_level) }}
            </el-tag>
            <span v-else>未评估</span>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(consultation.created_at) }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- AI诊断建议 -->
        <div class="section" v-if="consultation.ai_suggestion">
          <h3>AI诊断建议</h3>
          <el-card class="suggestion-card">
            <div class="ai-suggestion">{{ consultation.ai_suggestion }}</div>
          </el-card>
        </div>
        
        <!-- 医生审核意见 -->
        <div class="section" v-if="consultation.doctor_review">
          <h3>医生审核意见</h3>
          <el-card class="review-card">
            <div class="doctor-review">{{ consultation.doctor_review }}</div>
          </el-card>
        </div>
        
        <!-- 操作按钮 -->
        <div class="actions" v-if="consultation.status === 0">
          <el-button type="success" @click="handleFinish" :loading="finishing">完成问诊</el-button>
          <el-button type="warning" @click="handleGenerateReport" :loading="generating">生成报告</el-button>
          <el-button type="danger" @click="handleCancel" :loading="cancelling">取消问诊</el-button>
        </div>
        
        <!-- 报告列表 -->
        <div class="section" v-if="reports.length > 0">
          <h3>问诊报告</h3>
          <el-table :data="reports" stripe>
            <el-table-column prop="report_id" label="报告ID" width="80" />
            <el-table-column prop="report_type" label="报告类型" width="100" />
            <el-table-column prop="created_at" label="生成时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button link type="primary" @click="handleViewReport(row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
      
      <el-empty v-else-if="!loading" description="问诊记录不存在" />
    </div>
    
    <!-- 报告查看对话框 -->
    <el-dialog v-model="reportDialogVisible" title="问诊报告" width="600px">
      <div v-if="currentReport" class="report-content">
        <pre>{{ JSON.stringify(currentReport.report_content, null, 2) }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { consultationApi, type Consultation, type Report } from '@/api/consultation'

const router = useRouter()
const route = useRoute()

// 数据
const loading = ref(false)
const finishing = ref(false)
const generating = ref(false)
const cancelling = ref(false)
const consultation = ref<Consultation | null>(null)
const reports = ref<Report[]>([])
const reportDialogVisible = ref(false)
const currentReport = ref<Report | null>(null)

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

// 严重程度映射
const getSeverityType = (level: number): string => {
  const types: Record<number, string> = {
    0: 'success',
    1: 'warning',
    2: 'danger',
    3: 'danger'
  }
  return types[level] || 'info'
}

const getSeverityText = (level: number): string => {
  const texts: Record<number, string> = {
    0: '低危',
    1: '中危',
    2: '高危',
    3: '紧急'
  }
  return texts[level] || '未知'
}

// 格式化日期时间
const formatDateTime = (dateStr: string): string => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载问诊详情
const loadConsultationDetail = async () => {
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
    // 加载报告列表
    loadReports(id)
  } catch (error: any) {
    console.error('加载问诊详情失败:', error)
    if (error?.response?.status === 404) {
      ElMessage.error('问诊记录不存在')
    } else if (error?.response?.status === 403) {
      ElMessage.error('您无权查看此问诊记录')
    } else if (error?.code === 'ERR_NETWORK' || error?.message?.includes('Network Error')) {
      ElMessage.error('网络错误，请检查后端服务是否启动')
    } else {
      ElMessage.error('加载问诊详情失败，请稍后重试')
    }
    // 延迟跳转
    setTimeout(() => {
      router.push('/consultation')
    }, 1500)
  } finally {
    loading.value = false
  }
}

// 加载报告列表
const loadReports = async (consultationId: number) => {
  try {
    const res = await consultationApi.getReports(consultationId)
    // res 就是数组本身
    reports.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('加载报告列表失败:', error)
  }
}

// 返回
const goBack = () => {
  router.back()
}

// 继续对话
const handleChat = () => {
  if (consultation.value) {
    router.push(`/consultation/chat/${consultation.value.consultation_id}`)
  }
}

// 完成问诊
const handleFinish = async () => {
  if (!consultation.value) return
  
  try {
    await ElMessageBox.confirm('完成问诊后将生成诊断建议，是否继续？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })
    
    finishing.value = true
    const res = await consultationApi.finish(consultation.value.consultation_id)
    // request.ts 响应拦截器已返回 response.data
    consultation.value = res
    ElMessage.success('问诊已完成，诊断建议已生成')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('完成问诊失败:', error)
      ElMessage.error('完成问诊失败')
    }
  } finally {
    finishing.value = false
  }
}

// 生成报告
const handleGenerateReport = async () => {
  if (!consultation.value) return
  
  generating.value = true
  try {
    const res = await consultationApi.generateReport(consultation.value.consultation_id, {
      report_type: 'text'
    })
    // request.ts 响应拦截器已返回 response.data
    reports.value.unshift(res)
    ElMessage.success('报告生成成功')
  } catch (error) {
    console.error('生成报告失败:', error)
    ElMessage.error('生成报告失败')
  } finally {
    generating.value = false
  }
}

// 取消问诊
const handleCancel = async () => {
  if (!consultation.value) return
  
  try {
    await ElMessageBox.confirm('确定要取消此问诊吗？取消后无法恢复。', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    cancelling.value = true
    const res = await consultationApi.cancel(consultation.value.consultation_id)
    // request.ts 响应拦截器已返回 response.data
    consultation.value = res
    ElMessage.success('问诊已取消')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消问诊失败:', error)
      ElMessage.error('取消问诊失败')
    }
  } finally {
    cancelling.value = false
  }
}

// 查看报告
const handleViewReport = (report: Report) => {
  currentReport.value = report
  reportDialogVisible.value = true
}

// 页面加载
onMounted(() => {
  loadConsultationDetail()
})
</script>

<style scoped lang="scss">
.consultation-detail-page {
  padding: 20px;
  
  .page-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
      flex: 1;
    }
  }
  
  .symptoms-content {
    white-space: pre-wrap;
    word-break: break-word;
  }
  
  .section {
    margin-top: 20px;
    
    h3 {
      margin-bottom: 10px;
      font-size: 16px;
      font-weight: 500;
    }
  }
  
  .ai-suggestion, .doctor-review {
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.8;
  }
  
  .actions {
    margin-top: 20px;
    display: flex;
    gap: 10px;
  }
  
  .report-content {
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      background-color: #f5f7fa;
      padding: 15px;
      border-radius: 4px;
    }
  }
}
</style>

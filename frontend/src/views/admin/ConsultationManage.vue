<template>
  <div class="consultation-manage-page">
    <div class="page-header">
      <h2>问诊管理</h2>
    </div>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="statistics-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ statistics.total }}</div>
            <div class="stat-label">总问诊量</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ statistics.pending_review }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ statistics.emergency_count }}</div>
            <div class="stat-label">紧急问诊</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ statistics.completed }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable @change="handleFilterChange">
            <el-option label="全部" :value="undefined" />
            <el-option label="进行中" :value="0" />
            <el-option label="已完成" :value="1" />
            <el-option label="已取消" :value="2" />
            <el-option label="待审核" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="严重程度">
          <el-select v-model="filterForm.severity_level" placeholder="请选择严重程度" clearable @change="handleFilterChange">
            <el-option label="全部" :value="undefined" />
            <el-option label="低危" :value="0" />
            <el-option label="中危" :value="1" />
            <el-option label="高危" :value="2" />
            <el-option label="紧急" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 问诊列表 -->
    <el-table :data="consultations" v-loading="loading" stripe style="width: 100%">
      <el-table-column prop="consultation_id" label="问诊ID" width="80" />
      <el-table-column prop="user_id" label="用户ID" width="80" />
      <el-table-column prop="title" label="标题" min-width="150">
        <template #default="{ row }">
          <span v-if="row.title">{{ row.title }}</span>
          <span v-else class="no-title">无标题</span>
        </template>
      </el-table-column>
      <el-table-column prop="symptoms" label="症状描述" min-width="200" show-overflow-tooltip>
        <template #default="{ row }">
          <span v-if="row.symptoms">{{ row.symptoms }}</span>
          <span v-else class="no-content">暂无</span>
        </template>
      </el-table-column>
      <el-table-column prop="severity_level" label="严重程度" width="100">
        <template #default="{ row }">
          <el-tag v-if="row.severity_level !== null && row.severity_level !== undefined" 
                  :type="getSeverityType(row.severity_level)" size="small">
            {{ getSeverityText(row.severity_level) }}
          </el-tag>
          <span v-else class="no-content">未评估</span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" size="small">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleView(row)">查看</el-button>
          <el-button link type="success" size="small" @click="handleReview(row)" v-if="row.status === 3">审核</el-button>
          <el-button link type="warning" size="small" @click="handleReview(row)" v-else-if="row.status === 1">补充建议</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
    
    <!-- 审核对话框 -->
    <el-dialog v-model="reviewDialogVisible" title="医生审核" width="700px">
      <div v-if="currentConsultation">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="问诊ID">{{ currentConsultation.consultation_id }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentConsultation.status)">
              {{ getStatusText(currentConsultation.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="症状描述" :span="2">
            {{ currentConsultation.symptoms || '暂无' }}
          </el-descriptions-item>
        </el-descriptions>
        
        <!-- AI建议 -->
        <div class="section" v-if="currentConsultation.ai_suggestion">
          <h4>AI诊断建议</h4>
          <div class="ai-suggestion">{{ currentConsultation.ai_suggestion }}</div>
        </div>
        
        <!-- 审核表单 -->
        <el-form :model="reviewForm" ref="reviewFormRef" label-width="100px" class="review-form">
          <el-form-item label="审核意见" prop="review_content">
            <el-input
              v-model="reviewForm.review_content"
              type="textarea"
              :rows="6"
              placeholder="请输入审核意见，对AI诊断建议进行确认、修改或补充"
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitReview" :loading="submitting">提交审核</el-button>
      </template>
    </el-dialog>
    
    <!-- 查看详情对话框 -->
    <el-dialog v-model="viewDialogVisible" title="问诊详情" width="800px">
      <div v-if="currentConsultation">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="问诊ID">{{ currentConsultation.consultation_id }}</el-descriptions-item>
          <el-descriptions-item label="用户ID">{{ currentConsultation.user_id }}</el-descriptions-item>
          <el-descriptions-item label="标题" :span="2">{{ currentConsultation.title || '无标题' }}</el-descriptions-item>
          <el-descriptions-item label="症状描述" :span="2">
            <div class="content-text">{{ currentConsultation.symptoms || '暂无' }}</div>
          </el-descriptions-item>
          <el-descriptions-item label="严重程度">
            <el-tag v-if="currentConsultation.severity_level !== null" 
                    :type="getSeverityType(currentConsultation.severity_level)">
              {{ getSeverityText(currentConsultation.severity_level) }}
            </el-tag>
            <span v-else>未评估</span>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentConsultation.status)">
              {{ getStatusText(currentConsultation.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(currentConsultation.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDateTime(currentConsultation.updated_at) }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="section" v-if="currentConsultation.ai_suggestion">
          <h4>AI诊断建议</h4>
          <div class="content-text ai-suggestion">{{ currentConsultation.ai_suggestion }}</div>
        </div>
        
        <div class="section" v-if="currentConsultation.doctor_review">
          <h4>医生审核意见</h4>
          <div class="content-text doctor-review">{{ currentConsultation.doctor_review }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { consultationApi, type Consultation, type StatisticsResponse } from '@/api/consultation'

// 数据
const loading = ref(false)
const submitting = ref(false)
const consultations = ref<Consultation[]>([])
const currentConsultation = ref<Consultation | null>(null)
const reviewDialogVisible = ref(false)
const viewDialogVisible = ref(false)
const reviewFormRef = ref()

// 统计数据
const statistics = reactive<StatisticsResponse>({
  total: 0,
  completed: 0,
  in_progress: 0,
  pending_review: 0,
  cancelled: 0,
  emergency_count: 0,
  average_severity: 0
})

// 筛选表单
const filterForm = reactive({
  status: undefined as number | undefined,
  severity_level: undefined as number | undefined
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 审核表单
const reviewForm = reactive({
  review_content: ''
})

// 状态映射
const getStatusType = (status: number): string => {
  const types: Record<number, string> = {
    0: 'info',     // 进行中
    1: 'success', // 已完成
    2: 'info',    // 已取消
    3: 'warning'  // 待审核
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
    0: 'success', // 低危
    1: 'warning', // 中危
    2: 'danger',   // 高危
    3: 'danger'   // 紧急
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

// 加载统计数据
const loadStatistics = async () => {
  try {
    const res = await consultationApi.getStatistics()
    const data = res.data
    Object.assign(statistics, data)
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载问诊列表
const loadConsultations = async () => {
  loading.value = true
  try {
    const res = await consultationApi.getAdminList({
      page: pagination.page,
      page_size: pagination.pageSize,
      status: filterForm.status,
      severity_level: filterForm.severity_level
    })
    consultations.value = data.items
    pagination.total = data.total
  } catch (error) {
    console.error('加载问诊列表失败:', error)
    ElMessage.error('加载问诊列表失败')
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = () => {
  pagination.page = 1
  loadConsultations()
}

// 分页变化
const handlePageChange = (page: number) => {
  pagination.page = page
  loadConsultations()
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  loadConsultations()
}

// 查看详情
const handleView = async (row: Consultation) => {
  try {
    const res = await consultationApi.getAdminDetail(row.consultation_id)
    currentConsultation.value = res.data
    viewDialogVisible.value = true
  } catch (error) {
    console.error('加载问诊详情失败:', error)
    ElMessage.error('加载问诊详情失败')
  }
}

// 审核
const handleReview = async (row: Consultation) => {
  try {
    const res = await consultationApi.getAdminDetail(row.consultation_id)
    currentConsultation.value = res.data
    reviewForm.review_content = currentConsultation.value.doctor_review || ''
    reviewDialogVisible.value = true
  } catch (error) {
    console.error('加载问诊详情失败:', error)
    ElMessage.error('加载问诊详情失败')
  }
}

// 提交审核
const handleSubmitReview = async () => {
  if (!currentConsultation.value || !reviewForm.review_content.trim()) {
    ElMessage.warning('请输入审核意见')
    return
  }
  
  submitting.value = true
  try {
    await consultationApi.doctorReview(currentConsultation.value.consultation_id, {
      review_content: reviewForm.review_content
    })
    ElMessage.success('审核提交成功')
    reviewDialogVisible.value = false
    // 刷新列表
    loadConsultations()
    loadStatistics()
  } catch (error) {
    console.error('提交审核失败:', error)
    ElMessage.error('提交审核失败')
  } finally {
    submitting.value = false
  }
}

// 页面加载
onMounted(() => {
  loadStatistics()
  loadConsultations()
})
</script>

<style scoped lang="scss">
.consultation-manage-page {
  padding: 20px;
  
  .page-header {
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
    }
  }
  
  .statistics-row {
    margin-bottom: 20px;
    
    .stat-card {
      text-align: center;
      
      .stat-value {
        font-size: 32px;
        font-weight: bold;
        color: #409eff;
      }
      
      .stat-label {
        font-size: 14px;
        color: #666;
        margin-top: 10px;
      }
    }
  }
  
  .filter-card {
    margin-bottom: 20px;
  }
  
  .no-title, .no-content {
    color: #999;
    font-style: italic;
  }
  
  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  
  .section {
    margin-top: 20px;
    
    h4 {
      margin-bottom: 10px;
      font-size: 14px;
      font-weight: 500;
    }
  }
  
  .content-text {
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.8;
  }
  
  .ai-suggestion {
    background-color: #f0f9ff;
    padding: 15px;
    border-radius: 4px;
    border-left: 4px solid #409eff;
  }
  
  .doctor-review {
    background-color: #f0fdf4;
    padding: 15px;
    border-radius: 4px;
    border-left: 4px solid #67c23a;
  }
  
  .review-form {
    margin-top: 20px;
  }
}
</style>

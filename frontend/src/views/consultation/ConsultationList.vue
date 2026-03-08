<template>
  <div class="consultation-list-page">
    <div class="page-header">
      <h2>我的问诊</h2>
      <el-button type="primary" @click="handleCreateConsultation">发起问诊</el-button>
    </div>
    
    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable @change="handleFilterChange">
            <el-option label="进行中" :value="0" />
            <el-option label="已完成" :value="1" />
            <el-option label="已取消" :value="2" />
            <el-option label="待审核" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 问诊列表 -->
    <el-table :data="consultations" v-loading="loading" stripe style="width: 100%">
      <el-table-column label="序号" width="80">
        <template #default="{ $index }">
          {{ (pagination.page - 1) * pagination.pageSize + $index + 1 }}
        </template>
      </el-table-column>
      <el-table-column prop="title" label="标题" min-width="150">
        <template #default="{ row }">
          <span v-if="row.title">{{ row.title }}</span>
          <span v-else class="no-title">无标题</span>
        </template>
      </el-table-column>
      <el-table-column prop="symptoms" label="症状描述" min-width="200">
        <template #default="{ row }">
          <el-tooltip :content="row.symptoms" placement="top" v-if="row.symptoms">
            <span class="symptoms-text">{{ row.symptoms }}</span>
          </el-tooltip>
          <span v-else class="no-content">暂无</span>
        </template>
      </el-table-column>
      <el-table-column prop="severity_level" label="严重程度" width="100">
        <template #default="{ row }">
          <el-tag v-if="row.severity_level !== null && row.severity_level !== undefined" 
                  :type="getSeverityType(row.severity_level)">
            {{ getSeverityText(row.severity_level) }}
          </el-tag>
          <span v-else class="no-content">未评估</span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleViewDetail(row.consultation_id)">查看</el-button>
          <el-button link type="primary" @click="handleChat(row.consultation_id)" v-if="row.status === 0">继续对话</el-button>
          <el-button link type="success" @click="handleViewReport(row.consultation_id)" v-if="row.status === 1">查看报告</el-button>
          <el-button link type="danger" @click="handleDelete(row.consultation_id)" v-if="row.status !== 0">删除</el-button>
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
    
    <!-- 发起问诊对话框 -->
    <el-dialog 
      v-model="createDialogVisible" 
      title="发起问诊" 
      width="600px"
      :close-on-click-modal="false"
      class="create-consultation-dialog"
    >
      <div class="dialog-tip">
        <el-icon><InfoFilled /></el-icon>
        <span>请详细描述您的症状，以便AI医生更好地为您诊断</span>
      </div>
      
      <el-form :model="createForm" :rules="createRules" ref="createFormRef" label-width="100px" class="create-form">
        <el-form-item label="问诊标题" prop="title">
          <el-input 
            v-model="createForm.title" 
            placeholder="例如：持续咳嗽2周，伴有低热（可选）" 
            maxlength="50" 
            show-word-limit
            clearable
          />
        </el-form-item>
        
        <el-form-item label="就诊科室" prop="department">
          <el-select 
            v-model="createForm.department" 
            placeholder="请选择就诊科室（可选）" 
            clearable 
            filterable
            style="width: 100%"
          >
            <el-option label="呼吸内科" value="respiratory" />
            <el-option label="消化内科" value="digestive" />
            <el-option label="心血管内科" value="cardiovascular" />
            <el-option label="神经内科" value="neurology" />
            <el-option label="内分泌科" value="endocrinology" />
            <el-option label="儿科" value="pediatrics" />
            <el-option label="骨科" value="orthopedics" />
            <el-option label="皮肤科" value="dermatology" />
            <el-option label="眼科" value="ophthalmology" />
            <el-option label="耳鼻喉科" value="ent" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="紧急程度" prop="severity">
          <el-radio-group v-model="createForm.severity" class="severity-group">
            <el-radio-button label="0">
              <span class="severity-label">一般</span>
            </el-radio-button>
            <el-radio-button label="1">
              <span class="severity-label">较急</span>
            </el-radio-button>
            <el-radio-button label="2">
              <span class="severity-label">紧急</span>
            </el-radio-button>
          </el-radio-group>
          <div class="form-tip">
            <template v-if="createForm.severity === '2'">
              <el-icon color="#f56c6c"><WarningFilled /></el-icon>
              <span class="emergency-tip">紧急情况建议立即前往医院就诊或拨打120</span>
            </template>
            <template v-else>
              紧急情况请优先线下就诊或拨打急救电话
            </template>
          </div>
        </el-form-item>
        
        <el-form-item label="症状描述" prop="symptoms">
          <el-input
            v-model="createForm.symptoms"
            type="textarea"
            :rows="8"
            placeholder="请详细描述您的症状，例如：
- 具体症状（头痛、咳嗽、发烧等）
- 症状持续多长时间
- 是否有其他伴随症状
- 之前是否有过类似情况
- 是否服用过药物"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="既往病史" prop="medical_history">
          <el-input
            v-model="createForm.medical_history"
            type="textarea"
            :rows="3"
            placeholder="如有慢性病、手术史、过敏史等请填写（可选）"
            maxlength="500"
          />
        </el-form-item>
      </el-form>
      
      <div class="disclaimer">
        <el-icon><WarningFilled /></el-icon>
        <span>本系统提供的诊断建议仅供参考，不能替代专业医生的诊断和治疗。如有紧急情况，请立即就医。</span>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="handleSubmitCreate" 
            :loading="submitting"
            :disabled="submitting"
          >
            {{ submitting ? '提交中...' : '提交问诊' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { InfoFilled, WarningFilled } from '@element-plus/icons-vue'
import { consultationApi, type Consultation } from '@/api/consultation'

const router = useRouter()

// 数据
const loading = ref(false)
const submitting = ref(false)
const consultations = ref<Consultation[]>([])
const createDialogVisible = ref(false)
const createFormRef = ref()

// 筛选表单
const filterForm = reactive({
  status: undefined as number | undefined
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 创建问诊表单
const createForm = reactive({
  title: '',
  department: '',
  severity: '0' as string,
  symptoms: '',
  medical_history: ''
})

// 表单验证规则
const createRules = {
  title: [
    { max: 50, message: '标题最多50个字符', trigger: 'blur' }
  ],
  symptoms: [
    { required: true, message: '请输入症状描述', trigger: 'blur' },
    { min: 5, message: '症状描述至少5个字符', trigger: 'blur' },
    { max: 1000, message: '症状描述最多1000个字符', trigger: 'blur' }
  ],
  medical_history: [
    { max: 500, message: '既往病史最多500个字符', trigger: 'blur' }
  ]
}

// 状态映射
const getStatusType = (status: number): string => {
  const types: Record<number, string> = {
    0: 'info',     // 进行中
    1: 'success',  // 已完成
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
    0: 'success',  // 低危
    1: 'warning', // 中危
    2: 'danger',  // 高危
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

// 加载问诊列表
const loadConsultations = async () => {
  loading.value = true
  try {
    const res = await consultationApi.getList({
      page: pagination.page,
      page_size: pagination.pageSize,
      status: filterForm.status
    })
    consultations.value = res.items || []
    pagination.total = res.total || 0
  } catch (error: any) {
    console.error('加载问诊列表失败:', error)
    if (error?.code === 'ERR_NETWORK' || error?.message?.includes('Network Error')) {
      ElMessage.error('网络错误，请检查后端服务是否启动')
    } else {
      ElMessage.error('加载问诊列表失败')
    }
    consultations.value = []
  } finally {
    loading.value = false
  }
}

// 删除问诊
const handleDelete = async (consultationId: number) => {
  try {
    await ElMessageBox.confirm(
      '删除后将无法恢复，确认要删除这条问诊记录吗？',
      '提示',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    await consultationApi.remove(consultationId)
    ElMessage.success('删除成功')
    // 重新加载列表
    loadConsultations()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除问诊失败:', error)
      ElMessage.error('删除问诊失败，请稍后重试')
    }
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

// 发起问诊
const handleCreateConsultation = () => {
  createForm.title = ''
  createForm.department = ''
  createForm.severity = '0'
  createForm.symptoms = ''
  createForm.medical_history = ''
  createDialogVisible.value = true
}

// 提交创建
const handleSubmitCreate = async () => {
  if (!createFormRef.value) return
  
  await createFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    try {
      const res = await consultationApi.create({
        title: createForm.title || undefined,
        symptoms: createForm.symptoms,
      })
      
      // request.ts 响应拦截器已经返回 response.data，所以 res 就是数据本身
      // 确保响应数据存在
      if (!res || !res.consultation_id) {
        console.error('服务器响应:', res)
        throw new Error('服务器响应异常，无法获取问诊ID')
      }
      
      const consultationId = res.consultation_id
      
      ElMessage.success('问诊创建成功')
      createDialogVisible.value = false
      // 刷新列表
      loadConsultations()
      // 跳转到对话页面
      router.push(`/consultation/chat/${consultationId}`)
    } catch (error: any) {
      console.error('创建问诊失败:', error)
      // 提供更友好的错误提示
      let errorMsg = '请稍后重试'
      
      if (error?.response?.data?.detail) {
        errorMsg = error.response.data.detail
      } else if (error?.response?.data?.message) {
        errorMsg = error.response.data.message
      } else if (error?.message) {
        errorMsg = error.message
      }
      
      ElMessage.error(`创建问诊失败: ${errorMsg}`)
    } finally {
      submitting.value = false
    }
  })
}

// 查看详情
const handleViewDetail = (id: number) => {
  router.push(`/consultation/${id}`)
}

// 继续对话
const handleChat = (id: number) => {
  router.push(`/consultation/chat/${id}`)
}

// 查看报告
const handleViewReport = (id: number) => {
  router.push(`/consultation/report/${id}`)
}

// 页面加载
onMounted(() => {
  loadConsultations()
})
</script>

<style scoped lang="scss">
.consultation-list-page {
  padding: 20px;
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
    }
  }
  
  .filter-card {
    margin-bottom: 20px;
  }
  
  .symptoms-text {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
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
}

/* 发起问诊对话框样式 */
.dialog-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background-color: #f0f9ff;
  border: 1px solid #bae7ff;
  border-radius: 6px;
  margin-bottom: 20px;
  color: #1890ff;
  font-size: 14px;
}

.create-form {
  .el-form-item {
    margin-bottom: 20px;
  }
}

.severity-group {
  display: flex;
  gap: 10px;
  
  .severity-label {
    font-weight: 500;
  }
}

.form-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
  
  .emergency-tip {
    color: #f56c6c;
    font-weight: 500;
  }
}

.disclaimer {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 16px;
  background-color: #fff7e6;
  border: 1px solid #ffd591;
  border-radius: 6px;
  margin-top: 10px;
  color: #d46b08;
  font-size: 13px;
  line-height: 1.5;
  
  .el-icon {
    flex-shrink: 0;
    margin-top: 2px;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>

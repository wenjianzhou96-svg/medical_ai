<template>
  <div class="dashboard-page">
    <h2>仪表盘</h2>
    
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #409eff">
              <el-icon :size="30"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalUsers }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #67c23a">
              <el-icon :size="30"><FirstAidKit /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalConsultations }}</div>
              <div class="stat-label">问诊总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #e6a23c">
              <el-icon :size="30"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalArticles }}</div>
              <div class="stat-label">文章总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #f56c6c">
              <el-icon :size="30"><FirstAidKit /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pendingConsultations }}</div>
              <div class="stat-label">待处理问诊</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近问诊</span>
          </template>
          <el-table :data="recentConsultations" stripe>
            <el-table-column prop="consultation_id" label="ID" width="60" />
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="时间" width="160" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统公告</span>
          </template>
          <el-list>
            <el-list-item v-for="item in announcements" :key="item.id">
              <div class="announcement-item">
                <span class="title">{{ item.title }}</span>
                <span class="time">{{ item.time }}</span>
              </div>
            </el-list-item>
          </el-list>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { User, FirstAidKit, Document } from '@element-plus/icons-vue'

const stats = ref({
  totalUsers: 0,
  totalConsultations: 0,
  totalArticles: 0,
  pendingConsultations: 0
})

const recentConsultations = ref<any[]>([])

const announcements = ref([
  { id: 1, title: '系统升级通知', time: '2026-02-26' },
  { id: 2, title: '新功能上线', time: '2026-02-25' }
])

const getStatusType = (status: number) => {
  const types: Record<number, string> = {
    0: 'info',
    1: 'warning',
    2: 'success',
    3: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: number) => {
  const texts: Record<number, string> = {
    0: '待回复',
    1: '处理中',
    2: '已完成',
    3: '已关闭'
  }
  return texts[status] || '未知'
}
</script>

<style scoped lang="scss">
.dashboard-page {
  h2 {
    margin: 0 0 20px 0;
  }
  
  .stat-card {
    display: flex;
    align-items: center;
    gap: 20px;
    
    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    
    .stat-info {
      .stat-value {
        font-size: 28px;
        font-weight: bold;
      }
      
      .stat-label {
        color: #666;
        font-size: 14px;
      }
    }
  }
  
  .announcement-item {
    display: flex;
    justify-content: space-between;
    width: 100%;
    
    .title {
      flex: 1;
    }
    
    .time {
      color: #999;
      font-size: 12px;
    }
  }
}
</style>

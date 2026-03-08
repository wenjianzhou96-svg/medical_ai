<template>
  <div class="vital-signs-page">
    <div class="page-header">
      <h2>体征数据</h2>
      <el-button type="primary" @click="handleAdd">添加记录</el-button>
    </div>
    
    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="血压" name="blood_pressure">
        <div class="chart-container">
          <el-empty description="暂无血压数据" />
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="心率" name="heart_rate">
        <div class="chart-container">
          <el-empty description="暂无心率数据" />
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="血糖" name="blood_sugar">
        <div class="chart-container">
          <el-empty description="暂无血糖数据" />
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="体温" name="temperature">
        <div class="chart-container">
          <el-empty description="暂无体温数据" />
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <el-table :data="vitalSigns" stripe style="width: 100%; margin-top: 20px">
      <el-table-column prop="sign_type" label="测量类型" width="120" />
      <el-table-column prop="value" label="测量值" width="120">
        <template #default="{ row }">
          {{ row.value }} {{ row.unit }}
        </template>
      </el-table-column>
      <el-table-column prop="measured_at" label="测量时间" width="180" />
      <el-table-column prop="notes" label="备注" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('blood_pressure')
const vitalSigns = ref<any[]>([])

const handleAdd = () => {
  // TODO: 打开添加记录弹窗
}
</script>

<style scoped lang="scss">
.vital-signs-page {
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
  
  .chart-container {
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>

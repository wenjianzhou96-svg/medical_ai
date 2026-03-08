<template>
  <div class="doctor-manage-page">
    <div class="page-header">
      <h2>医生管理</h2>
      <el-button type="primary" @click="handleAdd">添加医生</el-button>
    </div>
    
    <el-table :data="doctors" stripe style="width: 100%">
      <el-table-column prop="doctor_id" label="医生ID" width="80" />
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="department" label="科室" width="120" />
      <el-table-column prop="title" label="职称" width="100" />
      <el-table-column prop="specialties" label="专长" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
            {{ row.status === 1 ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button link :type="row.status === 1 ? 'danger' : 'success'" size="small" @click="handleToggleStatus(row)">
            {{ row.status === 1 ? '禁用' : '启用' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-pagination
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      style="margin-top: 20px; justify-content: center"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const doctors = ref<any[]>([])

const handleAdd = () => {
  // TODO: 打开添加弹窗
}

const handleEdit = (row: any) => {
  // TODO: 打开编辑弹窗
  console.log('编辑医生:', row)
}

const handleToggleStatus = (row: any) => {
  row.status = row.status === 1 ? 0 : 1
  ElMessage.success(row.status === 1 ? '已启用' : '已禁用')
}
</script>

<style scoped lang="scss">
.doctor-manage-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
    }
  }
}
</style>

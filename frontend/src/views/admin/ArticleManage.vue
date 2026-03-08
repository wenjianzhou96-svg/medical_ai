<template>
  <div class="article-manage-page">
    <div class="page-header">
      <h2>文章管理</h2>
      <el-button type="primary" @click="handleAdd">发布文章</el-button>
    </div>
    
    <el-table :data="articles" stripe style="width: 100%">
      <el-table-column prop="article_id" label="文章ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="tags" label="标签" width="150" />
      <el-table-column prop="view_count" label="阅读量" width="80" />
      <el-table-column prop="like_count" label="点赞数" width="80" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" size="small">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="published_at" label="发布时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="success" size="small" @click="handlePublish(row)">发布</el-button>
          <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
import { ElMessage, ElMessageBox } from 'element-plus'

const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const articles = ref<any[]>([])

const getStatusType = (status: number) => {
  const types: Record<number, string> = {
    0: 'info',
    1: 'success'
  }
  return types[status] || 'info'
}

const getStatusText = (status: number) => {
  return status === 1 ? '已发布' : '草稿'
}

const handleAdd = () => {
  // TODO: 打开添加文章弹窗
}

const handleEdit = (row: any) => {
  // TODO: 打开编辑弹窗
  console.log('编辑文章:', row)
}

const handlePublish = (row: any) => {
  row.status = 1
  row.published_at = new Date().toISOString()
  ElMessage.success('发布成功')
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm('确定要删除这篇文章吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped lang="scss">
.article-manage-page {
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

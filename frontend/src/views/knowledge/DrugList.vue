<template>
  <div class="drug-list-page">
    <div class="page-header">
      <h2>药品查询</h2>
      <el-input
        v-model="keyword"
        placeholder="请输入药品名称"
        class="search-input"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
    </div>
    
    <el-table :data="drugs" stripe style="width: 100%">
      <el-table-column prop="drug_id" label="药品ID" width="80" />
      <el-table-column prop="drug_name" label="药品名称" width="150" />
      <el-table-column prop="generic_name" label="通用名" width="150" />
      <el-table-column prop="specification" label="规格" />
      <el-table-column prop="manufacturer" label="生产厂家" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleViewDetail(row.drug_id)">查看</el-button>
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
    
    <!-- 药品详情弹窗 -->
    <el-dialog v-model="dialogVisible" title="药品详情" width="600px">
      <el-descriptions v-if="currentDrug" :column="1" border>
        <el-descriptions-item label="药品名称">{{ currentDrug.drug_name }}</el-descriptions-item>
        <el-descriptions-item label="通用名">{{ currentDrug.generic_name }}</el-descriptions-item>
        <el-descriptions-item label="规格">{{ currentDrug.specification }}</el-descriptions-item>
        <el-descriptions-item label="生产厂家">{{ currentDrug.manufacturer }}</el-descriptions-item>
        <el-descriptions-item label="用法用量">{{ currentDrug.usage }}</el-descriptions-item>
        <el-descriptions-item label="适应症">{{ currentDrug.indication }}</el-descriptions-item>
        <el-descriptions-item label="禁忌">{{ currentDrug.contraindication }}</el-descriptions-item>
        <el-descriptions-item label="不良反应">{{ currentDrug.side_effect }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

const keyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const drugs = ref<any[]>([])
const dialogVisible = ref(false)
const currentDrug = ref<any>(null)

const handleSearch = () => {
  // TODO: 调用搜索 API
  console.log('搜索药品:', keyword.value)
}

const handleViewDetail = (id: number) => {
  // TODO: 获取药品详情
  currentDrug.value = {
    drug_id: id,
    drug_name: '示例药品',
    generic_name: '示例通用名',
    specification: '10mg*10片',
    manufacturer: '示例制药厂',
    usage: '口服，一次1片，一日3次',
    indication: '用于治疗感冒发热',
    contraindication: '对本品过敏者禁用',
    side_effect: '偶见恶心、呕吐等胃肠道反应'
  }
  dialogVisible.value = true
}
</script>

<style scoped lang="scss">
.drug-list-page {
  padding: 20px;
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h2 {
      margin: 0;
    }
    
    .search-input {
      width: 300px;
    }
  }
}
</style>

<template>
  <div class="knowledge-search-page">
    <div class="search-header">
      <h2>医疗知识库</h2>
      <el-input
        v-model="keyword"
        placeholder="请输入关键词搜索"
        size="large"
        class="search-input"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
    </div>
    
    <div class="search-filters">
      <el-radio-group v-model="category" size="small">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="disease">疾病</el-radio-button>
        <el-radio-button label="symptom">症状</el-radio-button>
        <el-radio-button label="treatment">治疗</el-radio-button>
        <el-radio-button label="prevention">预防</el-radio-button>
      </el-radio-group>
    </div>
    
    <div class="search-results">
      <el-empty v-if="results.length === 0" description="请输入关键词搜索" />
      
      <el-card 
        v-for="item in results" 
        :key="item.knowledge_id" 
        class="result-card"
        shadow="hover"
        @click="handleViewDetail(item.knowledge_id)"
      >
        <template #header>
          <div class="card-header">
            <span class="title">{{ item.title }}</span>
            <el-tag size="small">{{ item.category }}</el-tag>
          </div>
        </template>
        <p class="summary">{{ item.summary }}</p>
        <div class="meta">
          <span>关键词: {{ item.keywords }}</span>
          <span>阅读量: {{ item.view_count }}</span>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()

const keyword = ref('')
const category = ref('')
const results = ref<any[]>([])

const handleSearch = () => {
  // TODO: 调用搜索 API
  console.log('搜索:', keyword.value, '分类:', category.value)
}

const handleViewDetail = (id: number) => {
  // TODO: 跳转到详情页
  console.log('查看详情:', id)
}
</script>

<style scoped lang="scss">
.knowledge-search-page {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
  
  .search-header {
    text-align: center;
    margin-bottom: 30px;
    
    h2 {
      margin-bottom: 20px;
    }
    
    .search-input {
      max-width: 600px;
    }
  }
  
  .search-filters {
    margin-bottom: 20px;
    text-align: center;
  }
  
  .search-results {
    .result-card {
      margin-bottom: 15px;
      cursor: pointer;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .title {
          font-weight: bold;
        }
      }
      
      .summary {
        color: #666;
        margin: 10px 0;
      }
      
      .meta {
        display: flex;
        gap: 20px;
        font-size: 12px;
        color: #999;
      }
    }
  }
}
</style>

<template>
  <div class="health-record-page">
    <div class="page-header">
      <h2>健康档案</h2>
      <el-button type="primary" @click="handleEdit">编辑档案</el-button>
    </div>
    
    <el-card v-if="healthRecord">
      <el-descriptions title="基本信息" :column="2" border>
        <el-descriptions-item label="血型">{{ healthRecord.blood_type || '未设置' }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ getGenderText(healthRecord.gender) }}</el-descriptions-item>
        <el-descriptions-item label="身高">{{ healthRecord.height ? healthRecord.height + ' cm' : '未设置' }}</el-descriptions-item>
        <el-descriptions-item label="体重">{{ healthRecord.weight ? healthRecord.weight + ' kg' : '未设置' }}</el-descriptions-item>
        <el-descriptions-item label="BMI">{{ healthRecord.bmi || '未设置' }}</el-descriptions-item>
      </el-descriptions>
      
      <el-divider />
      
      <el-descriptions title="病史信息" :column="1" border>
        <el-descriptions-item label="既往病史">{{ healthRecord.medical_history || '无' }}</el-descriptions-item>
        <el-descriptions-item label="家族病史">{{ healthRecord.family_history || '无' }}</el-descriptions-item>
        <el-descriptions-item label="过敏史">{{ healthRecord.allergy_history || '无' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <el-empty v-else description="暂无健康档案" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const healthRecord = ref<any>(null)

const getGenderText = (gender?: number) => {
  const texts: Record<number, string> = {
    0: '未知',
    1: '男',
    2: '女'
  }
  return gender ? texts[gender] : '未设置'
}

const handleEdit = () => {
  // TODO: 打开编辑弹窗
}

onMounted(() => {
  // TODO: 加载健康档案
  healthRecord.value = {
    blood_type: 'O',
    gender: 1,
    height: 175,
    weight: 70,
    bmi: 22.9,
    medical_history: '无',
    family_history: '无',
    allergy_history: '无'
  }
})
</script>

<style scoped lang="scss">
.health-record-page {
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
}
</style>

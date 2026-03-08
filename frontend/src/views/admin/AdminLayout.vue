<template>
  <el-container class="admin-layout">
    <el-aside width="200px">
      <div class="logo">
        <h3>医疗系统管理</h3>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="admin-menu"
        router
      >
        <el-menu-item index="/admin/dashboard">
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/doctors">
          <span>医生管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/articles">
          <span>文章管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/consultations">
          <span>问诊管理</span>
        </el-menu-item>
        <el-sub-menu index="system">
          <template #title>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/admin/roles">
            <span>角色管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/permissions">
            <span>权限管理</span>
          </el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/">
          <span>返回前台</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-left">
          <span class="username">{{ userInfo?.username || '管理员' }}</span>
        </div>
        <div class="header-right">
          <el-button @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)
const activeMenu = computed(() => route.path)

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.admin-layout {
  height: 100vh;
  
  .el-aside {
    background-color: #304156;
    
    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #2b3a4a;
      
      h3 {
        color: white;
        margin: 0;
        font-size: 16px;
      }
    }
    
    .admin-menu {
      border-right: none;
      background-color: #304156;
      
      :deep(.el-menu-item) {
        color: #bfcbd9;
        
        &:hover {
          background-color: #263445;
        }
        
        &.is-active {
          background-color: #409eff !important;
          color: white;
        }
      }
    }
  }
  
  .el-header {
    background-color: white;
    box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    
    .username {
      font-weight: 500;
    }
  }
  
  .el-main {
    background-color: #f0f2f5;
    padding: 20px;
  }
}
</style>

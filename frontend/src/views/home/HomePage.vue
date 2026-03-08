<template>
  <div class="home-page">
    <!-- 顶部导航 -->
    <div class="header">
      <div class="container">
        <div class="logo">
          <el-icon :size="32" color="#409eff"><FirstAidKit /></el-icon>
          <span>医疗智能体系统</span>
        </div>
        <div class="nav">
          <el-menu mode="horizontal" :ellipsis="false">
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/consultation">智能问诊</el-menu-item>
            <el-menu-item index="/knowledge">知识库</el-menu-item>
            <el-menu-item index="/health" v-if="userStore.isLoggedIn">健康档案</el-menu-item>
          </el-menu>
        </div>
        <div class="user-actions">
          <template v-if="userStore.isLoggedIn">
            <el-dropdown>
              <span class="user-info">
                <el-avatar :size="32" :src="userStore.userInfo?.avatar_url" />
                <span>{{ userStore.userInfo?.username }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="$router.push('/profile')">个人中心</el-dropdown-item>
                  <el-dropdown-item @click="$router.push('/consultation')">我的问诊</el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="primary" @click="$router.push('/login')">登录</el-button>
            <el-button @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </div>

    <!-- 主体内容 -->
    <div class="main-content">
      <!-- Banner区域 -->
      <div class="hero-section">
        <div class="container">
          <div class="hero-content">
            <h1>基于大语言模型的医疗智能体系统</h1>
            <p>为您提供智能问诊、健康管理、知识查询等全方位医疗服务</p>
            <div class="hero-actions">
              <el-button type="primary" size="large" @click="$router.push('/consultation')">
                <el-icon><ChatDotRound /></el-icon>
                开始问诊
              </el-button>
              <el-button size="large" @click="$router.push('/knowledge')">
                <el-icon><Search /></el-icon>
                知识搜索
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能介绍 -->
      <div class="features-section">
        <div class="container">
          <h2 class="section-title">核心功能</h2>
          <div class="features-grid">
            <div class="feature-card">
              <el-icon :size="48"><ChatDotSquare /></el-icon>
              <h3>智能问诊</h3>
              <p>基于大语言模型，提供多轮对话式智能问诊，辅助健康评估</p>
            </div>
            <div class="feature-card">
              <el-icon :size="48"><FirstAidKit /></el-icon>
              <h3>健康管理</h3>
              <p>全面的健康档案管理，体征数据记录，健康趋势分析</p>
            </div>
            <div class="feature-card">
              <el-icon :size="48"><Reading /></el-icon>
              <h3>知识库</h3>
              <p>权威医学知识库，药品信息查询，临床指南参考</p>
            </div>
            <div class="feature-card">
              <el-icon :size="48"><DataAnalysis /></el-icon>
              <h3>数据分析</h3>
              <p>多维度健康数据分析，可视化图表，个性化健康建议</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 健康科普 -->
      <div class="articles-section">
        <div class="container">
          <h2 class="section-title">健康科普</h2>
          <div class="articles-grid">
            <el-card v-for="article in articles" :key="article.article_id" class="article-card" @click="viewArticle(article.article_id)">
              <img :src="article.cover_image || '/default-cover.jpg'" class="article-cover" />
              <div class="article-content">
                <h3>{{ article.title }}</h3>
                <p>{{ article.summary }}</p>
                <div class="article-meta">
                  <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
                  <span><el-icon><Star /></el-icon> {{ article.like_count }}</span>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <div class="footer">
      <div class="container">
        <p>&copy; 2026 医疗智能体系统. All rights reserved.</p>
        <p>本系统仅供演示，不能替代专业医疗诊断</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ChatDotRound, Search, ChatDotSquare, FirstAidKit, Reading, DataAnalysis, View, Star } from '@element-plus/icons-vue'
import request from '@/api/request'
import type { Article } from '@/types'

const router = useRouter()
const userStore = useUserStore()

const articles = ref<Article[]>([])

onMounted(async () => {
  try {
    const res = await request.get<Article[]>('/articles', { params: { limit: 6 } })
    articles.value = res
  } catch (e) {
    console.error('获取文章失败', e)
  }
})

const handleLogout = async () => {
  await userStore.logout()
  router.push('/')
}

const viewArticle = (id: number) => {
  router.push(`/articles/${id}`)
}
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
    font-weight: bold;
    color: #409eff;

    .el-icon {
      height: 36px;
    }
  }

  .nav {
    flex: 1;
    display: flex;
    justify-content: center;

    :deep(.el-menu) {
      border: none;
    }
  }

  .user-actions {
    display: flex;
    gap: 10px;

    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }
  }
}

.main-content {
  .hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 80px 0;

    .hero-content {
      text-align: center;
      max-width: 800px;
      margin: 0 auto;

      h1 {
        font-size: 42px;
        margin-bottom: 20px;
      }

      p {
        font-size: 18px;
        margin-bottom: 40px;
        opacity: 0.9;
      }

      .hero-actions {
        display: flex;
        gap: 20px;
        justify-content: center;
      }
    }
  }

  .features-section {
    padding: 80px 0;
    background: white;

    .section-title {
      text-align: center;
      font-size: 32px;
      margin-bottom: 50px;
    }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 30px;

      .feature-card {
        text-align: center;
        padding: 30px;
        border-radius: 12px;
        background: #f8f9fa;
        transition: all 0.3s;

        &:hover {
          transform: translateY(-5px);
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }

        .el-icon {
          color: #409eff;
          margin-bottom: 20px;
        }

        h3 {
          font-size: 20px;
          margin-bottom: 15px;
        }

        p {
          color: #666;
          line-height: 1.6;
        }
      }
    }
  }

  .articles-section {
    padding: 80px 0;

    .section-title {
      text-align: center;
      font-size: 32px;
      margin-bottom: 50px;
    }

    .articles-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 30px;

      .article-card {
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
          transform: translateY(-5px);
        }

        .article-cover {
          width: 100;
          height: 180px;
          object-fit: cover;
        }

        .article-content {
          padding: 15px 0;

          h3 {
            font-size: 18px;
            margin-bottom: 10px;
          }

          p {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 15px;
          }

          .article-meta {
            display: flex;
            gap: 15px;
            color: #999;
            font-size: 13px;
          }
        }
      }
    }
  }
}

.footer {
  background: #333;
  color: white;
  padding: 30px 0;
  text-align: center;

  p {
    margin: 5px 0;
    opacity: 0.7;
  }
}
</style>

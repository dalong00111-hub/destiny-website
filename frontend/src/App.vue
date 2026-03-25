<template>
  <div id="app">
    <el-container>
      <!-- 头部导航 -->
      <el-header class="header">
        <div class="header-content">
          <div class="logo">
            <h1>🔮 命运预测</h1>
            <p class="slogan">10元请大师回家 · 遇事不决，随时求解</p>
          </div>
          <div class="nav">
            <el-button type="primary" @click="scrollToService">立即测算</el-button>
            <el-button link @click="scrollToAbout">关于我们</el-button>
            <el-button link @click="scrollToFAQ">常见问题</el-button>
          </div>
        </div>
      </el-header>

      <!-- 主要内容 -->
      <el-main>
        <router-view />
      </el-main>

      <!-- 底部 -->
      <el-footer class="footer">
        <div class="footer-content">
          <p>© 2026 命运预测 · 仅供娱乐参考 · 科学命理分析</p>
          <p class="disclaimer">
            本网站提供的命理分析仅供参考，不构成任何决策建议。
            命运掌握在自己手中，努力才是最好的风水。
          </p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const scrollToService = () => {
  router.push('/service')
}

const scrollToAbout = () => {
  router.push('/about')
}

const scrollToFAQ = () => {
  router.push('/faq')
}
</script>

<style scoped>
.header {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo h1 {
  color: #333;
  margin: 0;
  font-size: 24px;
}

.slogan {
  color: #666;
  margin: 4px 0 0;
  font-size: 14px;
}

.nav {
  display: flex;
  gap: 12px;
}

.footer {
  background: #2c3e50;
  color: #ecf0f1;
  text-align: center;
  padding: 30px 20px;
}

.footer-content {
  max-width: 800px;
  margin: 0 auto;
}

.disclaimer {
  margin-top: 15px;
  font-size: 12px;
  color: #bdc3c7;
  line-height: 1.6;
}
</style>
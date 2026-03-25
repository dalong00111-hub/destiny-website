<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero">
      <div class="hero-content">
        <h2 class="hero-title">🔮 10元请大师回家</h2>
        <p class="hero-subtitle">遇事不决，随时求解 · 科学命理，精准分析</p>
        
        <div class="hero-features">
          <div class="feature">
            <div class="feature-icon">💰</div>
            <h3>价格亲民</h3>
            <p>仅需10元，即可获得专业命理分析</p>
          </div>
          <div class="feature">
            <div class="feature-icon">⚡</div>
            <h3>即时解答</h3>
            <p>无需预约，提交问题立即获得答案</p>
          </div>
          <div class="feature">
            <div class="feature-icon">🎯</div>
            <h3>科学依据</h3>
            <p>基于传统八字命理，结合现代数据分析</p>
          </div>
          <div class="feature">
            <div class="feature-icon">🔒</div>
            <h3>隐私保护</h3>
            <p>您的个人信息严格加密，安全可靠</p>
          </div>
        </div>

        <el-button 
          type="primary" 
          size="large" 
          class="start-btn"
          @click="$router.push('/service')"
        >
          🚀 立即开始测算
        </el-button>
      </div>
    </section>

    <!-- 服务流程 -->
    <section class="process">
      <h2 class="section-title">简单四步，了解命运</h2>
      <div class="process-steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>输入生辰</h3>
          <p>填写准确的出生年月日时</p>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>支付10元</h3>
          <p>微信/支付宝扫码支付</p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>获得分析</h3>
          <p>立即查看八字命理分析报告</p>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>追加提问</h3>
          <p>可继续提问3个具体问题</p>
        </div>
      </div>
    </section>

    <!-- 用户评价 -->
    <section class="testimonials">
      <h2 class="section-title">用户真实评价</h2>
      <div class="testimonial-list">
        <div class="testimonial">
          <p class="content">"很准！分析得很到位，给了我很多启发。"</p>
          <p class="author">—— 张女士，32岁</p>
        </div>
        <div class="testimonial">
          <p class="content">"10元超值，比外面几百的还详细。"</p>
          <p class="author">—— 李先生，28岁</p>
        </div>
        <div class="testimonial">
          <p class="content">"随时可以问，太方便了，已经推荐给朋友。"</p>
          <p class="author">—— 王小姐，25岁</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// 首页逻辑
</script>

<style scoped>
.home {
  padding: 20px 0;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
  border-radius: 20px;
  margin-bottom: 60px;
}

.hero-content {
  max-width: 1000px;
  margin: 0 auto;
}

.hero-title {
  font-size: 48px;
  margin-bottom: 20px;
  font-weight: bold;
}

.hero-subtitle {
  font-size: 20px;
  margin-bottom: 50px;
  opacity: 0.9;
}

.hero-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  margin-bottom: 50px;
}

.feature {
  background: rgba(255, 255, 255, 0.1);
  padding: 30px 20px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.feature h3 {
  margin: 10px 0;
  font-size: 18px;
}

.feature p {
  opacity: 0.8;
  font-size: 14px;
  line-height: 1.5;
}

.start-btn {
  font-size: 18px;
  padding: 20px 40px;
  border-radius: 50px;
  background: white;
  color: #764ba2;
  border: none;
  font-weight: bold;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.section-title {
  text-align: center;
  font-size: 36px;
  margin-bottom: 50px;
  color: #333;
}

.process {
  padding: 60px 20px;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

.step {
  text-align: center;
  padding: 30px 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.step-number {
  width: 50px;
  height: 50px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  margin: 0 auto 20px;
}

.step h3 {
  margin: 15px 0 10px;
  color: #333;
}

.step p {
  color: #666;
  font-size: 14px;
}

.testimonials {
  padding: 60px 20px;
  background: #f8f9fa;
  border-radius: 20px;
  margin: 40px 0;
}

.testimonial-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

.testimonial {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.testimonial .content {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
  font-style: italic;
}

.testimonial .author {
  text-align: right;
  color: #888;
  font-size: 14px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .section-title {
    font-size: 28px;
  }
}
</style>
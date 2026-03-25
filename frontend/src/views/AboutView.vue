<template>
  <div class="about">
    <div class="about-container">
      <h2 class="about-title">关于我们</h2>
      
      <div class="about-content">
        <!-- 使命愿景 -->
        <section class="mission">
          <h3>🎯 我们的使命</h3>
          <p>让传统命理智慧以科学、便捷的方式服务现代人，帮助大家在重要决策时获得更多参考视角。</p>
        </section>

        <!-- 核心理念 -->
        <section class="philosophy">
          <h3>💡 核心理念</h3>
          <div class="philosophy-grid">
            <div class="philosophy-item">
              <div class="icon">🔬</div>
              <h4>科学态度</h4>
              <p>将传统八字命理与现代数据分析结合，提供有理有据的分析。</p>
            </div>
            <div class="philosophy-item">
              <div class="icon">🤝</div>
              <h4>诚信服务</h4>
              <p>明码标价，10元一次，绝不虚假宣传，绝不诱导消费。</p>
            </div>
            <div class="philosophy-item">
              <div class="icon">🔒</div>
              <h4>隐私保护</h4>
              <p>您的个人信息严格加密，分析结果仅您可见，绝不外泄。</p>
            </div>
            <div class="philosophy-item">
              <div class="icon">🎯</div>
              <h4>实用价值</h4>
              <p>提供具体可行的建议，帮助您更好地规划人生。</p>
            </div>
          </div>
        </section>

        <!-- 技术优势 -->
        <section class="technology">
          <h3>🚀 技术优势</h3>
          <div class="tech-features">
            <div class="tech-item">
              <h4>AI智能分析</h4>
              <p>结合人工智能技术，提供个性化、深度的命理分析。</p>
            </div>
            <div class="tech-item">
              <h4>实时计算</h4>
              <p>提交信息后立即生成报告，无需等待。</p>
            </div>
            <div class="tech-item">
              <h4>移动优先</h4>
              <p>完美适配手机端，随时随地使用。</p>
            </div>
            <div class="tech-item">
              <h4>安全支付</h4>
              <p>集成微信、支付宝支付，安全便捷。</p>
            </div>
          </div>
        </section>

        <!-- 团队介绍 -->
        <section class="team">
          <h3>👥 团队介绍</h3>
          <p>我们是一支由命理研究者、数据科学家和软件工程师组成的跨学科团队，致力于将传统智慧与现代科技完美结合。</p>
          
          <div class="team-members">
            <div class="member">
              <div class="member-avatar">👨‍💻</div>
              <div class="member-info">
                <h4>张大师</h4>
                <p class="role">命理专家</p>
                <p class="desc">20年命理研究经验，精通八字、紫微斗数</p>
              </div>
            </div>
            <div class="member">
              <div class="member-avatar">👩‍🔬</div>
              <div class="member-info">
                <h4>李博士</h4>
                <p class="role">数据科学家</p>
                <p class="desc">统计学博士，负责算法优化和数据分析</p>
              </div>
            </div>
            <div class="member">
              <div class="member-avatar">👨‍💼</div>
              <div class="member-info">
                <h4>王总监</h4>
                <p class="role">产品总监</p>
                <p class="desc">10年互联网产品经验，负责用户体验设计</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 联系方式 -->
        <section class="contact">
          <h3>📞 联系我们</h3>
          <div class="contact-info">
            <p>如有任何问题或建议，欢迎通过以下方式联系我们：</p>
            <ul>
              <li>邮箱：contact@destiny.com</li>
              <li>微信：DestinyService</li>
              <li>工作时间：周一至周五 9:00-18:00</li>
            </ul>
          </div>
        </section>

        <!-- 免责声明 -->
        <section class="disclaimer">
          <h3>📝 重要声明</h3>
          <div class="disclaimer-content">
            <p>1. 本网站提供的命理分析仅供娱乐参考，不构成任何决策建议。</p>
            <p>2. 命运掌握在自己手中，努力奋斗才是改变命运的最佳途径。</p>
            <p>3. 请勿沉迷命理分析，理性看待分析结果。</p>
            <p>4. 如遇心理困扰，建议寻求专业心理咨询师帮助。</p>
          </div>
        </section>
      </div>

      <div class="back-home">
        <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 关于页面逻辑
</script>

<style scoped>
.about {
  padding: 40px 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.about-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.about-title {
  text-align: center;
  font-size: 36px;
  color: #333;
  margin-bottom: 40px;
}

.about-content section {
  margin-bottom: 50px;
}

.about-content h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #667eea;
}

.about-content p {
  line-height: 1.6;
  color: #555;
  margin-bottom: 15px;
}

.philosophy-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  margin-top: 20px;
}

.philosophy-item {
  text-align: center;
  padding: 30px 20px;
  background: #f8f9fa;
  border-radius: 15px;
  border: 1px solid #e9ecef;
}

.philosophy-item .icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.philosophy-item h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 18px;
}

.philosophy-item p {
  font-size: 14px;
  color: #666;
}

.tech-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.tech-item {
  padding: 20px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 10px;
}

.tech-item h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 18px;
}

.tech-item p {
  font-size: 14px;
  color: #666;
}

.team-members {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.member {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 15px;
}

.member-avatar {
  font-size: 50px;
}

.member-info h4 {
  color: #333;
  margin-bottom: 5px;
  font-size: 18px;
}

.member-info .role {
  color: #667eea;
  font-weight: bold;
  margin-bottom: 5px;
}

.member-info .desc {
  color: #666;
  font-size: 14px;
}

.contact-info ul {
  list-style: none;
  padding-left: 0;
}

.contact-info li {
  padding: 8px 0;
  color: #555;
  border-bottom: 1px solid #eee;
}

.contact-info li:last-child {
  border-bottom: none;
}

.disclaimer-content {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 10px;
  padding: 20px;
}

.disclaimer-content p {
  color: #856404;
  margin-bottom: 10px;
  font-size: 14px;
}

.back-home {
  text-align: center;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

@media (max-width: 768px) {
  .about-container {
    padding: 20px;
  }
  
  .about-title {
    font-size: 28px;
  }
  
  .philosophy-grid,
  .tech-features,
  .team-members {
    grid-template-columns: 1fr;
  }
}
</style>
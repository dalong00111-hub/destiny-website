<template>
  <div class="faq">
    <div class="faq-container">
      <h2 class="faq-title">❓ 常见问题解答</h2>
      <p class="faq-subtitle">如果您有其他问题，欢迎随时联系我们</p>

      <div class="faq-content">
        <!-- 服务相关 -->
        <section class="faq-section">
          <h3>📋 服务相关</h3>
          <el-collapse v-model="activeService">
            <el-collapse-item name="1" title="1. 这个服务真的只要10元吗？">
              <div class="faq-answer">
                <p>是的，基础命理分析服务仅需<strong>10元/次</strong>。包含：</p>
                <ul>
                  <li>完整的八字排盘分析</li>
                  <li>性格、事业、感情、健康四大维度解读</li>
                  <li>近期运势预测</li>
                  <li>3次追加提问机会</li>
                </ul>
                <p>我们坚持透明定价，绝不隐藏收费。</p>
              </div>
            </el-collapse-item>

            <el-collapse-item name="2" title="2. 支付后多久能收到分析报告？">
              <div class="faq-answer">
                <p><strong>立即生成！</strong>支付成功后，系统会在<strong>30秒内</strong>自动生成您的命理分析报告。</p>
                <p>相比传统命理咨询需要预约等待，我们的AI系统可以实时分析，让您立即获得结果。</p>
              </div>
            </el-collapse-item>

            <el-collapse-item name="3" title="3. 可以退款吗？">
              <div class="faq-answer">
                <p>由于命理分析是即时生成的知识服务，一般情况下不支持退款。但如果您遇到以下情况，可以申请退款：</p>
                <ul>
                  <li>支付成功但未收到分析报告</li>
                  <li>报告内容出现严重错误</li>
                  <li>技术故障导致服务无法使用</li>
                </ul>
                <p>退款申请请在支付后24小时内联系客服处理。</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </section>

        <!-- 技术相关 -->
        <section class="faq-section">
          <h3>💻 技术相关</h3>
          <el-collapse v-model="activeTech">
            <el-collapse-item name="1" title="1. 你们的分析准确吗？">
              <div class="faq-answer">
                <p>我们的分析基于：</p>
                <ul>
                  <li><strong>传统八字命理算法</strong>：严格按照古代命理经典计算</li>
                  <li><strong>大数据分析</strong>：结合大量命理案例进行优化</li>
                  <li><strong>AI智能解读</strong>：提供个性化、深度的分析</li>
                </ul>
                <p>但需要说明的是：</p>
                <ul>
                  <li>命理分析是概率性预测，不是100%准确</li>
                  <li>结果仅供参考，请勿作为唯一决策依据</li>
                  <li>命运掌握在自己手中，努力才是关键</li>
                </ul>
              </div>
            </el-collapse-item>

            <el-collapse-item name="2" title="2. 需要提供哪些个人信息？">
              <div class="faq-answer">
                <p>只需要提供：</p>
                <ul>
                  <li><strong>出生年月日时</strong>（用于八字计算）</li>
                  <li><strong>性别</strong>（男女命理算法不同）</li>
                </ul>
                <p><strong>我们承诺：</strong></p>
                <ul>
                  <li>绝不收集身份证号、手机号等敏感信息</li>
                  <li>所有数据加密存储，绝不泄露</li>
                  <li>分析结果仅您可见，绝不外传</li>
                  <li>支持随时删除您的数据</li>
                </ul>
              </div>
            </el-collapse-item>

            <el-collapse-item name="3" title="3. 可以在手机上使用吗？">
              <div class="faq-answer">
                <p><strong>完全可以！</strong>我们的网站采用响应式设计，完美适配：</p>
                <ul>
                  <li>📱 手机（iPhone、Android）</li>
                  <li>💻 平板（iPad、Android平板）</li>
                  <li>🖥️ 电脑（Windows、Mac）</li>
                </ul>
                <p>建议使用最新版本的Chrome、Safari、微信浏览器等现代浏览器。</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </section>

        <!-- 命理知识 -->
        <section class="faq-section">
          <h3>🔮 命理知识</h3>
          <el-collapse v-model="activeKnowledge">
            <el-collapse-item name="1" title="1. 什么是八字命理？">
              <div class="faq-answer">
                <p>八字命理，又称四柱命理，是中国传统命理学的重要组成部分：</p>
                <ul>
                  <li><strong>八字</strong>：指出生时的年、月、日、时对应的天干地支，共八个字</li>
                  <li><strong>四柱</strong>：年柱、月柱、日柱、时柱</li>
                  <li><strong>原理</strong>：通过分析八字之间的五行生克关系，推断人的命运走势</li>
                </ul>
                <p>八字命理已有千年历史，是中华传统文化的重要遗产。</p>
              </div>
            </el-collapse-item>

            <el-collapse-item name="2" title="2. 为什么出生时间要精确到时辰？">
              <div class="faq-answer">
                <p>时辰在八字命理中非常重要：</p>
                <ul>
                  <li><strong>影响时柱</strong>：时辰决定时柱，时柱影响整体格局</li>
                  <li><strong>决定五行</strong>：不同时辰对应不同的五行属性</li>
                  <li><strong>关系运势</strong>：时辰影响晚年运势和子女运势</li>
                </ul>
                <p>如果不知道具体时辰：</p>
                <ul>
                  <li>尽量回忆，可以询问家人</li>
                  <li>如果实在不知道，可以选择"不确定"</li>
                  <li>系统会根据日柱进行推算，但准确性会降低</li>
                </ul>
              </div>
            </el-collapse-item>

            <el-collapse-item name="3" title="3. 命理分析能改变命运吗？">
              <div class="faq-answer">
                <p><strong>命理分析不能改变命运，但可以：</strong></p>
                <ul>
                  <li><strong>了解自己</strong>：认识自己的优势和不足</li>
                  <li><strong>把握时机</strong>：在运势好的时候积极进取</li>
                  <li><strong>规避风险</strong>：在运势不佳时谨慎行事</li>
                  <li><strong>调整心态</strong>：以更积极的心态面对人生</li>
                </ul>
                <p><strong>记住：</strong>命运掌握在自己手中，努力奋斗、积极向上才是改变命运的最佳途径。</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </section>

        <!-- 使用指南 -->
        <section class="faq-section">
          <h3>📖 使用指南</h3>
          <el-collapse v-model="activeGuide">
            <el-collapse-item name="1" title="1. 如何使用追加提问功能？">
              <div class="faq-answer">
                <p>每次命理分析包含<strong>3次免费追加提问</strong>机会：</p>
                <ol>
                  <li>在分析报告页面找到"追加提问"区域</li>
                  <li>输入您关心的具体问题</li>
                  <li>点击"提交问题"按钮</li>
                  <li>等待AI大师回答（通常1-2分钟）</li>
                </ol>
                <p><strong>提问建议：</strong></p>
                <ul>
                  <li>问题要具体明确，如"我今年适合换工作吗？"</li>
                  <li>避免过于宽泛的问题，如"我的命运怎么样？"</li>
                  <li>可以问事业、感情、健康等具体方面</li>
                </ul>
              </div>
            </el-collapse-item>

            <el-collapse-item name="2" title="2. 如何保存或分享分析报告？">
              <div class="faq-answer">
                <p>您可以通过以下方式保存或分享报告：</p>
                <ul>
                  <li><strong>截图保存</strong>：直接截屏保存到手机相册</li>
                  <li><strong>下载报告</strong>：点击"下载报告"按钮（开发中）</li>
                  <li><strong>分享链接</strong>：点击"分享报告"生成专属链接</li>
                  <li><strong>收藏页面</strong>：将页面添加到浏览器收藏夹</li>
                </ul>
                <p><strong>注意：</strong>分享时请注意保护个人隐私。</p>
              </div>
            </el-collapse-item>

            <el-collapse-item name="3" title="3. 可以多次测算吗？">
              <div class="faq-answer">
                <p><strong>当然可以！</strong>您可以：</p>
                <ul>
                  <li>为不同的人生阶段进行测算</li>
                  <li>为家人朋友进行测算（需要他们的出生信息）</li>
                  <li>对比不同时间的运势变化</li>
                </ul>
                <p>每次测算都是独立的，需要重新支付10元费用。</p>
                <p><strong>温馨提示：</strong>命理分析仅供参考，请勿过度依赖或频繁测算。</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </section>
      </div>

      <!-- 更多问题 -->
      <div class="more-questions">
        <h3>😊 还有其他问题？</h3>
        <p>如果这里没有找到您想要的答案，欢迎通过以下方式联系我们：</p>
        <div class="contact-methods">
          <div class="contact-method">
            <div class="method-icon">📧</div>
            <div class="method-info">
              <h4>邮箱</h4>
              <p>contact@destiny.com</p>
              <p class="method-desc">24小时内回复</p>
            </div>
          </div>
          <div class="contact-method">
            <div class="method-icon">💬</div>
            <div class="method-info">
              <h4>微信客服</h4>
              <p>DestinyService</p>
              <p class="method-desc">工作日9:00-18:00在线</p>
            </div>
          </div>
          <div class="contact-method">
            <div class="method-icon">📱</div>
            <div class="method-info">
              <h4>在线留言</h4>
              <p>在"关于我们"页面留言</p>
              <p class="method-desc">我们会尽快回复</p>
            </div>
          </div>
        </div>
      </div>

      <div class="back-home">
        <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
        <el-button @click="$router.push('/service')">立即测算</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeService = ref(['1'])
const activeTech = ref(['1'])
const activeKnowledge = ref(['1'])
const activeGuide = ref(['1'])
</script>

<style scoped>
.faq {
  padding: 40px 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.faq-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.faq-title {
  text-align: center;
  font-size: 36px;
  color: #333;
  margin-bottom: 10px;
}

.faq-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 40px;
}

.faq-section {
  margin-bottom: 40px;
}

.faq-section h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #667eea;
}

.faq-answer {
  padding: 10px 0;
}

.faq-answer p {
  line-height: 1.6;
  color: #555;
  margin-bottom: 10px;
}

.faq-answer ul, .faq-answer ol {
  padding-left: 20px;
  margin: 10px 0;
}

.faq-answer li {
  line-height: 1.6;
  color: #555;
  margin-bottom: 5px;
}

.faq-answer strong {
  color: #333;
}

.more-questions {
  margin-top: 50px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

.more-questions h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 15px;
}

.more-questions p {
  color: #666;
  margin-bottom: 30px;
}

.contact-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.contact-method {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 15px;
  border: 1px solid #e9ecef;
}

.method-icon {
  font-size: 40px;
}

.method-info h4 {
  color: #333;
  margin-bottom: 5px;
  font-size: 18px;
}

.method-info p {
  color: #666;
  margin-bottom: 5px;
  font-size: 14px;
}

.method-desc {
  color: #888;
  font-size: 12px;
}

.back-home {
  text-align: center;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
  gap: 20px;
}

@media (max-width: 768px) {
  .faq-container {
    padding: 20px;
  }
  
  .faq-title {
    font-size: 28px;
  }
  
  .contact-methods {
    grid-template-columns: 1fr;
  }
  
  .back-home {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
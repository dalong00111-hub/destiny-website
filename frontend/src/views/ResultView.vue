<template>
  <div class="result">
    <div class="result-container">
      <!-- 结果头部 -->
      <div class="result-header">
        <h2 class="result-title">🎉 您的命理分析报告已生成</h2>
        <p class="result-subtitle">基于您的生辰八字，AI大师为您深度解读</p>
        <div class="result-meta">
          <div class="meta-item">
            <span class="meta-label">分析时间：</span>
            <span class="meta-value">{{ currentTime }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">报告编号：</span>
            <span class="meta-value">{{ reportId }}</span>
          </div>
        </div>
      </div>

      <!-- 八字信息 -->
      <div class="bazi-section">
        <h3 class="section-title">📜 您的八字信息</h3>
        <div class="bazi-grid">
          <div class="bazi-item" v-for="(item, index) in baziInfo" :key="index">
            <div class="bazi-label">{{ item.label }}</div>
            <div class="bazi-value">{{ item.value }}</div>
            <div class="bazi-desc">{{ item.desc }}</div>
          </div>
        </div>
      </div>

      <!-- 命理分析 -->
      <div class="analysis-section">
        <h3 class="section-title">🔮 命理深度分析</h3>
        
        <div class="analysis-tabs">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="性格特点" name="personality">
              <div class="tab-content">
                <h4>您的性格特征：</h4>
                <p>{{ analysis.personality }}</p>
                
                <div class="strengths-weaknesses">
                  <div class="strengths">
                    <h5>👍 优势特质</h5>
                    <ul>
                      <li v-for="(strength, index) in analysis.strengths" :key="index">{{ strength }}</li>
                    </ul>
                  </div>
                  <div class="weaknesses">
                    <h5>👎 需要注意</h5>
                    <ul>
                      <li v-for="(weakness, index) in analysis.weaknesses" :key="index">{{ weakness }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="事业财运" name="career">
              <div class="tab-content">
                <h4>事业发展建议：</h4>
                <p>{{ analysis.career }}</p>
                
                <div class="career-tips">
                  <h5>💼 适合行业</h5>
                  <div class="tags">
                    <span class="tag" v-for="(industry, index) in analysis.industries" :key="index">{{ industry }}</span>
                  </div>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="感情婚姻" name="relationship">
              <div class="tab-content">
                <h4>感情婚姻分析：</h4>
                <p>{{ analysis.relationship }}</p>
                
                <div class="relationship-tips">
                  <h5>❤️ 感情建议</h5>
                  <ul>
                    <li v-for="(tip, index) in analysis.relationshipTips" :key="index">{{ tip }}</li>
                  </ul>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="健康运势" name="health">
              <div class="tab-content">
                <h4>健康运势分析：</h4>
                <p>{{ analysis.health }}</p>
                
                <div class="health-tips">
                  <h5>🏥 健康建议</h5>
                  <ul>
                    <li v-for="(tip, index) in analysis.healthTips" :key="index">{{ tip }}</li>
                  </ul>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <!-- 运势预测 -->
      <div class="fortune-section">
        <h3 class="section-title">📅 近期运势预测</h3>
        <div class="fortune-cards">
          <div class="fortune-card" v-for="(fortune, index) in fortunes" :key="index">
            <div class="fortune-period">{{ fortune.period }}</div>
            <div :class="['fortune-level', fortune.level]">{{ fortune.levelText }}</div>
            <div class="fortune-desc">{{ fortune.desc }}</div>
            <div class="fortune-tip">{{ fortune.tip }}</div>
          </div>
        </div>
      </div>

      <!-- 追加提问 -->
      <div class="qa-section">
        <h3 class="section-title">❓ 追加提问（剩余 {{ remainingQuestions }} 次）</h3>
        <p class="section-subtitle">您可以继续提问3个具体问题，AI大师将为您详细解答</p>
        
        <div class="qa-list">
          <div class="qa-item" v-for="(qa, index) in questions" :key="index">
            <div class="question">
              <strong>Q{{ index + 1 }}：</strong>{{ qa.question }}
            </div>
            <div class="answer" v-if="qa.answer">
              <strong>A：</strong>{{ qa.answer }}
            </div>
            <div class="answer-placeholder" v-else>
              等待AI大师回答...
            </div>
          </div>
        </div>

        <div class="new-question" v-if="remainingQuestions > 0">
          <el-input
            v-model="newQuestion"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题，例如：我今年适合换工作吗？"
            maxlength="200"
            show-word-limit
          />
          <div class="question-actions">
            <el-button @click="clearQuestion">清空</el-button>
            <el-button 
              type="primary" 
              @click="submitQuestion"
              :loading="submittingQuestion"
              :disabled="!newQuestion.trim()"
            >
              提交问题
            </el-button>
          </div>
        </div>

        <div class="no-questions" v-else>
          <p>您的提问次数已用完，如需更多咨询，请重新下单。</p>
          <el-button type="primary" @click="$router.push('/service')">再次测算</el-button>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button @click="$router.push('/')">返回首页</el-button>
        <el-button @click="downloadReport">下载报告</el-button>
        <el-button type="primary" @click="shareReport">分享报告</el-button>
        <el-button type="success" @click="$router.push('/service')">再次测算</el-button>
      </div>

      <!-- 免责声明 -->
      <div class="disclaimer">
        <h4>📝 免责声明</h4>
        <p>本命理分析报告基于传统八字命理算法生成，仅供娱乐参考。命运掌握在自己手中，努力奋斗才是改变命运的最佳途径。请勿将分析结果作为重要决策的唯一依据。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { api } from '../utils/api'

const router = useRouter()
const currentTime = ref('')
const reportId = ref('')
const activeTab = ref('personality')
const newQuestion = ref('')
const submittingQuestion = ref(false)

// 从localStorage加载分析结果
const analysisData = ref<any>(null)
const baziInfo = ref<any[]>([])
const analysis = ref<any>({})
const fortunes = ref<any[]>([])
const questions = ref<any[]>([])

// 生成报告ID
const generateReportId = () => {
  const timestamp = Date.now()
  const random = Math.floor(Math.random() * 10000)
  return `DESTINY-${timestamp}-${random}`
}

// 八字信息
const baziInfo = reactive([
  { label: '年柱', value: '甲子', desc: '木鼠之年' },
  { label: '月柱', value: '乙丑', desc: '木牛之月' },
  { label: '日柱', value: '丙寅', desc: '火虎之日' },
  { label: '时柱', value: '丁卯', desc: '火兔之时' },
  { label: '五行', value: '木火旺', desc: '缺金水土' },
  { label: '十神', value: '正印偏财', desc: '聪明重情' }
])

// 命理分析数据
const analysis = reactive({
  personality: '您性格外向开朗，思维敏捷，富有创造力。做事积极主动，但有时容易冲动，需要学会三思而后行。',
  strengths: [
    '领导能力强，善于组织协调',
    '学习能力强，适应环境快',
    '富有同情心，人际关系好',
    '执行力强，说到做到'
  ],
  weaknesses: [
    '有时过于自信，需要听取他人意见',
    '情绪波动较大，需要学会控制',
    '做事容易虎头蛇尾，需要坚持',
    '对细节关注不够，需要更细心'
  ],
  career: '您适合从事需要创意和沟通的工作，如媒体、教育、咨询等行业。中年后事业运逐渐上升，45岁左右可能达到事业高峰。',
  industries: ['教育培训', '文化传媒', '市场营销', '咨询服务', '创意设计'],
  relationship: '您感情丰富，重视家庭，但有时过于理想化。适合找性格稳重、能包容您的伴侣。婚姻运势较好，但需要多沟通。',
  relationshipTips: [
    '多关注伴侣感受，学会换位思考',
    '避免因工作忙碌而忽略家庭',
    '培养共同兴趣爱好',
    '定期进行深度沟通'
  ],
  health: '您身体素质较好，但需要注意消化系统和神经系统。建议规律作息，适当运动，避免过度劳累。',
  healthTips: [
    '每天保证7-8小时睡眠',
    '饮食清淡，少食辛辣',
    '每周至少运动3次',
    '学会放松，避免压力过大'
  ]
})

// 运势预测
const fortunes = reactive([
  {
    period: '本月运势',
    level: 'good',
    levelText: '★★★★☆',
    desc: '事业上有新机会，财运平稳上升',
    tip: '适合拓展人脉，注意把握机会'
  },
  {
    period: '下月运势',
    level: 'normal',
    levelText: '★★★☆☆',
    desc: '工作压力增大，需要调整心态',
    tip: '注意劳逸结合，避免过度劳累'
  },
  {
    period: '本季度',
    level: 'excellent',
    levelText: '★★★★★',
    desc: '整体运势上升，可能有重要突破',
    tip: '大胆尝试新事物，会有意外收获'
  }
])

// 问题列表
const questions = reactive([
  { question: '', answer: '' },
  { question: '', answer: '' },
  { question: '', answer: '' }
])

const remainingQuestions = computed(() => {
  return questions.filter(q => !q.question).length
})

const submitQuestion = async () => {
  if (!newQuestion.value.trim()) {
    ElMessage.warning('请输入问题内容')
    return
  }

  const orderId = localStorage.getItem('current_order_id')
  if (!orderId) {
    ElMessage.error('未找到订单信息')
    return
  }

  submittingQuestion.value = true

  try {
    const result = await api.askQuestion(orderId, newQuestion.value)
    if (result.success) {
      ElMessage.success('问题已回答')
      newQuestion.value = ''
      
      // 重新加载问题列表
      await loadQuestions(orderId)
    } else {
      ElMessage.error(result.error || '提问失败')
    }
  } catch (error) {
    ElMessage.error('提问失败，请重试')
  } finally {
    submittingQuestion.value = false
  }
}

const clearQuestion = () => {
  newQuestion.value = ''
}

const downloadReport = () => {
  ElMessage.success('报告下载功能开发中...')
  // 实际应该生成PDF并下载
}

const shareReport = () => {
  ElMessage.success('分享功能开发中...')
  // 实际应该生成分享链接
}

onMounted(async () => {
  // 设置当前时间
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })

  // 生成报告ID
  reportId.value = generateReportId()
  
  // 从localStorage加载分析结果
  const savedAnalysis = localStorage.getItem('analysis_result')
  if (savedAnalysis) {
    try {
      analysisData.value = JSON.parse(savedAnalysis)
      loadAnalysisData(analysisData.value)
    } catch (error) {
      ElMessage.error('加载分析结果失败')
      router.push('/')
    }
  } else {
    ElMessage.warning('未找到分析结果，请重新测算')
    router.push('/service')
  }
})

const loadAnalysisData = (data: any) => {
  // 加载八字信息
  if (data.analysis?.bazi_display) {
    const baziParts = data.analysis.bazi_display.split(' ')
    baziInfo.value = [
      { label: '年柱', value: baziParts[0], desc: getBaziDesc(baziParts[0]) },
      { label: '月柱', value: baziParts[1], desc: getBaziDesc(baziParts[1]) },
      { label: '日柱', value: baziParts[2], desc: getBaziDesc(baziParts[2]) },
      { label: '时柱', value: baziParts[3], desc: getBaziDesc(baziParts[3]) },
      { label: '五行', value: '木火旺', desc: '缺金水土' },
      { label: '十神', value: '正印偏财', desc: '聪明重情' }
    ]
  }
  
  // 加载分析内容
  analysis.value = data.analysis || {}
  
  // 加载运势
  fortunes.value = data.analysis?.fortunes || []
  
  // 加载问题
  const orderId = localStorage.getItem('current_order_id')
  if (orderId) {
    loadQuestions(orderId)
  }
}

const getBaziDesc = (bazi: string) => {
  // 简化的八字描述
  const descMap: Record<string, string> = {
    '甲子': '木鼠之年', '乙丑': '木牛之月', '丙寅': '火虎之日', '丁卯': '火兔之时',
    '戊辰': '土龙之年', '己巳': '土蛇之月', '庚午': '金马之日', '辛未': '金羊之时',
    '壬申': '水猴之年', '癸酉': '水鸡之月', '甲戌': '木狗之日', '乙亥': '木猪之时'
  }
  return descMap[bazi] || '命理分析'
}

const loadQuestions = async (orderId: string) => {
  try {
    const result = await api.getQuestions(orderId)
    if (result.success && result.data?.questions) {
      questions.value = result.data.questions
    }
  } catch (error) {
    console.error('加载问题失败:', error)
  }
}
</script>

<style scoped>
.result {
  padding: 40px 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.result-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.result-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #eee;
}

.result-title {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
}

.result-subtitle {
  color: #666;
  font-size: 16px;
  margin-bottom: 20px;
}

.result-meta {
  display: flex;
  justify-content: center;
  gap: 30px;
  font-size: 14px;
  color: #888;
}

.meta-label {
  font-weight: bold;
}

.section-title {
  font-size: 24px;
  color: #333;
  margin: 40px 0 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #667eea;
}

.section-subtitle {
  color: #666;
  margin-bottom: 20px;
}

.bazi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.bazi-item {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  border: 1px solid #e9ecef;
}

.bazi-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.bazi-value {
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 5px;
}

.bazi-desc {
  font-size: 12px;
  color: #888;
}

.analysis-tabs {
  margin: 30px 0;
}

.tab-content {
  padding: 20px;
}

.tab-content h4 {
  color: #333;
  margin-bottom: 15px;
  font-size: 18px;
}

.tab-content p {
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
}

.strengths-weaknesses {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-top: 20px;
}

.strengths h5, .weaknesses h5 {
  color: #333;
  margin-bottom: 10px;
  font-size: 16px;
}

.strengths ul, .weaknesses ul {
  padding-left: 20px;
}

.strengths li {
  color: #28a745;
}

.weaknesses li {
  color: #dc3545;
}

.career-tips, .relationship-tips, .health-tips {
  margin-top: 20px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.tag {
  background: #e9ecef;
  padding: 5px 15px;
  border-radius: 15px;
  font-size: 14px;
  color: #495057;
}

.fortune-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.fortune-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease;
}

.fortune-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.fortune-period {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.fortune-level {
  font-size: 24px;
  margin-bottom: 10px;
}

.fortune-level.good {
  color: #28a745;
}

.fortune-level.normal {
  color: #ffc107;
}

.fortune-level.excellent {
  color: #dc3545;
}

.fortune-desc {
  color: #555;
  margin-bottom: 10px;
  line-height: 1.4;
}

.fortune-tip {
  font-size: 12px;
  color: #888;
  font-style
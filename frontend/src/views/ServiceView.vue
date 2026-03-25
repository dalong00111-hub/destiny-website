<template>
  <div class="service">
    <div class="service-container">
      <!-- 步骤指示器 -->
      <div class="steps">
        <div :class="['step', { active: currentStep >= 1 }]">
          <div class="step-circle">1</div>
          <div class="step-label">输入生辰</div>
        </div>
        <div class="step-line"></div>
        <div :class="['step', { active: currentStep >= 2 }]">
          <div class="step-circle">2</div>
          <div class="step-label">支付费用</div>
        </div>
        <div class="step-line"></div>
        <div :class="['step', { active: currentStep >= 3 }]">
          <div class="step-circle">3</div>
          <div class="step-label">查看结果</div>
        </div>
      </div>

      <!-- 步骤1：输入生辰 -->
      <div v-if="currentStep === 1" class="step-content">
        <h2 class="step-title">📅 请输入您的生辰八字</h2>
        <p class="step-description">准确的出生时间能获得更精准的分析结果</p>
        
        <el-form 
          ref="birthForm" 
          :model="birthData" 
          :rules="birthRules" 
          label-width="120px"
          class="birth-form"
        >
          <el-form-item label="出生年份" prop="year">
            <el-select v-model="birthData.year" placeholder="请选择年份" style="width: 100%">
              <el-option 
                v-for="year in years" 
                :key="year" 
                :label="`${year}年`" 
                :value="year"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="出生月份" prop="month">
            <el-select v-model="birthData.month" placeholder="请选择月份" style="width: 100%">
              <el-option 
                v-for="month in months" 
                :key="month.value" 
                :label="month.label" 
                :value="month.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="出生日期" prop="day">
            <el-select v-model="birthData.day" placeholder="请选择日期" style="width: 100%">
              <el-option 
                v-for="day in days" 
                :key="day" 
                :label="`${day}日`" 
                :value="day"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="出生时辰" prop="hour">
            <el-select v-model="birthData.hour" placeholder="请选择时辰" style="width: 100%">
              <el-option 
                v-for="hour in hours" 
                :key="hour.value" 
                :label="hour.label" 
                :value="hour.value"
              />
            </el-select>
            <div class="hour-tip">古代时辰对应现代时间：子时(23-1)、丑时(1-3)...</div>
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="birthData.gender">
              <el-radio label="male">男</el-radio>
              <el-radio label="female">女</el-radio>
            </el-radio-group>
          </el-form-item>

          <div class="form-actions">
            <el-button @click="$router.push('/')">返回首页</el-button>
            <el-button 
              type="primary" 
              @click="handleNextStep"
              :loading="loading"
            >
              下一步：支付10元
            </el-button>
          </div>
        </el-form>
      </div>

      <!-- 步骤2：支付 -->
      <div v-else-if="currentStep === 2" class="step-content">
        <h2 class="step-title">💰 支付费用</h2>
        <p class="step-description">支付成功后立即生成命理分析报告</p>
        
        <div class="payment-info">
          <div class="price-card">
            <div class="price">10元</div>
            <div class="price-desc">单次命理分析</div>
          </div>

          <div class="payment-methods">
            <h3>选择支付方式</h3>
            <div class="methods">
              <div 
                :class="['method', { active: paymentMethod === 'wechat' }]"
                @click="paymentMethod = 'wechat'"
              >
                <div class="method-icon">💳</div>
                <div class="method-name">微信支付</div>
              </div>
              <div 
                :class="['method', { active: paymentMethod === 'alipay' }]"
                @click="paymentMethod = 'alipay'"
              >
                <div class="method-icon">💰</div>
                <div class="method-name">支付宝</div>
              </div>
            </div>

            <div class="payment-qrcode" v-if="paymentMethod">
              <div class="qrcode-placeholder">
                <div class="qrcode-text">扫码支付10元</div>
                <div class="qrcode-demo">
                  <!-- 这里应该是真实的二维码 -->
                  <div class="demo-qr">[二维码区域]</div>
                </div>
                <div class="payment-tip">请使用{{ paymentMethod === 'wechat' ? '微信' : '支付宝' }}扫描二维码</div>
              </div>
            </div>

            <div class="payment-actions">
              <el-button @click="currentStep = 1">上一步</el-button>
              <el-button 
                type="primary" 
                @click="simulatePayment"
                :loading="paymentLoading"
              >
                我已支付完成
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 步骤3：加载中 -->
      <div v-else-if="currentStep === 3" class="step-content">
        <h2 class="step-title">🔮 正在生成命理分析报告</h2>
        <p class="step-description">AI大师正在为您分析八字命理...</p>
        
        <div class="loading-container">
          <div class="loading-spinner"></div>
          <div class="loading-text">
            <p>正在分析：{{ loadingProgress }}%</p>
            <p class="loading-tip">{{ loadingTips[currentTip] }}</p>
          </div>
        </div>

        <div class="loading-actions">
          <el-button @click="currentStep = 2">返回支付</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const currentStep = ref(1)
const loading = ref(false)
const paymentLoading = ref(false)
const paymentMethod = ref('')
const loadingProgress = ref(0)
const currentTip = ref(0)

const birthForm = ref<FormInstance>()

const birthData = reactive({
  year: '',
  month: '',
  day: '',
  hour: '',
  gender: 'male'
})

const birthRules = {
  year: [{ required: true, message: '请选择出生年份', trigger: 'change' }],
  month: [{ required: true, message: '请选择出生月份', trigger: 'change' }],
  day: [{ required: true, message: '请选择出生日期', trigger: 'change' }],
  hour: [{ required: true, message: '请选择出生时辰', trigger: 'change' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
}

// 生成年份选项（1900-2026）
const years = computed(() => {
  const currentYear = new Date().getFullYear()
  const years = []
  for (let i = currentYear; i >= 1900; i--) {
    years.push(i)
  }
  return years
})

// 月份选项
const months = [
  { label: '一月', value: 1 }, { label: '二月', value: 2 },
  { label: '三月', value: 3 }, { label: '四月', value: 4 },
  { label: '五月', value: 5 }, { label: '六月', value: 6 },
  { label: '七月', value: 7 }, { label: '八月', value: 8 },
  { label: '九月', value: 9 }, { label: '十月', value: 10 },
  { label: '十一月', value: 11 }, { label: '十二月', value: 12 }
]

// 日期选项（根据月份动态生成）
const days = computed(() => {
  if (!birthData.year || !birthData.month) return Array.from({ length: 31 }, (_, i) => i + 1)
  
  const year = parseInt(birthData.year)
  const month = parseInt(birthData.month)
  const daysInMonth = new Date(year, month, 0).getDate()
  return Array.from({ length: daysInMonth }, (_, i) => i + 1)
})

// 时辰选项
const hours = [
  { label: '子时 (23:00-01:00)', value: 0 },
  { label: '丑时 (01:00-03:00)', value: 1 },
  { label: '寅时 (03:00-05:00)', value: 2 },
  { label: '卯时 (05:00-07:00)', value: 3 },
  { label: '辰时 (07:00-09:00)', value: 4 },
  { label: '巳时 (09:00-11:00)', value: 5 },
  { label: '午时 (11:00-13:00)', value: 6 },
  { label: '未时 (13:00-15:00)', value: 7 },
  { label: '申时 (15:00-17:00)', value: 8 },
  { label: '酉时 (17:00-19:00)', value: 9 },
  { label: '戌时 (19:00-21:00)', value: 10 },
  { label: '亥时 (21:00-23:00)', value: 11 }
]

// 加载提示语
const loadingTips = [
  '正在排定八字...',
  '分析天干地支关系...',
  '计算五行强弱...',
  '解读十神含义...',
  '生成命理建议...',
  '优化分析报告...'
]

import { api } from '../utils/api'

const handleNextStep = async () => {
  if (!birthForm.value) return
  
  try {
    await birthForm.value.validate()
    loading.value = true
    
    // 1. 初始化用户
    const userResult = await api.initUser()
    if (!userResult.success) {
      throw new Error(userResult.error || '用户初始化失败')
    }
    
    const userId = userResult.data?.user_id
    if (!userId) {
      throw new Error('未获取到用户ID')
    }
    
    // 2. 创建订单
    const orderResult = await api.createOrder(userId, {
      year: parseInt(birthData.year),
      month: parseInt(birthData.month),
      day: parseInt(birthData.day),
      hour: parseInt(birthData.hour),
      gender: birthData.gender
    })
    
    if (!orderResult.success) {
      throw new Error(orderResult.error || '订单创建失败')
    }
    
    const orderId = orderResult.data?.order_id
    if (!orderId) {
      throw new Error('未获取到订单ID')
    }
    
    // 保存订单信息
    localStorage.setItem('current_order_id', orderId)
    localStorage.setItem('current_user_id', userId)
    
    loading.value = false
    currentStep.value = 2
    ElMessage.success('生辰信息提交成功，请完成支付')
  } catch (error) {
    loading.value = false
    ElMessage.error(error instanceof Error ? error.message : '提交失败，请重试')
  }
}

const simulatePayment = async () => {
  paymentLoading.value = true
  
  try {
    const orderId = localStorage.getItem('current_order_id')
    if (!orderId) {
      throw new Error('未找到订单信息')
    }
    
    // 完成订单（模拟支付）
    const result = await api.completeOrder(orderId)
    if (!result.success) {
      throw new Error(result.error || '支付失败')
    }
    
    paymentLoading.value = false
    currentStep.value = 3
    startLoadingAnimation()
  } catch (error) {
    paymentLoading.value = false
    ElMessage.error(error instanceof Error ? error.message : '支付失败，请重试')
  }
}

const startLoadingAnimation = async () => {
  let progress = 0
  const orderId = localStorage.getItem('current_order_id')
  
  if (!orderId) {
    ElMessage.error('未找到订单信息')
    return
  }
  
  const interval = setInterval(async () => {
    progress += Math.random() * 10
    loadingProgress.value = Math.min(progress, 100)
    
    // 切换提示语
    if (progress % 20 < 10) {
      currentTip.value = Math.floor(progress / 20) % loadingTips.length
    }
    
    if (progress >= 100) {
      clearInterval(interval)
      loadingProgress.value = 100
      
      try {
        // 获取分析结果
        const result = await api.getAnalysis(orderId)
        if (result.success) {
          // 保存分析结果
          localStorage.setItem('analysis_result', JSON.stringify(result.data))
          ElMessage.success('命理分析完成！')
          
          // 跳转到结果页面
          setTimeout(() => {
            router.push('/result')
          }, 1000)
        } else {
          ElMessage.error(result.error || '分析生成失败')
        }
      } catch (error) {
        ElMessage.error('获取分析结果失败')
      }
    }
  }, 300)
}

onMounted(() => {
  // 设置默认年份为1990
  birthData.year = '1990'
})
</script>

<style scoped>
.service {
  padding: 40px 20px;
  max-width: 800px;
  margin: 0 auto;
}

.service-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 50px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.step-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e0e0e0;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.step.active .step-circle {
  background: #667eea;
  color: white;
}

.step-label {
  margin-top: 10px;
  color: #999;
  font-size: 14px;
}

.step.active .step-label {
  color: #667eea;
  font-weight: bold;
}

.step-line {
  width: 100px;
  height: 2px;
  background: #e0e0e0;
  margin: 0 20px;
}

.step-content {
  min-height: 400px;
}

.step-title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 10px;
  color: #333;
}

.step-description {
  text-align: center;
  color: #666;
  margin-bottom: 40px;
}

.birth-form {
  max-width: 500px;
  margin: 0 auto;
}

.hour-tip {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.payment-info {
  text-align: center;
}

.price-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 40px;
  display: inline-block;
}

.price {
  font-size: 48px;
  font-weight: bold;
}

.price-desc {
  font-size: 16px;
  opacity: 0.9;
}

.payment-methods {
  margin-top: 40px;
}

.payment-methods h3 {
  margin-bottom: 20px;
  color: #333;
}

.methods {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 40px;
}

.method {
  padding: 20px 40px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  min-width: 150px;
}

.method:hover {
  border-color: #667eea;
}

.method.active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.method-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.method-name {
  font-size: 16px;
  font-weight: bold;
}

.payment-qrcode {
  margin: 40px auto;
  max-width: 300px;
}

.qrcode-placeholder {
  padding: 30px;
  border: 2px dashed #e0e0e0;
  border-radius: 10px;
}

.qrcode-text {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.demo-qr {
  width: 200px;
  height: 200px;
  background: #f5f5f5;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  border-radius: 5px;
}

.payment-tip {
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.payment-actions {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.loading-container {
  text-align: center;
  padding: 60px 0;
}

.loading-spinner {
  width: 80px;
  height: 80px;
  border: 8px solid #f3f3f3;
  border-top: 8px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 30px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text p {
  font-size: 18px;
  margin: 10px 0;
  color: #333;
}

.loading-tip {
  color: #666;
  font-size: 14px;
  font-style: italic;
}

.loading-actions {
  margin-top: 40px;
  text-align: center;
}

@media (max-width: 768px) {
  .service-container {
    padding: 20px
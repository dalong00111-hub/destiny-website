// API基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    const data = await response.json()
    
    if (!response.ok) {
      return {
        success: false,
        error: data.error || `HTTP ${response.status}`,
        message: data.message,
      }
    }

    return {
      success: true,
      data: data,
      message: data.message,
    }
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : '网络请求失败',
    }
  }
}

// 具体的API方法
export const api = {
  // 健康检查
  healthCheck: () => apiRequest('/api/health'),
  
  // 用户相关
  initUser: () => apiRequest('/api/init-user', { method: 'POST' }),
  
  // 订单相关
  createOrder: (user_id: string, birth_data: any) => 
    apiRequest('/api/create-order', {
      method: 'POST',
      body: JSON.stringify({ user_id, birth_data }),
    }),
  
  completeOrder: (order_id: string) =>
    apiRequest('/api/complete-order', {
      method: 'POST',
      body: JSON.stringify({ order_id }),
    }),
  
  getAnalysis: (order_id: string) =>
    apiRequest(`/api/get-analysis/${order_id}`),
  
  // 问题相关
  askQuestion: (order_id: string, question: string) =>
    apiRequest('/api/ask-question', {
      method: 'POST',
      body: JSON.stringify({ order_id, question }),
    }),
  
  getQuestions: (order_id: string) =>
    apiRequest(`/api/get-questions/${order_id}`),
}
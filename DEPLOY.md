# 🚀 命运预测网站部署指南

## 部署到公网（免费方案）

### 方案：Vercel（前端）+ Railway（后端）

#### 优点：
- 完全免费（有一定限制）
- 自动SSL证书
- 全球CDN加速
- 自动部署

---

## 第1步：部署后端到 Railway

### 1.1 注册 Railway
1. 访问 https://railway.app
2. 使用GitHub账号登录
3. 点击"New Project"

### 1.2 部署后端
1. 选择"Deploy from GitHub repo"
2. 选择你的仓库（或fork我的仓库）
3. 选择`backend`目录
4. Railway会自动检测并部署

### 1.3 获取后端URL
部署完成后，Railway会提供一个URL，例如：
```
https://destiny-backend-production.up.railway.app
```

记下这个URL，后面部署前端时需要。

---

## 第2步：部署前端到 Vercel

### 2.1 注册 Vercel
1. 访问 https://vercel.com
2. 使用GitHub账号登录
3. 点击"New Project"

### 2.2 部署前端
1. 导入你的GitHub仓库
2. 在配置中：
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: frontend/dist
3. 点击"Deploy"

### 2.3 配置环境变量
在Vercel项目设置中，添加环境变量：
```
VITE_API_BASE_URL=https://你的railway后端地址
```

### 2.4 获取前端URL
部署完成后，Vercel会提供一个URL，例如：
```
https://destiny-website.vercel.app
```

这就是你的网站地址！

---

## 第3步：配置域名（可选但推荐）

### 3.1 购买域名
推荐在以下平台购买：
- Namecheap
- GoDaddy
- 阿里云
- 腾讯云

### 3.2 在Vercel绑定域名
1. 进入Vercel项目设置
2. 选择"Domains"
3. 添加你的域名
4. 按照提示配置DNS

### 3.3 在Railway绑定域名（后端）
1. 进入Railway项目设置
2. 选择"Domains"
3. 添加子域名，如：`api.你的域名.com`
4. 配置DNS记录

---

## 第4步：测试部署

### 4.1 测试后端API
```
curl https://你的后端地址/api/health
```
应该返回：
```json
{"status": "healthy", "timestamp": "..."}
```

### 4.2 测试前端网站
1. 访问你的网站地址
2. 测试完整流程：
   - 输入生辰信息
   - 模拟支付
   - 查看分析结果
   - 测试提问功能

### 4.3 测试API连接
确保前端能正确连接到后端API。

---

## 第5步：配置真实支付（生产环境）

### 5.1 申请支付接口
1. **微信支付**：https://pay.weixin.qq.com
2. **支付宝**：https://open.alipay.com

### 5.2 修改后端代码
在`backend/app.py`中，修改支付相关代码：
```python
# 替换模拟支付为真实支付
# 需要集成微信/支付宝SDK
```

### 5.3 配置支付回调
1. 在支付平台配置回调URL
2. 在后端实现回调处理

---

## 第6步：监控和维护

### 6.1 监控服务状态
- **Vercel**：自带监控和日志
- **Railway**：自带监控和日志
- **第三方**：UptimeRobot, StatusCake

### 6.2 定期备份
- 数据库备份（Railway提供自动备份）
- 代码备份（GitHub）
- 配置文件备份

### 6.3 更新和维护
1. 定期更新依赖
2. 监控错误日志
3. 根据用户反馈优化

---

## 故障排除

### 问题1：前端无法连接后端
**解决**：
1. 检查环境变量`VITE_API_BASE_URL`
2. 检查CORS配置
3. 检查网络连接

### 问题2：数据库连接失败
**解决**：
1. 检查Railway环境变量
2. 检查数据库权限
3. 重启服务

### 问题3：支付功能异常
**解决**：
1. 检查支付接口配置
2. 检查回调URL
3. 查看支付平台日志

### 问题4：性能问题
**解决**：
1. 启用CDN缓存
2. 优化数据库查询
3. 使用缓存机制

---

## 安全建议

### 1. 数据安全
- 使用HTTPS
- 加密敏感数据
- 定期备份

### 2. 代码安全
- 不要提交敏感信息到Git
- 使用环境变量
- 定期更新依赖

### 3. 运营安全
- 监控异常访问
- 设置访问限制
- 准备应急预案

---

## 成本估算

### 免费方案
- **Vercel**：免费（每月100GB带宽）
- **Railway**：免费（每月5美元额度）
- **域名**：10-50元/年（可选）

### 付费方案（用户量增长后）
- **Vercel Pro**：20美元/月
- **Railway**：按使用量计费
- **CDN**：按流量计费

---

## 扩展建议

### 1. 增加功能
- 用户账户系统
- 更多命理算法
- 社区功能
- 移动APP

### 2. 优化体验
- 更快的加载速度
- 更好的移动端体验
- 多语言支持

### 3. 商业扩展
- VIP会员服务
- 命理课程
- 电商导流
- 广告收入

---

## 联系方式

如有部署问题，可以通过以下方式联系：

- **GitHub Issues**：提交问题
- **Email**：contact@destiny.com
- **微信**：DestinyService

---

## 更新日志

### v1.0 (2026-03-26)
- 初始版本发布
- 基础八字命理功能
- 模拟支付系统
- 响应式前端界面

### 后续计划
- 真实支付接口
- 更精准的八字算法
- 用户管理系统
- 数据分析后台
# 🔮 命运预测网站

**10元请大师回家 · 遇事不决，随时求解**

基于传统八字命理，结合现代AI技术，提供科学、便捷的命理分析服务。

## 🎯 核心功能

- **💰 10元一次**：价格亲民，人人可用
- **⚡ 即时分析**：支付后30秒内生成报告
- **🔮 八字命理**：基于传统八字算法
- **🤖 AI辅助**：智能回答用户问题
- **📱 响应式设计**：完美适配手机和电脑
- **🔒 隐私保护**：数据加密，安全可靠

## 🏗️ 技术架构

```
前端：Vue 3 + TypeScript + Element Plus
后端：Python Flask + SQLite
AI：OpenClaw Zero Token（免费）
部署：Vercel + Railway（免费托管）
```

## 🚀 快速开始

### 1. 环境要求
- Node.js 16+
- Python 3.8+
- npm 或 yarn

### 2. 安装依赖
```bash
# 一键安装
bash scripts/setup.sh

# 或手动安装
cd frontend && npm install
cd backend && pip install -r requirements.txt
```

### 3. 启动服务
```bash
# 一键启动
bash scripts/start.sh

# 或分别启动
# 后端：cd backend && python3 app.py
# 前端：cd frontend && npm run dev
```

### 4. 访问网站
- 前端界面：http://localhost:3000
- 后端API：http://localhost:5000
- API健康检查：http://localhost:5000/api/health

## 📁 项目结构

```
destiny-website/
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── views/        # 页面
│   │   ├── router/       # 路由
│   │   └── utils/        # 工具函数
│   ├── package.json
│   └── vite.config.ts
├── backend/              # 后端代码
│   ├── app.py           # 主应用
│   ├── requirements.txt # Python依赖
│   └── data/           # 数据库目录
├── scripts/             # 脚本文件
│   ├── setup.sh        # 安装脚本
│   └── start.sh        # 启动脚本
└── docs/               # 文档
```

## 🔧 API接口

### 健康检查
```
GET /api/health
```

### 用户相关
```
POST /api/init-user        # 初始化用户
POST /api/create-order     # 创建订单
POST /api/complete-order   # 完成订单
```

### 分析相关
```
GET  /api/get-analysis/:order_id    # 获取分析结果
POST /api/ask-question             # 提问问题
GET  /api/get-questions/:order_id  # 获取问题列表
```

## 🎨 页面说明

### 1. 首页 (`/`)
- 网站介绍和功能展示
- 服务流程说明
- 用户评价展示

### 2. 测算页面 (`/service`)
- 输入生辰八字信息
- 支付10元费用
- 生成分析报告

### 3. 结果页面 (`/result`)
- 八字信息展示
- 命理深度分析
- 运势预测
- 追加提问功能

### 4. 关于页面 (`/about`)
- 公司介绍
- 团队信息
- 联系方式

### 5. 常见问题 (`/faq`)
- 服务相关问题
- 技术相关问题
- 使用指南

## 💰 商业模式

### 收入来源
1. **单次测算**：10元/次
2. **追加提问**：免费3次，后续收费
3. **VIP服务**：99元/年无限问（规划中）
4. **深度报告**：199元/份（规划中）

### 成本控制
1. **技术成本**：使用免费开源技术
2. **服务器成本**：使用免费托管服务
3. **AI成本**：使用 OpenClaw Zero Token（免费）
4. **运营成本**：自动化运营，减少人力

## 🔒 安全与合规

### 数据安全
- 用户数据加密存储
- 不收集敏感个人信息
- 支持数据删除功能

### 法律合规
- 明确"仅供娱乐参考"声明
- 避免绝对化宣传用语
- 遵守相关法律法规

## 📈 发展计划

### 第一阶段（MVP）
- [x] 基础八字排盘功能
- [x] 在线支付集成
- [x] 响应式前端界面
- [x] 基础AI回答功能

### 第二阶段（优化）
- [ ] 更精准的八字算法
- [ ] 真实的支付接口
- [ ] 用户管理系统
- [ ] 数据分析后台

### 第三阶段（扩展）
- [ ] 多语言支持
- [ ] 移动APP
- [ ] 社区功能
- [ ] 电商导流

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

## 📞 联系方式

- 邮箱：contact@destiny.com
- 微信：DestinyService
- 工作时间：周一至周五 9:00-18:00

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

本网站提供的命理分析仅供娱乐参考，不构成任何决策建议。命运掌握在自己手中，努力奋斗才是改变命运的最佳途径。请勿沉迷命理分析，理性看待分析结果。
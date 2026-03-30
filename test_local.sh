#!/bin/bash
# 本地测试脚本

echo "🚀 命运预测网站 - 本地测试"
echo "="*50

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "1. 📦 检查依赖..."
if [ ! -f "backend/requirements.txt" ]; then
    echo -e "${YELLOW}⚠️  依赖文件不存在${NC}"
    exit 1
fi

echo "2. 🔧 创建测试环境变量..."
cat > backend/.env.test << 'EOF'
# 测试环境配置
PAYMENT_ENABLED=true
SANDBOX_MODE=true
DEBUG_MODE=true

# 微信支付测试配置
WECHAT_APP_ID=test_app_id
WECHAT_MCH_ID=test_mch_id
WECHAT_API_KEY=test_api_key

# 支付宝测试配置
ALIPAY_APP_ID=test_alipay_app_id
ALIPAY_PRIVATE_KEY=test_private_key
ALIPAY_PUBLIC_KEY=test_public_key

# 测试回调URL
NOTIFY_URL=http://localhost:5000/api/payment/notify
RETURN_URL=http://localhost:8080/payment/result

# 数据库
DATABASE_URL=sqlite:///data/test_destiny.db
SECRET_KEY=test_secret_key_123
EOF

echo -e "${GREEN}✅ 测试环境变量已创建${NC}"

echo ""
echo "3. 🗄️ 创建测试数据库..."
mkdir -p backend/data
if [ -f "backend/data/destiny.db" ]; then
    cp backend/data/destiny.db backend/data/test_destiny.db
    echo -e "${GREEN}✅ 测试数据库已创建${NC}"
else
    echo -e "${YELLOW}⚠️  原数据库不存在，将创建新数据库${NC}"
fi

echo ""
echo "4. 🧪 运行支付测试..."
cd backend && python3 test_payment.py

echo ""
echo "5. 🌐 启动本地服务器..."
echo "   后端：http://localhost:5000"
echo "   前端：http://localhost:8080"
echo ""
echo "启动命令："
echo "   后端：cd backend && python3 app.py"
echo "   前端：cd frontend && npm run dev"
echo ""
echo "6. 📋 测试API端点："
echo "   - 健康检查：curl http://localhost:5000/api/health"
echo "   - 支付配置：curl http://localhost:5000/api/payment/config"
echo "   - 创建订单："
echo "     curl -X POST http://localhost:5000/api/create-order \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"user_id\":\"test\",\"birth_data\":{\"year\":1990,\"month\":1,\"day\":1,\"hour\":0,\"gender\":\"male\"}}'"
echo ""
echo "="*50
echo "🎯 本地测试环境准备完成！"
echo ""
echo "下一步："
echo "1. 启动后端服务器"
echo "2. 启动前端开发服务器"
echo "3. 测试完整支付流程"
echo "4. 部署到生产环境"
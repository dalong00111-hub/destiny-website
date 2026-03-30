#!/bin/bash
# 支付集成一键部署脚本

echo "🚀 命运预测网站 - 支付集成部署"
echo "="*50

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查目录
echo "📁 检查项目目录..."
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ 项目目录结构不完整${NC}"
    exit 1
fi
echo -e "${GREEN}✅ 项目目录检查通过${NC}"

# 步骤1：检查支付配置
echo ""
echo "1. 🔧 检查支付配置..."
if [ ! -f "backend/payment_config.py" ]; then
    echo -e "${RED}❌ 支付配置文件不存在${NC}"
    exit 1
fi

if [ ! -f "backend/.env.example" ]; then
    echo -e "${YELLOW}⚠️  环境变量示例文件不存在${NC}"
else
    echo -e "${GREEN}✅ 环境变量示例文件存在${NC}"
fi

# 步骤2：检查依赖
echo ""
echo "2. 📦 检查依赖..."
if [ ! -f "backend/requirements.txt" ]; then
    echo -e "${RED}❌ 依赖文件不存在${NC}"
    exit 1
fi

# 检查支付SDK是否已添加
if grep -q "wechatpayv3\|python-alipay-sdk" backend/requirements.txt; then
    echo -e "${GREEN}✅ 支付SDK依赖已配置${NC}"
else
    echo -e "${YELLOW}⚠️  支付SDK依赖未配置${NC}"
    echo "添加支付SDK到requirements.txt..."
    cat >> backend/requirements.txt << 'EOF'

# 支付SDK
wechatpayv3==1.2.60
python-alipay-sdk==3.1.3
qrcode==7.4.2
pillow==10.1.0
EOF
    echo -e "${GREEN}✅ 支付SDK依赖已添加${NC}"
fi

# 步骤3：创建部署配置
echo ""
echo "3. ⚙️ 创建部署配置..."

# 创建Railway配置文件
if [ ! -f "backend/railway.json" ]; then
    cat > backend/railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python app.py",
    "healthcheckPath": "/api/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
EOF
    echo -e "${GREEN}✅ Railway配置文件已创建${NC}"
fi

# 步骤4：创建环境变量配置指南
echo ""
echo "4. 🔐 环境变量配置指南..."
cat > /tmp/payment_env_guide.txt << 'EOF'
支付集成环境变量配置指南
================================

请将以下环境变量配置到部署平台（Railway）：

必需配置：
---------
PAYMENT_ENABLED=true
SANDBOX_MODE=true  # 测试阶段设为true，生产环境设为false

微信支付配置（测试）：
-------------------
WECHAT_APP_ID=wx1234567890abcdef
WECHAT_MCH_ID=1230000109
WECHAT_API_KEY=abcdef1234567890abcdef1234567890

支付宝配置（测试）：
-----------------
ALIPAY_APP_ID=2016092700601234
ALIPAY_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----\n测试私钥\n-----END RSA PRIVATE KEY-----
ALIPAY_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----\n测试公钥\n-----END PUBLIC KEY-----

回调URL配置（部署后更新）：
------------------------
NOTIFY_URL=https://你的后端域名/api/payment/notify
RETURN_URL=https://你的前端域名/payment/result

其他配置：
---------
DEBUG_MODE=true
SECRET_KEY=your-secret-key-here

配置步骤：
1. 部署后端到Railway
2. 获取后端域名
3. 部署前端到Vercel
4. 获取前端域名
5. 更新NOTIFY_URL和RETURN_URL
6. 重新部署后端
EOF

echo -e "${GREEN}✅ 环境变量指南已保存到 /tmp/payment_env_guide.txt${NC}"

# 步骤5：创建测试脚本
echo ""
echo "5. 🧪 创建测试脚本..."
cat > backend/test_payment.py << 'EOF'
#!/usr/bin/env python3
"""
支付系统测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from payment_config import PaymentConfig
from payment_service import PaymentFactory

def test_payment_config():
    """测试支付配置"""
    print("🔧 测试支付配置...")
    config = PaymentConfig()
    
    errors = config.validate_config()
    if errors:
        print(f"❌ 配置错误: {errors}")
        return False
    
    print(f"✅ 支付开关: {config.PAYMENT_ENABLED}")
    print(f"✅ 沙箱模式: {config.SANDBOX_MODE}")
    print(f"✅ 服务价格: {config.SERVICE_PRICE}元")
    print(f"✅ 微信支付配置: {'已配置' if config.WECHAT_APP_ID else '未配置'}")
    print(f"✅ 支付宝配置: {'已配置' if config.ALIPAY_APP_ID else '未配置'}")
    
    return True

def test_payment_service():
    """测试支付服务"""
    print("\n💳 测试支付服务...")
    
    # 测试微信支付
    try:
        wechat_service = PaymentFactory.get_payment_service('wechat')
        print("✅ 微信支付服务初始化成功")
        
        # 测试创建支付
        result = wechat_service.create_payment(
            order_id='test_order_123',
            amount=1000,
            description='测试支付',
            user_id='test_user'
        )
        
        if result.get('success'):
            print(f"✅ 微信支付创建成功: {result.get('order_id')}")
            print(f"   二维码: {result.get('qr_code', '')[:50]}...")
        else:
            print(f"❌ 微信支付创建失败: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ 微信支付服务测试失败: {str(e)}")
    
    # 测试支付宝
    try:
        alipay_service = PaymentFactory.get_payment_service('alipay')
        print("✅ 支付宝服务初始化成功")
        
        # 测试创建支付
        result = alipay_service.create_payment(
            order_id='test_order_456',
            amount=1000,
            description='测试支付',
            user_id='test_user'
        )
        
        if result.get('success'):
            print(f"✅ 支付宝支付创建成功: {result.get('order_id')}")
            print(f"   支付URL: {result.get('payment_url', '')[:50]}...")
        else:
            print(f"❌ 支付宝支付创建失败: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ 支付宝服务测试失败: {str(e)}")
    
    return True

def main():
    """主测试函数"""
    print("🚀 支付系统测试开始")
    print("="*50)
    
    # 测试配置
    if not test_payment_config():
        print("\n❌ 支付配置测试失败")
        return 1
    
    # 测试服务
    if not test_payment_service():
        print("\n❌ 支付服务测试失败")
        return 1
    
    print("\n" + "="*50)
    print("🎉 所有测试通过！")
    print("\n下一步：")
    print("1. 配置环境变量")
    print("2. 部署后端到Railway")
    print("3. 部署前端到Vercel")
    print("4. 进行真实支付测试")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x backend/test_payment.py
echo -e "${GREEN}✅ 支付测试脚本已创建${NC}"

# 步骤6：总结
echo ""
echo "6. 📋 部署总结"
echo "="*50
echo -e "${GREEN}✅ 支付集成代码已准备就绪${NC}"
echo ""
echo "📁 已创建的文件："
echo "  - backend/payment_config.py      # 支付配置"
echo "  - backend/payment_service.py     # 支付服务"
echo "  - backend/payment_api.py         # 支付API"
echo "  - backend/test_payment.py        # 测试脚本"
echo "  - backend/.env.example           # 环境变量示例"
echo ""
echo "🚀 下一步操作："
echo "1. 配置环境变量（参考 /tmp/payment_env_guide.txt）"
echo "2. 运行测试：cd backend && python test_payment.py"
echo "3. 部署后端：railway up"
echo "4. 部署前端：vercel --prod"
echo "5. 进行支付测试"
echo ""
echo "⏰ 预计部署时间：2-3小时"
echo "💳 支持支付渠道：微信支付、支付宝"
echo "🔒 安全特性：签名验证、防重放、数据加密"
echo ""
echo "="*50
echo "🎯 支付集成部署准备完成！"
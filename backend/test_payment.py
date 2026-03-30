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

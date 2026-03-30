#!/usr/bin/env python3
"""
支付配置模块
支持微信支付和支付宝
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class PaymentConfig:
    """支付配置类"""
    
    # 支付开关
    PAYMENT_ENABLED = os.getenv('PAYMENT_ENABLED', 'false').lower() == 'true'
    
    # 微信支付配置
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', '')
    WECHAT_MCH_ID = os.getenv('WECHAT_MCH_ID', '')
    WECHAT_API_KEY = os.getenv('WECHAT_API_KEY', '')
    WECHAT_CERT_PATH = os.getenv('WECHAT_CERT_PATH', '')
    WECHAT_KEY_PATH = os.getenv('WECHAT_KEY_PATH', '')
    
    # 支付宝配置
    ALIPAY_APP_ID = os.getenv('ALIPAY_APP_ID', '')
    ALIPAY_PRIVATE_KEY = os.getenv('ALIPAY_PRIVATE_KEY', '')
    ALIPAY_PUBLIC_KEY = os.getenv('ALIPAY_PUBLIC_KEY', '')
    ALIPAY_SIGN_TYPE = os.getenv('ALIPAY_SIGN_TYPE', 'RSA2')
    
    # 支付金额配置
    SERVICE_PRICE = 10  # 服务价格（元）
    
    # 回调URL配置
    NOTIFY_URL = os.getenv('NOTIFY_URL', '')
    RETURN_URL = os.getenv('RETURN_URL', '')
    
    # 沙箱模式
    SANDBOX_MODE = os.getenv('SANDBOX_MODE', 'true').lower() == 'true'
    
    @classmethod
    def validate_config(cls):
        """验证配置是否完整"""
        errors = []
        
        if cls.PAYMENT_ENABLED:
            # 检查微信支付配置
            if not cls.WECHAT_APP_ID:
                errors.append("微信支付APP_ID未配置")
            if not cls.WECHAT_MCH_ID:
                errors.append("微信支付商户号未配置")
            if not cls.WECHAT_API_KEY:
                errors.append("微信支付API密钥未配置")
            
            # 检查支付宝配置
            if not cls.ALIPAY_APP_ID:
                errors.append("支付宝APP_ID未配置")
            if not cls.ALIPAY_PRIVATE_KEY:
                errors.append("支付宝私钥未配置")
            if not cls.ALIPAY_PUBLIC_KEY:
                errors.append("支付宝公钥未配置")
        
        return errors
    
    @classmethod
    def get_wechat_config(cls):
        """获取微信支付配置"""
        return {
            'appid': cls.WECHAT_APP_ID,
            'mchid': cls.WECHAT_MCH_ID,
            'key': cls.WECHAT_API_KEY,
            'cert_path': cls.WECHAT_CERT_PATH,
            'key_path': cls.WECHAT_KEY_PATH,
            'sandbox': cls.SANDBOX_MODE
        }
    
    @classmethod
    def get_alipay_config(cls):
        """获取支付宝配置"""
        return {
            'appid': cls.ALIPAY_APP_ID,
            'app_private_key_string': cls.ALIPAY_PRIVATE_KEY,
            'alipay_public_key_string': cls.ALIPAY_PUBLIC_KEY,
            'sign_type': cls.ALIPAY_SIGN_TYPE,
            'sandbox': cls.SANDBOX_MODE
        }
    
    @classmethod
    def get_service_price(cls):
        """获取服务价格（分）"""
        return cls.SERVICE_PRICE * 100  # 转换为分
#!/usr/bin/env python3
"""
支付服务模块
处理微信支付和支付宝的集成
"""

import json
import time
import hashlib
import logging
from typing import Dict, Optional, Tuple
from payment_config import PaymentConfig

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentService:
    """支付服务基类"""
    
    def __init__(self):
        self.config = PaymentConfig()
        
    def create_payment(self, order_id: str, amount: int, description: str, 
                      user_id: str, ip: str = "127.0.0.1") -> Dict:
        """创建支付订单"""
        raise NotImplementedError("子类必须实现此方法")
    
    def verify_notification(self, data: Dict) -> Tuple[bool, str]:
        """验证支付通知"""
        raise NotImplementedError("子类必须实现此方法")
    
    def query_order(self, order_id: str) -> Dict:
        """查询支付订单状态"""
        raise NotImplementedError("子类必须实现此方法")
    
    def refund(self, order_id: str, refund_amount: int, reason: str = "") -> Dict:
        """退款"""
        raise NotImplementedError("子类必须实现此方法")

class WechatPaymentService(PaymentService):
    """微信支付服务"""
    
    def __init__(self):
        super().__init__()
        self.wechat_config = self.config.get_wechat_config()
        
        # 初始化微信支付客户端
        if self.config.PAYMENT_ENABLED and not self.config.SANDBOX_MODE:
            try:
                from wechatpayv3 import WeChatPay, WeChatPayType
                self.client = WeChatPay(
                    wechatpay_type=WeChatPayType.NATIVE,
                    mchid=self.wechat_config['mchid'],
                    private_key=self.wechat_config['key'],
                    cert_serial_no='',
                    apiv3_key=self.wechat_config['key'],
                    appid=self.wechat_config['appid'],
                    notify_url=self.config.NOTIFY_URL + '/wechat',
                    cert_dir='',
                    logger=logger,
                    partner_mode=False
                )
                logger.info("微信支付客户端初始化成功")
            except ImportError:
                logger.warning("微信支付SDK未安装，使用模拟模式")
                self.client = None
        else:
            self.client = None
            logger.info("微信支付使用模拟模式")
    
    def create_payment(self, order_id: str, amount: int, description: str, 
                      user_id: str, ip: str = "127.0.0.1") -> Dict:
        """创建微信支付订单"""
        
        if self.client is None or self.config.SANDBOX_MODE:
            # 模拟模式
            return {
                'success': True,
                'payment_type': 'wechat',
                'order_id': order_id,
                'code_url': f'weixin://wxpay/bizpayurl?pr={order_id}',
                'qr_code': f'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIxMDAiIHk9IjEwMCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5XZWNoYXQgUGF5IERFTU88L3RleHQ+PC9zdmc+',
                'amount': amount,
                'description': description,
                'sandbox': True
            }
        
        try:
            # 真实微信支付
            code, message = self.client.pay(
                description=description,
                out_trade_no=order_id,
                amount={'total': amount},
                payer={'ip': ip}
            )
            
            if code == 200:
                return {
                    'success': True,
                    'payment_type': 'wechat',
                    'order_id': order_id,
                    'code_url': message.get('code_url', ''),
                    'qr_code': self._generate_qr_code(message.get('code_url', '')),
                    'amount': amount,
                    'description': description,
                    'sandbox': False
                }
            else:
                return {
                    'success': False,
                    'error': f'微信支付创建失败: {message}',
                    'payment_type': 'wechat'
                }
                
        except Exception as e:
            logger.error(f"微信支付创建异常: {str(e)}")
            return {
                'success': False,
                'error': f'支付系统异常: {str(e)}',
                'payment_type': 'wechat'
            }
    
    def verify_notification(self, data: Dict) -> Tuple[bool, str]:
        """验证微信支付通知"""
        if self.config.SANDBOX_MODE:
            # 模拟验证
            return True, data.get('out_trade_no', '')
        
        # 真实验证逻辑
        # 这里需要实现微信支付通知的验证
        # 包括签名验证、金额验证等
        return False, "未实现"
    
    def query_order(self, order_id: str) -> Dict:
        """查询微信支付订单"""
        if self.config.SANDBOX_MODE:
            # 模拟查询
            return {
                'success': True,
                'order_id': order_id,
                'status': 'SUCCESS',  # 模拟支付成功
                'amount': 1000,
                'paid_time': int(time.time())
            }
        
        # 真实查询逻辑
        return {
            'success': False,
            'error': '未实现真实查询',
            'order_id': order_id
        }
    
    def _generate_qr_code(self, code_url: str) -> str:
        """生成二维码图片（简化版）"""
        # 实际项目中应该使用qrcode库生成二维码
        return f'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIxMDAiIHk9IjEwMCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5XZWNoYXQgUGF5PC90ZXh0Pjwvc3ZnPg=='

class AlipayPaymentService(PaymentService):
    """支付宝支付服务"""
    
    def __init__(self):
        super().__init__()
        self.alipay_config = self.config.get_alipay_config()
        
        # 初始化支付宝客户端
        if self.config.PAYMENT_ENABLED and not self.config.SANDBOX_MODE:
            try:
                from alipay import AliPay
                self.client = AliPay(
                    appid=self.alipay_config['appid'],
                    app_notify_url=self.config.NOTIFY_URL + '/alipay',
                    app_private_key_string=self.alipay_config['app_private_key_string'],
                    alipay_public_key_string=self.alipay_config['alipay_public_key_string'],
                    sign_type=self.alipay_config['sign_type'],
                    debug=self.config.SANDBOX_MODE
                )
                logger.info("支付宝客户端初始化成功")
            except ImportError:
                logger.warning("支付宝SDK未安装，使用模拟模式")
                self.client = None
        else:
            self.client = None
            logger.info("支付宝使用模拟模式")
    
    def create_payment(self, order_id: str, amount: int, description: str, 
                      user_id: str, ip: str = "127.0.0.1") -> Dict:
        """创建支付宝订单"""
        
        if self.client is None or self.config.SANDBOX_MODE:
            # 模拟模式
            return {
                'success': True,
                'payment_type': 'alipay',
                'order_id': order_id,
                'qr_code': f'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIxMDAiIHk9IjEwMCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BbGlwYXkgREVNTzwvdGV4dD48L3N2Zz4=',
                'amount': amount,
                'description': description,
                'sandbox': True
            }
        
        try:
            # 真实支付宝支付
            order_string = self.client.api_alipay_trade_page_pay(
                out_trade_no=order_id,
                total_amount=amount / 100,  # 转换为元
                subject=description,
                return_url=self.config.RETURN_URL,
                notify_url=self.config.NOTIFY_URL + '/alipay'
            )
            
            # 生成支付页面URL
            if self.config.SANDBOX_MODE:
                gateway = "https://openapi.alipaydev.com/gateway.do"
            else:
                gateway = "https://openapi.alipay.com/gateway.do"
            
            payment_url = f"{gateway}?{order_string}"
            
            return {
                'success': True,
                'payment_type': 'alipay',
                'order_id': order_id,
                'payment_url': payment_url,
                'qr_code': self._generate_qr_code(payment_url),
                'amount': amount,
                'description': description,
                'sandbox': self.config.SANDBOX_MODE
            }
                
        except Exception as e:
            logger.error(f"支付宝支付创建异常: {str(e)}")
            return {
                'success': False,
                'error': f'支付系统异常: {str(e)}',
                'payment_type': 'alipay'
            }
    
    def verify_notification(self, data: Dict) -> Tuple[bool, str]:
        """验证支付宝通知"""
        if self.config.SANDBOX_MODE:
            # 模拟验证
            return True, data.get('out_trade_no', '')
        
        # 真实验证逻辑
        if self.client:
            success = self.client.verify(data, data.get('sign'))
            if success:
                return True, data.get('out_trade_no', '')
        
        return False, "验证失败"
    
    def query_order(self, order_id: str) -> Dict:
        """查询支付宝订单"""
        if self.config.SANDBOX_MODE:
            # 模拟查询
            return {
                'success': True,
                'order_id': order_id,
                'status': 'TRADE_SUCCESS',
                'amount': 1000,
                'paid_time': int(time.time())
            }
        
        # 真实查询逻辑
        if self.client:
            try:
                result = self.client.api_alipay_trade_query(out_trade_no=order_id)
                if result.get('code') == '10000':
                    return {
                        'success': True,
                        'order_id': order_id,
                        'status': result.get('trade_status'),
                        'amount': int(float(result.get('total_amount', 0)) * 100),
                        'paid_time': result.get('send_pay_date')
                    }
            except Exception as e:
                logger.error(f"支付宝查询异常: {str(e)}")
        
        return {
            'success': False,
            'error': '查询失败',
            'order_id': order_id
        }
    
    def _generate_qr_code(self, payment_url: str) -> str:
        """生成二维码图片（简化版）"""
        return f'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNmZmYiLz48dGV4dCB4PSIxMDAiIHk9IjEwMCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BbGlwYXk8L3RleHQ+PC9zdmc+'

class PaymentFactory:
    """支付工厂类"""
    
    @staticmethod
    def get_payment_service(payment_type: str) -> PaymentService:
        """获取支付服务实例"""
        if payment_type == 'wechat':
            return WechatPaymentService()
        elif payment_type == 'alipay':
            return AlipayPaymentService()
        else:
            raise ValueError(f"不支持的支付类型: {payment_type}")
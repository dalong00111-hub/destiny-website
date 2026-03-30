#!/usr/bin/env python3
"""
支付API模块
提供支付相关的REST API接口
"""

import json
import logging
from flask import Blueprint, request, jsonify, g
from payment_service import PaymentFactory
from payment_config import PaymentConfig

# 创建蓝图
payment_bp = Blueprint('payment', __name__, url_prefix='/api/payment')

# 设置日志
logger = logging.getLogger(__name__)

@payment_bp.route('/create', methods=['POST'])
def create_payment():
    """创建支付订单"""
    try:
        data = request.json
        order_id = data.get('order_id')
        payment_type = data.get('payment_type', 'wechat')
        user_id = data.get('user_id')
        description = data.get('description', '命运预测服务')
        
        if not order_id or not user_id:
            return jsonify({
                'success': False,
                'error': '缺少必要参数'
            }), 400
        
        # 获取支付服务
        try:
            payment_service = PaymentFactory.get_payment_service(payment_type)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        
        # 获取配置
        config = PaymentConfig()
        amount = config.get_service_price()
        
        # 获取客户端IP
        client_ip = request.remote_addr
        
        # 创建支付
        result = payment_service.create_payment(
            order_id=order_id,
            amount=amount,
            description=description,
            user_id=user_id,
            ip=client_ip
        )
        
        # 记录支付创建日志
        db = g.get('_database')
        if db:
            db.execute('''
                INSERT INTO payment_logs (order_id, payment_type, amount, status, request_data)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, payment_type, amount, 'created', json.dumps(data)))
            db.commit()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"创建支付异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'支付系统异常: {str(e)}'
        }), 500

@payment_bp.route('/query/<order_id>', methods=['GET'])
def query_payment(order_id):
    """查询支付状态"""
    try:
        payment_type = request.args.get('payment_type', 'wechat')
        
        # 获取支付服务
        try:
            payment_service = PaymentFactory.get_payment_service(payment_type)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        
        # 查询支付状态
        result = payment_service.query_order(order_id)
        
        # 更新订单状态
        if result.get('success') and result.get('status') in ['SUCCESS', 'TRADE_SUCCESS']:
            db = g.get('_database')
            if db:
                # 更新订单状态
                db.execute('''
                    UPDATE orders SET status = 'paid', paid_at = CURRENT_TIMESTAMP
                    WHERE order_id = ?
                ''', (order_id,))
                
                # 记录支付成功日志
                db.execute('''
                    INSERT INTO payment_logs (order_id, payment_type, amount, status, response_data)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, payment_type, result.get('amount', 0), 'success', json.dumps(result)))
                db.commit()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"查询支付异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'查询异常: {str(e)}'
        }), 500

@payment_bp.route('/notify/wechat', methods=['POST'])
def wechat_notify():
    """微信支付回调通知"""
    try:
        # 获取通知数据
        data = request.get_data(as_text=True)
        logger.info(f"微信支付回调: {data}")
        
        # 解析数据
        try:
            notify_data = json.loads(data)
        except:
            notify_data = dict(request.form)
        
        # 获取支付服务
        payment_service = PaymentFactory.get_payment_service('wechat')
        
        # 验证通知
        success, order_id = payment_service.verify_notification(notify_data)
        
        if success and order_id:
            # 更新订单状态
            db = g.get('_database')
            if db:
                db.execute('''
                    UPDATE orders SET status = 'paid', paid_at = CURRENT_TIMESTAMP
                    WHERE order_id = ?
                ''', (order_id,))
                
                # 记录通知日志
                db.execute('''
                    INSERT INTO payment_logs (order_id, payment_type, status, request_data)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, 'wechat', 'notified', data))
                db.commit()
            
            # 返回成功响应给微信
            return jsonify({'code': 'SUCCESS', 'message': 'OK'})
        else:
            return jsonify({'code': 'FAIL', 'message': '验证失败'}), 400
            
    except Exception as e:
        logger.error(f"微信支付回调异常: {str(e)}")
        return jsonify({'code': 'FAIL', 'message': str(e)}), 500

@payment_bp.route('/notify/alipay', methods=['POST'])
def alipay_notify():
    """支付宝支付回调通知"""
    try:
        # 获取通知数据
        data = dict(request.form)
        logger.info(f"支付宝支付回调: {data}")
        
        # 获取支付服务
        payment_service = PaymentFactory.get_payment_service('alipay')
        
        # 验证通知
        success, order_id = payment_service.verify_notification(data)
        
        if success and order_id:
            # 更新订单状态
            db = g.get('_database')
            if db:
                db.execute('''
                    UPDATE orders SET status = 'paid', paid_at = CURRENT_TIMESTAMP
                    WHERE order_id = ?
                ''', (order_id,))
                
                # 记录通知日志
                db.execute('''
                    INSERT INTO payment_logs (order_id, payment_type, status, request_data)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, 'alipay', 'notified', json.dumps(data)))
                db.commit()
            
            # 返回成功响应给支付宝
            return 'success'
        else:
            return 'failure'
            
    except Exception as e:
        logger.error(f"支付宝支付回调异常: {str(e)}")
        return 'failure', 500

@payment_bp.route('/refund', methods=['POST'])
def refund_payment():
    """退款"""
    try:
        data = request.json
        order_id = data.get('order_id')
        payment_type = data.get('payment_type', 'wechat')
        reason = data.get('reason', '用户申请退款')
        
        if not order_id:
            return jsonify({
                'success': False,
                'error': '缺少订单ID'
            }), 400
        
        # 获取支付服务
        try:
            payment_service = PaymentFactory.get_payment_service(payment_type)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        
        # 查询订单金额
        db = g.get('_database')
        if db:
            order = db.execute('''
                SELECT amount FROM orders WHERE order_id = ?
            ''', (order_id,)).fetchone()
            
            if not order:
                return jsonify({
                    'success': False,
                    'error': '订单不存在'
                }), 404
            
            amount = order['amount']
            
            # 执行退款
            result = payment_service.refund(order_id, amount, reason)
            
            if result.get('success'):
                # 更新订单状态
                db.execute('''
                    UPDATE orders SET status = 'refunded', refunded_at = CURRENT_TIMESTAMP
                    WHERE order_id = ?
                ''', (order_id,))
                
                # 记录退款日志
                db.execute('''
                    INSERT INTO payment_logs (order_id, payment_type, amount, status, request_data)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, payment_type, amount, 'refunded', json.dumps(data)))
                db.commit()
            
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': '数据库连接失败'
            }), 500
            
    except Exception as e:
        logger.error(f"退款异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'退款异常: {str(e)}'
        }), 500

@payment_bp.route('/config', methods=['GET'])
def get_payment_config():
    """获取支付配置信息"""
    try:
        config = PaymentConfig()
        
        # 验证配置
        errors = config.validate_config()
        
        return jsonify({
            'success': True,
            'payment_enabled': config.PAYMENT_ENABLED,
            'sandbox_mode': config.SANDBOX_MODE,
            'service_price': config.SERVICE_PRICE,
            'config_errors': errors,
            'wechat_configured': bool(config.WECHAT_APP_ID),
            'alipay_configured': bool(config.ALIPAY_APP_ID)
        })
        
    except Exception as e:
        logger.error(f"获取支付配置异常: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
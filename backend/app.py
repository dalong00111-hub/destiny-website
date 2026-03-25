#!/usr/bin/env python3
"""
命运预测网站后端API
使用 Flask + SQLite + AI 分析
"""

import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import hashlib
import random

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置
DATABASE = 'data/destiny.db'

def get_db():
    """获取数据库连接"""
    db = getattr(g, '_database', None)
    if db is None:
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """关闭数据库连接"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """初始化数据库"""
    with app.app_context():
        db = get_db()
        
        # 创建用户表
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建订单表
        db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                birth_data TEXT NOT NULL,
                amount INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # 创建分析结果表
        db.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                bazi_info TEXT NOT NULL,
                analysis_result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (order_id)
            )
        ''')
        
        # 创建问题记录表
        db.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (order_id)
            )
        ''')
        
        db.commit()
        print("数据库初始化完成")

def generate_user_id():
    """生成用户ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices('0123456789abcdef', k=8))
    return f'USER_{timestamp}_{random_str}'

def generate_order_id():
    """生成订单ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices('0123456789ABCDEF', k=6))
    return f'ORDER_{timestamp}_{random_str}'

def calculate_bazi(year, month, day, hour, gender):
    """
    计算八字（简化版）
    实际应该使用完整的八字算法
    """
    # 天干
    heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    # 地支
    earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 简化计算：使用年份和时辰生成八字
    year_idx = (year - 4) % 10  # 简化计算
    month_idx = month % 12
    day_idx = day % 10
    hour_idx = hour % 12
    
    bazi = {
        'year_stem': heavenly_stems[year_idx % 10],
        'year_branch': earthly_branches[year_idx % 12],
        'month_stem': heavenly_stems[month_idx % 10],
        'month_branch': earthly_branches[month_idx % 12],
        'day_stem': heavenly_stems[day_idx % 10],
        'day_branch': earthly_branches[day_idx % 12],
        'hour_stem': heavenly_stems[hour_idx % 10],
        'hour_branch': earthly_branches[hour_idx % 12]
    }
    
    return bazi

def generate_analysis(bazi_info, gender):
    """生成命理分析（使用AI或模板）"""
    
    # 这里应该调用AI API，暂时使用模板
    analysis_templates = {
        'personality': [
            "您性格开朗，思维敏捷，富有创造力。",
            "您为人稳重，做事踏实，值得信赖。",
            "您聪明机智，适应能力强，善于交际。",
            "您意志坚定，目标明确，执行力强。"
        ],
        'career': [
            "适合从事需要创意和沟通的工作。",
            "在技术或专业领域会有很好的发展。",
            "适合创业或管理工作。",
            "在教育和咨询行业会有不错的表现。"
        ],
        'relationship': [
            "感情丰富，重视家庭，婚姻运势较好。",
            "需要多沟通，避免误解。",
            "适合找性格互补的伴侣。",
            "感情路上需要更多耐心和理解。"
        ],
        'health': [
            "身体素质较好，注意规律作息。",
            "需要注意消化系统健康。",
            "建议适当运动，保持良好心态。",
            "注意劳逸结合，避免过度劳累。"
        ]
    }
    
    # 根据八字信息选择不同的模板
    stem_sum = sum(ord(c) for c in ''.join(bazi_info.values()))
    idx = stem_sum % 4
    
    analysis = {
        'bazi_display': f"{bazi_info['year_stem']}{bazi_info['year_branch']} {bazi_info['month_stem']}{bazi_info['month_branch']} {bazi_info['day_stem']}{bazi_info['day_branch']} {bazi_info['hour_stem']}{bazi_info['hour_branch']}",
        'personality': analysis_templates['personality'][idx],
        'career': analysis_templates['career'][idx],
        'relationship': analysis_templates['relationship'][idx],
        'health': analysis_templates['health'][idx],
        'fortunes': generate_fortunes(),
        'recommendations': generate_recommendations(gender)
    }
    
    return analysis

def generate_fortunes():
    """生成运势预测"""
    fortunes = []
    periods = ['本月', '下月', '本季度', '下半年']
    levels = ['★★★★☆', '★★★☆☆', '★★★★★', '★★☆☆☆']
    descriptions = [
        '事业上有新机会，财运平稳上升',
        '工作压力增大，需要调整心态',
        '整体运势上升，可能有重要突破',
        '需要谨慎行事，避免重大决策'
    ]
    
    for i in range(4):
        fortunes.append({
            'period': periods[i],
            'level': levels[i],
            'desc': descriptions[i],
            'tip': '保持积极心态，把握机会' if i % 2 == 0 else '注意细节，避免冲动'
        })
    
    return fortunes

def generate_recommendations(gender):
    """生成建议"""
    if gender == 'male':
        return [
            '多关注事业发展，把握晋升机会',
            '注意工作与生活的平衡',
            '加强人际关系的维护',
            '培养长期投资意识'
        ]
    else:
        return [
            '关注自我成长和提升',
            '平衡家庭与个人发展',
            '建立自己的社交圈子',
            '培养理财能力'
        ]

def answer_question(question, bazi_info):
    """回答用户问题（AI辅助）"""
    # 这里应该调用AI API分析问题并生成回答
    # 暂时使用模板回答
    
    question_lower = question.lower()
    
    if '工作' in question_lower or '事业' in question_lower:
        answers = [
            "根据您的八字，今年是事业发展的重要时期。",
            "建议把握下半年的事业机会。",
            "适合在现有基础上寻求突破。",
            "需要注意与同事的沟通协调。"
        ]
    elif '感情' in question_lower or '婚姻' in question_lower:
        answers = [
            "感情运势平稳，需要多沟通。",
            "适合通过共同兴趣增进感情。",
            "避免因小事产生矛盾。",
            "珍惜眼前人，用心经营感情。"
        ]
    elif '健康' in question_lower:
        answers = [
            "注意规律作息，保证充足睡眠。",
            "适当运动，增强体质。",
            "饮食清淡，避免暴饮暴食。",
            "保持良好心态，避免压力过大。"
        ]
    elif '财运' in question_lower or '金钱' in question_lower:
        answers = [
            "财运平稳，适合稳健投资。",
            "避免高风险投资。",
            "注意理性消费。",
            "可以考虑长期理财规划。"
        ]
    else:
        answers = [
            "根据您的命理分析，建议保持积极心态。",
            "命运掌握在自己手中，努力是关键。",
            "当前运势平稳，适合稳步发展。",
            "注意把握时机，避免冲动决策。"
        ]
    
    return random.choice(answers)

# API路由
@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/init-user', methods=['POST'])
def init_user():
    """初始化用户"""
    try:
        user_id = generate_user_id()
        db = get_db()
        
        db.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        db.commit()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': '用户初始化成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/create-order', methods=['POST'])
def create_order():
    """创建订单"""
    try:
        data = request.json
        user_id = data.get('user_id')
        birth_data = data.get('birth_data')
        
        if not user_id or not birth_data:
            return jsonify({
                'success': False,
                'error': '缺少必要参数'
            }), 400
        
        # 验证用户是否存在
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在'
            }), 404
        
        # 创建订单
        order_id = generate_order_id()
        db.execute('''
            INSERT INTO orders (order_id, user_id, birth_data, amount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, user_id, json.dumps(birth_data), 10, 'pending'))
        db.commit()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'amount': 10,
            'message': '订单创建成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/complete-order', methods=['POST'])
def complete_order():
    """完成订单（支付成功）"""
    try:
        data = request.json
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({
                'success': False,
                'error': '缺少订单ID'
            }), 400
        
        db = get_db()
        
        # 获取订单信息
        order = db.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,)).fetchone()
        if not order:
            return jsonify({
                'success': False,
                'error': '订单不存在'
            }), 404
        
        if order['status'] == 'completed':
            return jsonify({
                'success': False,
                'error': '订单已完成'
            }), 400
        
        # 更新订单状态
        db.execute('''
            UPDATE orders 
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP 
            WHERE order_id = ?
        ''', (order_id,))
        
        # 生成命理分析
        birth_data = json.loads(order['birth_data'])
        bazi_info = calculate_bazi(
            birth_data['year'],
            birth_data['month'],
            birth_data['day'],
            birth_data['hour'],
            birth_data['gender']
        )
        
        analysis = generate_analysis(bazi_info, birth_data['gender'])
        
        # 保存分析结果
        db.execute('''
            INSERT INTO analyses (order_id, bazi_info, analysis_result)
            VALUES (?, ?, ?)
        ''', (order_id, json.dumps(bazi_info), json.dumps(analysis)))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'analysis': analysis,
            'message': '订单完成，分析生成成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get-analysis/<order_id>', methods=['GET'])
def get_analysis(order_id):
    """获取分析结果"""
    try:
        db = get_db()
        
        analysis = db.execute('''
            SELECT * FROM analyses WHERE order_id = ?
        ''', (order_id,)).fetchone()
        
        if not analysis:
            return jsonify({
                'success': False,
                'error': '分析结果不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'analysis': json.loads(analysis['analysis_result']),
            'bazi_info': json.loads(analysis['bazi_info']),
            'created_at': analysis['created_at']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    """提问问题"""
    try:
        data = request.json
        order_id = data.get('order_id')
        question = data.get('question')
        
        if not order_id or not question:
            return jsonify({
                'success': False,
                'error': '缺少必要参数'
            }), 400
        
        # 检查订单是否存在且已完成
        db = get_db()
        order = db.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,)).fetchone()
        if not order or order['status'] != 'completed':
            return jsonify({
                'success': False,
                'error': '订单不存在或未完成'
            }), 404
        
        # 检查问题数量（最多3个）
        question_count = db.execute('''
            SELECT COUNT(*) as count FROM questions WHERE order_id = ?
        ''', (order_id,)).fetchone()['count']
        
        if question_count >= 3:
            return jsonify({
                'success': False,
                'error': '提问次数已用完'
            }), 400
        
        # 获取八字信息用于生成回答
        analysis = db.execute('''
            SELECT bazi_info FROM analyses WHERE order_id = ?
        ''', (order_id,)).fetchone()
        
        bazi_info = json.loads(analysis['bazi_info']) if analysis else {}
        
        # 生成回答
        answer = answer_question(question, bazi_info)
        
        # 保存问题
        db.execute('''
            INSERT INTO questions (order_id, question, answer)
            VALUES (?, ?, ?)
        ''', (order_id, question, answer))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'answer': answer,
            'remaining_questions': 2 - question_count,
            'message': '问题已回答'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get-questions/<order_id>', methods=['GET'])
def get_questions(order_id):
    """获取问题列表"""
    try:
        db = get_db()
        
        questions = db.execute('''
            SELECT * FROM questions WHERE order_id = ? ORDER BY created_at
        ''', (order_id,)).fetchall()
        
        question_list = []
        for q in questions:
            question_list.append({
                'id': q['id'],
                'question': q['question'],
                'answer': q['answer'],
                'created_at': q['created_at']
            })
        
        return jsonify({
            'success': True,
            'questions': question_list,
            'count': len(question_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 初始化数据库
    init_db()
    
    print("=" * 60)
    print("命运预测网站后端启动")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("API地址: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
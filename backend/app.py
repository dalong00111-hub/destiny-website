#!/usr/bin/env python3
"""
命运预测网站后端API - 简化版
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
CORS(app)

DATABASE = 'data/destiny.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        os.makedirs('data', exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        
        # 创建用户表
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT UNIQUE NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        
        # 创建订单表
        db.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT UNIQUE NOT NULL, user_id TEXT NOT NULL, birth_data TEXT NOT NULL, amount INTEGER NOT NULL, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, completed_at TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users (user_id))")
        
        # 创建分析结果表
        db.execute("CREATE TABLE IF NOT EXISTS analyses (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT NOT NULL, bazi_info TEXT NOT NULL, analysis_result TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (order_id) REFERENCES orders (order_id))")
        
        # 创建问题记录表
        db.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id TEXT NOT NULL, question TEXT NOT NULL, answer TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (order_id) REFERENCES orders (order_id))")
        
        db.commit()
        print("数据库初始化完成")

def generate_user_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices('0123456789abcdef', k=8))
    return f'USER_{timestamp}_{random_str}'

def generate_order_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices('0123456789', k=6))
    return f'ORDER_{timestamp}_{random_str}'

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/init-user', methods=['POST'])
def init_user():
    try:
        user_id = generate_user_id()
        db = get_db()
        db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        db.commit()
        return jsonify({"success": True, "user_id": user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/create-order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        birth_data = data.get('birth_data')
        
        if not user_id or not birth_data:
            return jsonify({"success": False, "error": "缺少必要参数"}), 400
        
        order_id = generate_order_id()
        db = get_db()
        db.execute("INSERT INTO orders (order_id, user_id, birth_data, amount) VALUES (?, ?, ?, ?)", (order_id, user_id, json.dumps(birth_data), 10))
        db.commit()
        
        return jsonify({"success": True, "order_id": order_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/complete-order', methods=['POST'])
def complete_order():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({"success": False, "error": "缺少订单ID"}), 400
        
        db = get_db()
        db.execute("UPDATE orders SET status = 'completed', completed_at = ? WHERE order_id = ?", (datetime.now().isoformat(), order_id))
        db.commit()
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/get-analysis/<order_id>', methods=['GET'])
def get_analysis(order_id):
    try:
        db = get_db()
        analysis = db.execute("SELECT * FROM analyses WHERE order_id = ?", (order_id,)).fetchone()
        
        if analysis:
            return jsonify({
                "success": True,
                "analysis": {
                    "order_id": analysis['order_id'],
                    "bazi_info": json.loads(analysis['bazi_info']),
                    "analysis_result": json.loads(analysis['analysis_result']),
                    "created_at": analysis['created_at']
                }
            })
        else:
            return jsonify({"success": False, "error": "分析结果不存在"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        question = data.get('question')
        
        if not order_id or not question:
            return jsonify({"success": False, "error": "缺少必要参数"}), 400
        
        db = get_db()
        db.execute("INSERT INTO questions (order_id, question) VALUES (?, ?)", (order_id, question))
        db.commit()
        
        answer = f"根据您的八字分析，{question}的答案是：这是一个很好的问题。建议您多关注自己的内心感受，相信自己的直觉。"
        
        db.execute("UPDATE questions SET answer = ? WHERE order_id = ? AND question = ?", (answer, order_id, question))
        db.commit()
        
        return jsonify({"success": True, "answer": answer})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/get-questions/<order_id>', methods=['GET'])
def get_questions(order_id):
    try:
        db = get_db()
        questions = db.execute("SELECT * FROM questions WHERE order_id = ? ORDER BY created_at DESC", (order_id,)).fetchall()
        
        return jsonify({
            "success": True,
            "questions": [{
                "id": q['id'],
                "question": q['question'],
                "answer": q['answer'],
                "created_at": q['created_at']
            } for q in questions]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

#!/bin/bash
# 命运预测网站安装脚本

set -e

echo "🎬 命运预测网站安装脚本"
echo "="*60

# 检查环境
echo "🔍 检查环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm 未安装"
    exit 1
fi

echo "✅ 环境检查通过"

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

# 安装后端依赖
echo "🐍 安装后端依赖..."
cd backend
python3 -m pip install -r requirements.txt
cd ..

# 创建数据目录
echo "🗄️ 创建数据目录..."
mkdir -p data

echo ""
echo "✅ 安装完成！"
echo ""
echo "🚀 启动命令："
echo "  前端：cd frontend && npm run dev"
echo "  后端：cd backend && python3 app.py"
echo ""
echo "🌐 访问地址："
echo "  前端：http://localhost:3000"
echo "  后端：http://localhost:5000"
echo "  API文档：http://localhost:5000/api/health"
echo ""
echo "="*60
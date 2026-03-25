#!/bin/bash
# 启动命运预测网站

set -e

echo "🚀 启动命运预测网站"
echo "="*60

# 检查是否已安装
if [ ! -d "frontend/node_modules" ] || [ ! -d "backend/__pycache__" ]; then
    echo "⚠️  检测到未安装依赖，正在安装..."
    bash scripts/setup.sh
fi

# 启动后端
echo "🐍 启动后端服务..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "⏳ 等待后端启动..."
sleep 3

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 服务已启动！"
echo ""
echo "🌐 访问地址："
echo "  前端界面：http://localhost:3000"
echo "  后端API：http://localhost:5000"
echo ""
echo "📊 服务状态："
echo "  后端PID：$BACKEND_PID"
echo "  前端PID：$FRONTEND_PID"
echo ""
echo "🛑 停止服务："
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "="*60

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM
wait
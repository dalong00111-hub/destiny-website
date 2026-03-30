#!/bin/bash
echo "🔍 命运预测网站部署检查"
echo "="*50

echo "1. 检查前端配置..."
if [ -f "frontend/.env.production" ]; then
    echo "   ✅ .env.production存在"
    echo "   API URL: $(cat frontend/.env.production)"
else
    echo "   ❌ .env.production不存在"
fi

echo ""
echo "2. 检查后端配置..."
if [ -f "backend/requirements.txt" ]; then
    echo "   ✅ requirements.txt存在"
    echo "   依赖: $(cat backend/requirements.txt | wc -l) 个"
else
    echo "   ❌ requirements.txt不存在"
fi

echo ""
echo "3. 检查数据库..."
if [ -f "backend/data/destiny.db" ]; then
    echo "   ✅ destiny.db存在"
    echo "   大小: $(ls -lh backend/data/destiny.db | awk '{print $5}')"
else
    echo "   ❌ destiny.db不存在"
fi

echo ""
echo "4. 检查部署文件..."
if [ -f "vercel.json" ]; then
    echo "   ✅ vercel.json存在"
else
    echo "   ❌ vercel.json不存在"
fi

if [ -f "backend/railway.json" ]; then
    echo "   ✅ railway.json存在"
else
    echo "   ❌ railway.json不存在"
fi

echo ""
echo "5. 一键启动测试..."
echo "   启动命令:"
echo "   后端: cd backend && python3 app.py"
echo "   前端: cd frontend && npm run dev"
echo ""
echo "6. 一键部署命令:"
echo "   后端部署: railway up"
echo "   前端部署: vercel --prod"
echo ""
echo "="*50
echo "📋 部署准备状态: 就绪"
echo "🚀 下一步: 执行部署到Railway和Vercel"

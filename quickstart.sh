#!/bin/bash

echo "========================================"
echo "🤖 具身智能每日速递 - 快速开始"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3，请先安装 Python"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo ""
    echo "📝 未找到 .env 文件，正在创建..."
    cp .env.example .env
    echo "✓ 已创建 .env 文件"
    echo ""
    echo "⚠️  请编辑 .env 文件，填写以下配置："
    echo "   - SENDER_EMAIL (发件邮箱)"
    echo "   - SENDER_PASSWORD (邮箱授权码/应用专用密码)"
    echo "   - RECEIVER_EMAIL (收件邮箱)"
    echo "   - OPENAI_API_KEY (OpenAI 或 DeepSeek 的 API Key)"
    echo ""
    echo "详细配置说明请查看 SETUP_GUIDE.md"
    echo ""
    read -p "配置完成后按回车继续..."
fi

# 安装依赖
echo ""
echo "📦 正在安装依赖..."
pip install -r requirements.txt python-dotenv -q

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✓ 依赖安装完成"

# 测试配置
echo ""
echo "🔧 测试配置..."
python3 test_config.py

echo ""
read -p "如果配置测试通过，按回车运行完整程序..."

# 运行主程序
echo ""
python3 main.py

echo ""
echo "========================================"
echo "✅ 运行完成！"
echo "========================================"
echo ""
echo "下一步："
echo "1. 如果成功收到邮件，说明配置正确"
echo "2. 推送到 GitHub 并配置 GitHub Actions 实现每日自动推送"
echo "3. 详细说明请查看 README.md"
echo ""

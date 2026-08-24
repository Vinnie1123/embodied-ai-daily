#!/usr/bin/env python3
"""
配置测试脚本 - 验证邮箱和 API 配置是否正确
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI

def test_email_config():
    """测试邮箱配置"""
    print("\n" + "="*60)
    print("📧 测试邮箱配置...")
    print("="*60)
    
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    # 检查配置
    if not all([sender_email, sender_password, receiver_email]):
        print("❌ 缺少邮箱配置，请检查 .env 文件")
        return False
    
    print(f"发件邮箱: {sender_email}")
    print(f"收件邮箱: {receiver_email}")
    print(f"SMTP 服务器: {smtp_server}:{smtp_port}")
    
    try:
        # 创建测试邮件
        msg = MIMEText("这是一封测试邮件，如果收到说明配置成功！\n\n来自：具身智能每日速递", "plain", "utf-8")
        msg['Subject'] = "✅ 配置测试成功 - 具身智能每日速递"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        # 发送邮件
        print("\n正在发送测试邮件...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print("✅ 邮箱配置正确！测试邮件已发送")
        print(f"   请检查 {receiver_email} 的收件箱")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ 邮箱认证失败")
        print("   请检查:")
        print("   1. Gmail 用户：是否使用了'应用专用密码'？")
        print("   2. QQ 用户：是否使用了'授权码'？")
        print("   3. 密码中是否有多余的空格？")
        return False
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def test_openai_config():
    """测试 OpenAI API 配置"""
    print("\n" + "="*60)
    print("🤖 测试 OpenAI API 配置...")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    if not api_key:
        print("❌ 缺少 OPENAI_API_KEY，请检查 .env 文件")
        return False
    
    print(f"API Base URL: {base_url}")
    print(f"API Key: {api_key[:15]}...{api_key[-4:]}")
    
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        print("\n正在测试 API 调用...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "回复'配置成功'三个字"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API 配置正确！")
        print(f"   测试响应: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        print("\n   请检查:")
        print("   1. API Key 是否正确？")
        print("   2. 账户是否有余额？")
        print("   3. 如果使用 DeepSeek，OPENAI_BASE_URL 是否设置为 https://api.deepseek.com/v1 ？")
        return False

def main():
    print("\n" + "="*60)
    print("🔧 具身智能每日速递 - 配置测试工具")
    print("="*60)
    
    # 加载环境变量
    if not os.path.exists(".env"):
        print("\n❌ 未找到 .env 文件")
        print("   请复制 .env.example 为 .env 并填写配置：")
        print("   cp .env.example .env")
        return
    
    load_dotenv()
    print("✓ 已加载 .env 配置文件")
    
    # 测试邮箱
    email_ok = test_email_config()
    
    # 测试 API
    api_ok = test_openai_config()
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    print(f"邮箱配置: {'✅ 通过' if email_ok else '❌ 失败'}")
    print(f"API 配置: {'✅ 通过' if api_ok else '❌ 失败'}")
    
    if email_ok and api_ok:
        print("\n🎉 所有配置正确！可以运行 python main.py 了")
    else:
        print("\n⚠️  请修复上述问题后重新测试")
        print("   详细配置说明请查看 SETUP_GUIDE.md")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

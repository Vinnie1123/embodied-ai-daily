#!/usr/bin/env python3
"""
具身智能每日速递 - 主程序
每天自动抓取 arXiv 论文和 GitHub 项目，生成摘要并发送邮件
"""

import os
from dotenv import load_dotenv
from fetch_content import ContentFetcher
from send_email import EmailSender

def main():
    # 加载环境变量
    load_dotenv()
    
    # 检查必要的环境变量
    required_vars = ["SENDER_EMAIL", "SENDER_PASSWORD", "RECEIVER_EMAIL", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请复制 .env.example 为 .env 并填写配置")
        return
    
    print("=" * 60)
    print("🤖 具身智能每日速递 - 开始运行")
    print("=" * 60)
    
    # 1. 抓取内容
    print("\n📥 正在抓取内容...")
    fetcher = ContentFetcher()
    data = fetcher.fetch_all()
    
    candidate_counts = data.get("candidate_counts", {})
    print(f"\n✓ 候选池：{candidate_counts.get('papers', 0)} 篇论文，{candidate_counts.get('repos', 0)} 个项目")
    print(f"✓ 邮件精选：{len(data['papers'])} 篇论文，{len(data['repos'])} 个项目")
    
    # 2. 发送邮件
    print("\n📧 正在发送邮件...")
    sender = EmailSender()
    success = sender.send_daily_digest(data)
    
    if success:
        print("\n✅ 每日速递发送完成！")
    else:
        print("\n❌ 发送失败，请检查配置")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

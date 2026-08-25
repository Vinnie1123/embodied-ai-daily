import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import os
from typing import Dict

EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 28px; }
        .header .date { opacity: 0.9; margin-top: 10px; font-size: 14px; }
        .section { margin-bottom: 40px; }
        .section-title { font-size: 22px; color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }
        .item { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #667eea; }
        .item-title { font-size: 18px; font-weight: 600; color: #2d3748; margin-bottom: 10px; }
        .item-title a { color: #667eea; text-decoration: none; }
        .item-title a:hover { text-decoration: underline; }
        .meta { font-size: 13px; color: #718096; margin-bottom: 12px; }
        .summary { background: white; padding: 15px; border-radius: 6px; margin-top: 10px; font-size: 15px; line-height: 1.7; }
        .keywords { margin-top: 10px; }
        .keyword { display: inline-block; background: #e0e7ff; color: #5a67d8; padding: 4px 12px; border-radius: 12px; font-size: 12px; margin-right: 6px; margin-top: 6px; }
        .stats { display: inline-flex; align-items: center; gap: 15px; }
        .stat-item { display: flex; align-items: center; gap: 5px; }
        .footer { text-align: center; padding: 20px; color: #718096; font-size: 13px; border-top: 1px solid #e2e8f0; margin-top: 40px; }
        .no-content { text-align: center; padding: 40px; color: #718096; }
        .toc { background: #f8f9fa; padding: 18px 22px; border-radius: 8px; margin-bottom: 30px; }
        .toc .section-title { font-size: 18px; margin-bottom: 8px; }
        .toc ol { margin: 0; padding-left: 24px; }
        .toc a { color: #4c51bf; text-decoration: none; }
        .toc a:hover { text-decoration: underline; }
        .overview { background: #eef2ff; padding: 20px 24px; border-radius: 8px; margin-bottom: 30px; color: #373f66; }
        .overview p { margin: 0; }
        .recommendation { border-left-color: #d97706; background: #fffbeb; }
        .recommendation-badge { display: inline-block; background: #d97706; color: white; padding: 3px 9px; border-radius: 4px; font-size: 12px; margin-bottom: 8px; }
        .reason { color: #92400e; font-size: 14px; margin: 8px 0 12px; }
        .empty-note { color: #718096; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 具身智能每日速递</h1>
        <div class="date">{{ date }}</div>
    </div>

    <div class="toc">
        <div class="section-title">目录</div>
        <ol>
            <li><a href="#overview">今日总览</a></li>
            {% if selected %}<li><a href="#recommendations">重点推荐（{{ [selected|length, 3]|min }}）</a></li>{% endif %}
            {% if selected %}<li><a href="#selected">每日精选（{{ selected|length }}）</a></li>{% endif %}
        </ol>
    </div>

    <div class="section" id="overview">
        <div class="section-title">今日总览</div>
        <div class="overview">
            <p>{{ overview or '今日精选内容正在整理中。' }}</p>
        </div>
    </div>

    {% if selected %}
    <div class="section" id="recommendations">
        <div class="section-title">重点推荐</div>
        {% for item in selected[:3] %}
        <div class="item recommendation">
            <span class="recommendation-badge">优先阅读</span>
            <div class="item-title">
                <a href="{{ item.url }}" target="_blank">{{ item.title or item.full_name }}</a>
            </div>
            <div class="meta">{{ item.content_type }}{% if item.published %} | 📅 {{ item.published }}{% endif %}{% if item.category %} | 🏷️ {{ item.category }}{% endif %}{% if item.stars %} | ⭐ {{ item.stars }}{% endif %}</div>
            <div class="reason">{{ item.recommendation_reason }}</div>
            <div class="summary"><strong>深度解读：</strong>{{ item.ai_summary }}</div>
        </div>
        {% endfor %}
    </div>

    <div class="section" id="selected">
        <div class="section-title">每日精选 ({{ selected|length }})</div>
        {% for item in selected[3:] %}
        <div class="item">
            <div class="item-title">
                <a href="{{ item.url }}" target="_blank">{{ item.title or item.full_name }}</a>
            </div>
            <div class="meta">{{ item.content_type }}{% if item.published %} | 📅 {{ item.published }}{% endif %}{% if item.authors %} | 👥 {{ item.authors|join(', ') }}{% endif %}{% if item.category %} | 🏷️ {{ item.category }}{% endif %}{% if item.stars %} | ⭐ {{ item.stars }}{% endif %}</div>
            <div class="summary"><strong>深度解读：</strong>{{ item.ai_summary }}</div>
            {% if item.keywords %}<div class="keywords">{% for kw in item.keywords %}<span class="keyword">{{ kw }}</span>{% endfor %}</div>{% endif %}
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="section"><div class="section-title">每日精选</div><div class="no-content">今日没有匹配的新内容</div></div>
    {% endif %}

    <div class="footer">
        <p>本邮件由 <strong>具身智能每日速递</strong> 自动生成</p>
        <p>关键词过滤：embodied, world model, robot manipulation, LLM+robot, sim2real, edge deployment, ROS, vision-language</p>
    </div>
</body>
</html>
"""

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.receiver_email = os.getenv("RECEIVER_EMAIL")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    def send_daily_digest(self, data: Dict):
        """发送每日速递邮件"""
        # 渲染 HTML
        template = Template(EMAIL_TEMPLATE)
        html_content = template.render(**data)
        
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🤖 具身智能每日速递 - {data['date']}"
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        
        # 添加 HTML 内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 发送邮件
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✓ 邮件发送成功到 {self.receiver_email}")
            return True
        except Exception as e:
            print(f"✗ 邮件发送失败: {e}")
            return False

if __name__ == "__main__":
    # 测试邮件模板
    test_paper = {
        "title": "Test Paper",
        "authors": ["Author 1", "Author 2"],
        "published": "2026-08-24",
        "category": "cs.RO",
        "content_type": "论文",
        "url": "https://arxiv.org/abs/test",
        "ai_summary": "这是一个测试解读",
        "recommendation_reason": "适合作为今日研究方向的入门阅读。",
        "keywords": ["embodied", "robot"]
    }
    test_data = {
        "date": "2026-08-24",
        "overview": "今天的测试总览。",
        "selected": [test_paper],
        "papers": [test_paper],
        "repos": []
    }
    
    sender = EmailSender()
    sender.send_daily_digest(test_data)

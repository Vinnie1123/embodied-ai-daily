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
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 具身智能每日速递</h1>
        <div class="date">{{ date }}</div>
    </div>

    {% if papers %}
    <div class="section">
        <div class="section-title">📄 最新论文 ({{ papers|length }})</div>
        {% for paper in papers %}
        <div class="item">
            <div class="item-title">
                <a href="{{ paper.url }}" target="_blank">{{ paper.title }}</a>
            </div>
            <div class="meta">
                📅 {{ paper.published }} | 👥 {{ paper.authors|join(', ') }}{% if paper.authors|length > 3 %} et al.{% endif %} | 🏷️ {{ paper.category }}
            </div>
            {% if paper.ai_summary %}
            <div class="summary">
                <strong>AI 摘要：</strong>{{ paper.ai_summary }}
            </div>
            {% endif %}
            <div class="keywords">
                {% for kw in paper.keywords %}
                <span class="keyword">{{ kw }}</span>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="section">
        <div class="section-title">📄 最新论文</div>
        <div class="no-content">今日没有匹配的新论文</div>
    </div>
    {% endif %}

    {% if repos %}
    <div class="section">
        <div class="section-title">⭐ GitHub 热门项目 ({{ repos|length }})</div>
        {% for repo in repos %}
        <div class="item">
            <div class="item-title">
                <a href="{{ repo.url }}" target="_blank">{{ repo.full_name }}</a>
            </div>
            <div class="meta">
                <div class="stats">
                    <span class="stat-item">⭐ {{ repo.stars }}</span>
                    <span class="stat-item">💻 {{ repo.language }}</span>
                </div>
            </div>
            <div class="summary">
                <strong>{{ repo.description }}</strong>
                {% if repo.ai_summary %}
                <br><br><em>{{ repo.ai_summary }}</em>
                {% endif %}
            </div>
            {% if repo.keywords %}
            <div class="keywords">
                {% for kw in repo.keywords %}
                <span class="keyword">{{ kw }}</span>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="section">
        <div class="section-title">⭐ GitHub 热门项目</div>
        <div class="no-content">今日没有匹配的热门项目</div>
    </div>
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
    test_data = {
        "date": "2026-08-24",
        "papers": [{
            "title": "Test Paper",
            "authors": ["Author 1", "Author 2"],
            "published": "2026-08-24",
            "category": "cs.RO",
            "url": "https://arxiv.org/abs/test",
            "ai_summary": "这是一个测试摘要",
            "keywords": ["embodied", "robot"]
        }],
        "repos": [{
            "full_name": "test/repo",
            "description": "Test repository",
            "url": "https://github.com/test/repo",
            "stars": 100,
            "language": "Python",
            "ai_summary": "测试项目摘要",
            "keywords": ["llm"]
        }]
    }
    
    sender = EmailSender()
    sender.send_daily_digest(test_data)

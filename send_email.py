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
        .header { background: linear-gradient(135deg, #334155 0%, #0f766e 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { margin: 0; font-size: 28px; }
        .header .date { opacity: 0.9; margin-top: 10px; font-size: 14px; }
        .section { margin-bottom: 40px; }
        .section-title { font-size: 22px; color: #0f766e; border-bottom: 2px solid #0f766e; padding-bottom: 10px; margin-bottom: 20px; }
        .item { background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #0f766e; }
        .item-title { font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 10px; }
        .item-title a { color: #0f766e; text-decoration: none; }
        .item-title a:hover { text-decoration: underline; }
        .meta, .heat { font-size: 13px; color: #64748b; margin-bottom: 12px; }
        .heat { color: #b45309; font-weight: 600; }
        .summary { background: white; padding: 15px; border-radius: 6px; margin-top: 10px; font-size: 15px; line-height: 1.7; }
        .keywords { margin-top: 10px; }
        .keyword { display: inline-block; background: #ccfbf1; color: #115e59; padding: 4px 10px; border-radius: 12px; font-size: 12px; margin-right: 6px; margin-top: 6px; }
        .toc { background: #f8fafc; padding: 18px 22px; border-radius: 8px; margin-bottom: 30px; }
        .toc .section-title { font-size: 18px; margin-bottom: 8px; }
        .toc ol { margin: 0; padding-left: 24px; }
        .toc a { color: #0f766e; text-decoration: none; }
        .overview { background: #ecfeff; padding: 20px 24px; border-radius: 8px; margin-bottom: 30px; color: #164e63; }
        .recommendation { border-left-color: #d97706; background: #fffbeb; }
        .recommendation-badge { display: inline-block; background: #d97706; color: white; padding: 3px 9px; border-radius: 4px; font-size: 12px; margin-bottom: 8px; }
        .reason { color: #92400e; font-size: 14px; margin: 8px 0 12px; }
        .empty-note { color: #718096; font-size: 14px; padding: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #718096; font-size: 13px; border-top: 1px solid #e2e8f0; margin-top: 40px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>具身智能每日速递</h1>
        <div class="date">{{ date }} · 今日精选 {{ selected|length }} 条</div>
    </div>

    <div class="toc">
        <div class="section-title">今日目录</div>
        <ol>
            <li><a href="#overview">趋势总览</a></li>
            {% if recommendations %}<li><a href="#recommendations">重点推荐（{{ recommendations|length }}）</a></li>{% endif %}
            <li><a href="#papers">论文精选（{{ papers|length }}）</a></li>
            <li><a href="#repos">项目精选（{{ repos|length }}）</a></li>
        </ol>
    </div>

    <div class="section" id="overview">
        <div class="section-title">今日趋势总览</div>
        <div class="overview"><p>{{ overview or '今日精选内容正在整理中。' }}</p></div>
    </div>

    {% if recommendations %}
    <div class="section" id="recommendations">
        <div class="section-title">重点推荐</div>
        {% for item in recommendations %}
        <div class="item recommendation">
            <span class="recommendation-badge">优先阅读</span>
            <div class="item-title"><a href="{{ item.url }}" target="_blank">{{ item.title or item.full_name }}</a></div>
            <div class="heat">{{ item.heat_label }}：{{ item.heat_detail }}</div>
            <div class="reason">{{ item.recommendation_reason }}</div>
            <div class="summary"><strong>内容解读：</strong>{{ item.ai_summary }}</div>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="section" id="papers">
        <div class="section-title">论文精选（{{ papers|length }}）</div>
        {% if papers %}
        {% for item in papers if not item.is_recommended %}
        <div class="item">
            <div class="item-title"><a href="{{ item.url }}" target="_blank">{{ item.title }}</a></div>
            <div class="heat">{{ item.heat_label }}：{{ item.heat_detail }}</div>
            <div class="meta">📅 {{ item.published }}{% if item.authors %} · {{ item.authors|join(', ') }}{% endif %}</div>
            <div class="summary"><strong>内容解读：</strong>{{ item.ai_summary }}</div>
            {% if item.keywords %}<div class="keywords">{% for kw in item.keywords %}<span class="keyword">{{ kw }}</span>{% endfor %}</div>{% endif %}
        </div>
        {% endfor %}
        {% else %}<div class="empty-note">今日暂无可用论文。</div>{% endif %}
    </div>

    <div class="section" id="repos">
        <div class="section-title">GitHub 项目精选（{{ repos|length }}）</div>
        {% if repos %}
        {% for item in repos if not item.is_recommended %}
        <div class="item">
            <div class="item-title"><a href="{{ item.url }}" target="_blank">{{ item.full_name }}</a></div>
            <div class="heat">{{ item.heat_label }}：{{ item.heat_detail }}</div>
            <div class="meta">{{ item.description }}</div>
            <div class="summary"><strong>项目解读：</strong>{{ item.ai_summary }}</div>
            {% if item.keywords %}<div class="keywords">{% for kw in item.keywords %}<span class="keyword">{{ kw }}</span>{% endfor %}</div>{% endif %}
        </div>
        {% endfor %}
        {% else %}<div class="empty-note">今日暂无可用 GitHub 项目。</div>{% endif %}
    </div>

    <div class="footer"><p>本邮件由具身智能每日速递自动生成</p></div>
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
        template = Template(EMAIL_TEMPLATE)
        html_content = template.render(**data)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"具身智能每日速递 - {data['date']}"
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

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

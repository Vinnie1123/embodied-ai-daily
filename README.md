# 🤖 具身智能每日速递

> 每天早上 9 点自动推送最新的具身智能领域论文和 GitHub 项目到你的邮箱

## ✨ 功能特性

- 🔍 **智能过滤**：根据 8 个关键词自动筛选相关内容
  - embodied（具身智能）
  - world model（世界模型）
  - robot manipulation（机器人操作）
  - LLM + robot（大模型+机器人）
  - sim2real（仿真到现实）
  - edge deployment / quantization（端侧部署/量化）
  - ROS / ROS2（机器人中间件）
  - vision-language model（视觉语言模型）

- 🤖 **AI 摘要**：每篇论文/项目用 1-2 句话总结核心创新点
- 📧 **邮件推送**：精美的 HTML 邮件，移动端友好
- ⚡ **零成本运行**：基于 GitHub Actions，完全免费

## 📦 快速开始

### 1. Fork 本项目到你的 GitHub

点击右上角 "Fork" 按钮

### 2. 配置 GitHub Secrets

进入你 Fork 的仓库，点击 `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

添加以下 secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `SENDER_EMAIL` | 发件邮箱 | `your-email@gmail.com` |
| `SENDER_PASSWORD` | 邮箱应用专用密码 | 见下方说明 |
| `RECEIVER_EMAIL` | 收件邮箱 | `your-email@example.com` |
| `SMTP_SERVER` | SMTP 服务器 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `OPENAI_API_KEY` | OpenAI API Key | `sk-xxx` 或 DeepSeek Key |
| `OPENAI_BASE_URL` | API 地址（可选） | `https://api.deepseek.com/v1` |

### 3. 获取邮箱应用专用密码

#### Gmail 用户：
1. 前往 https://myaccount.google.com/security
2. 开启"两步验证"
3. 搜索"应用专用密码"
4. 选择"邮件"和"其他设备"
5. 生成密码并复制（16位，无空格）

#### QQ 邮箱用户：
1. 登录 QQ 邮箱网页版
2. 设置 → 账户 → 开启 SMTP 服务
3. 获取授权码
4. 配置：
   - `SMTP_SERVER`: `smtp.qq.com`
   - `SMTP_PORT`: `587`

#### 163 邮箱用户：
1. 设置 → POP3/SMTP/IMAP → 开启 SMTP
2. 获取授权码
3. 配置：
   - `SMTP_SERVER`: `smtp.163.com`
   - `SMTP_PORT`: `465`（需修改代码为 SSL）

### 4. 获取 OpenAI API Key

#### 方案 A：使用 OpenAI（推荐新手）
1. 前往 https://platform.openai.com/api-keys
2. 注册并创建 API Key
3. 费用：约 $0.01-0.02 / 天（使用 gpt-4o-mini）

#### 方案 B：使用 DeepSeek（推荐国内用户，更便宜）
1. 前往 https://platform.deepseek.com/
2. 注册并创建 API Key
3. 配置：
   - `OPENAI_API_KEY`: 填 DeepSeek Key
   - `OPENAI_BASE_URL`: `https://api.deepseek.com/v1`
4. 费用：约 ¥0.01-0.02 / 天

### 5. 启用 GitHub Actions

1. 进入你 Fork 的仓库
2. 点击 `Actions` 标签
3. 点击 "I understand my workflows, go ahead and enable them"

### 6. 测试运行

点击 `Actions` → `Daily Digest` → `Run workflow` → `Run workflow`

等待 2-3 分钟，查收邮件！

## 🔧 本地测试

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/embodied-ai-daily.git
cd embodied-ai-daily

# 2. 安装依赖
pip install -r requirements.txt
pip install python-dotenv

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写配置

# 4. 运行
python main.py
```

## ⏰ 修改推送时间

编辑 `.github/workflows/daily-digest.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 01:00 = 北京时间 09:00
```

常用时间对照：
- 北京时间 08:00 → `0 0 * * *`
- 北京时间 09:00 → `0 1 * * *`
- 北京时间 12:00 → `0 4 * * *`
- 北京时间 18:00 → `0 10 * * *`

## 🎨 自定义关键词

编辑 `fetch_content.py` 的 `KEYWORDS` 列表：

```python
KEYWORDS = [
    "embodied",
    "world model",
    "你的关键词",
    # ...
]
```

## 📊 邮件示例

<img src="https://via.placeholder.com/800x600/667eea/ffffff?text=Email+Preview" alt="邮件预览">

## 🛠️ 技术栈

- **Python 3.11**
- **arxiv** - arXiv 论文抓取
- **requests** - GitHub API 调用
- **OpenAI API** - 论文摘要生成
- **Jinja2** - 邮件模板渲染
- **GitHub Actions** - 定时任务

## ❓ 常见问题

### Q1: 没有收到邮件？
1. 检查 GitHub Actions 运行日志是否有报错
2. 确认邮箱配置正确，应用专用密码无误
3. 查看垃圾邮件文件夹

### Q2: API 费用太贵？
- 使用 DeepSeek API（比 OpenAI 便宜 10 倍）
- 修改 `fetch_content.py` 中的 `papers[:10]` 为 `papers[:5]`，减少摘要数量

### Q3: GitHub Actions 没有运行？
- 确认已在 Actions 页面启用工作流
- Fork 的仓库需要手动启用 Actions
- 第一次需要手动触发一次

### Q4: 想要更多/更少的内容？
修改 `fetch_content.py`：
- 论文数量：`max_results=50` → 调整数字
- 项目数量：`repos[:15]` → 调整数字
- 日期范围：`days_back=1` → 调整天数

## 📝 许可证

MIT License

## 🙏 致谢

- arXiv.org - 开放获取的预印本服务
- GitHub - 代码托管和 Actions 服务
- OpenAI / DeepSeek - LLM API 服务

---

**如有问题，欢迎提 Issue！**

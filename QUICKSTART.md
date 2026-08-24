# 🚀 三步开始使用

## 方案一：GitHub Actions 自动运行（推荐）

### 1️⃣ 推送到 GitHub

```bash
# 在 GitHub 上创建新仓库（名称：embodied-ai-daily）
# 然后执行：
git remote add origin https://github.com/你的用户名/embodied-ai-daily.git
git branch -M main
git push -u origin main
```

### 2️⃣ 配置 GitHub Secrets

进入仓库 `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**最简配置（QQ邮箱 + DeepSeek）：**

| Secret 名称 | 值 |
|------------|---|
| `SENDER_EMAIL` | `你的QQ邮箱@qq.com` |
| `SENDER_PASSWORD` | `QQ邮箱授权码（16位）` |
| `RECEIVER_EMAIL` | `你的QQ邮箱@qq.com` |
| `SMTP_SERVER` | `smtp.qq.com` |
| `SMTP_PORT` | `587` |
| `OPENAI_API_KEY` | `DeepSeek 的 API Key` |
| `OPENAI_BASE_URL` | `https://api.deepseek.com/v1` |

详细配置说明：📖 [SETUP_GUIDE.md](SETUP_GUIDE.md)

### 3️⃣ 启用 Actions 并测试

1. 进入 `Actions` 标签
2. 点击 `I understand my workflows, go ahead and enable them`
3. 点击 `Daily Digest` → `Run workflow` → `Run workflow`
4. 等待 2-3 分钟，查收邮件！

✅ 完成！以后每天早上 9 点自动推送。

---

## 方案二：本地运行（快速测试）

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt python-dotenv
```

### 2️⃣ 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env，填写邮箱和 API 配置
nano .env  # 或用其他编辑器
```

### 3️⃣ 测试配置

```bash
# 测试邮箱和 API 配置是否正确
python test_config.py
```

### 4️⃣ 运行

```bash
# 发送今日速递
python main.py
```

或者使用快速启动脚本：

```bash
./quickstart.sh
```

---

## 📁 项目结构

```
embodied-ai-daily/
├── main.py                    # 主程序入口
├── fetch_content.py           # 内容抓取（arXiv + GitHub）
├── send_email.py              # 邮件发送
├── test_config.py             # 配置测试工具
├── quickstart.sh              # 快速启动脚本
├── requirements.txt           # Python 依赖
├── .env.example               # 配置模板
├── .github/workflows/
│   └── daily-digest.yml       # GitHub Actions 配置
├── README.md                  # 项目说明
├── SETUP_GUIDE.md             # 详细配置教程
└── QUICKSTART.md              # 本文件
```

---

## 🎯 关键词配置

当前筛选的关键词（在 `fetch_content.py` 中）：

- **embodied** - 具身智能
- **world model** - 世界模型
- **robot manipulation** - 机器人操作
- **llm robot** - 大模型+机器人
- **sim2real** - 仿真到现实
- **edge deployment / quantization** - 端侧部署/量化
- **ros** - 机器人中间件
- **vision-language model** - 视觉语言模型

可以根据需要修改。

---

## 💰 费用估算

### DeepSeek API（推荐）
- 每天约 ¥0.01-0.02
- **¥10 可用 1-2 年**

### OpenAI API
- 每天约 $0.01-0.02
- $5 可用几个月

### GitHub Actions
- **完全免费**（每月 2000 分钟额度）

---

## ⏰ 修改推送时间

编辑 `.github/workflows/daily-digest.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # 北京时间 09:00
```

常用时间：
- 08:00 → `0 0 * * *`
- 12:00 → `0 4 * * *`
- 18:00 → `0 10 * * *`

---

## ❓ 遇到问题？

1. 📖 查看 [SETUP_GUIDE.md](SETUP_GUIDE.md) - 详细配置说明
2. 📖 查看 [README.md](README.md) - 完整项目文档
3. 🔧 运行 `python test_config.py` - 测试配置
4. 📝 查看 GitHub Actions 日志 - 排查错误

---

**祝你每天都能获取最新的具身智能知识！** 🎉

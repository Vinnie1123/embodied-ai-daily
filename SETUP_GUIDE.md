# 📖 详细配置教程

## 第一步：Fork 项目到你的 GitHub

1. 首先你需要把这个项目推送到 GitHub（见下方"推送到 GitHub"部分）
2. 或者如果项目已经在 GitHub 上，直接 Fork

## 第二步：配置邮箱（最关键）

### 方案 A：使用 Gmail（推荐国外用户）

#### 1. 开启 Gmail 的"两步验证"

1. 访问 https://myaccount.google.com/security
2. 找到"登录 Google"部分
3. 点击"两步验证" → 按照提示完成设置

#### 2. 生成应用专用密码

1. 回到 https://myaccount.google.com/security
2. 在搜索框输入"应用专用密码"
3. 点击"应用专用密码"
4. 选择"选择应用" → "邮件"
5. 选择"选择设备" → "其他（自定义名称）"
6. 输入名称：`Embodied AI Daily`
7. 点击"生成"
8. **复制 16 位密码**（格式：xxxx xxxx xxxx xxxx，去掉空格）

#### 3. 需要配置的 Secrets：

```
SENDER_EMAIL = your-email@gmail.com
SENDER_PASSWORD = （上面生成的 16 位密码，去掉空格）
RECEIVER_EMAIL = your-email@gmail.com （可以是同一个邮箱）
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
```

---

### 方案 B：使用 QQ 邮箱（推荐国内用户）

#### 1. 开启 QQ 邮箱 SMTP 服务

1. 登录 QQ 邮箱网页版：https://mail.qq.com
2. 点击右上角"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"SMTP服务"（如果已开启，跳过）
5. 点击"生成授权码"
6. 按照提示发送短信
7. **复制生成的授权码**（16位字母+数字）

#### 2. 需要配置的 Secrets：

```
SENDER_EMAIL = your-email@qq.com
SENDER_PASSWORD = （上面生成的授权码）
RECEIVER_EMAIL = your-email@qq.com （可以是同一个邮箱）
SMTP_SERVER = smtp.qq.com
SMTP_PORT = 587
```

---

### 方案 C：使用 163 邮箱

#### 1. 开启 163 邮箱 SMTP 服务

1. 登录 163 邮箱：https://mail.163.com
2. 设置 → POP3/SMTP/IMAP
3. 开启"SMTP服务"
4. 设置授权密码（不是邮箱密码！）
5. **记住这个授权密码**

#### 2. 需要配置的 Secrets：

```
SENDER_EMAIL = your-email@163.com
SENDER_PASSWORD = （上面设置的授权密码）
RECEIVER_EMAIL = your-email@163.com
SMTP_SERVER = smtp.163.com
SMTP_PORT = 465
```

**注意**：163 邮箱使用 SSL，需要修改代码中的 `server.starttls()` 部分。

---

## 第三步：配置 OpenAI API

### 方案 A：使用 DeepSeek（强烈推荐国内用户）

**优势**：
- 国内可直接访问，无需翻墙
- 价格便宜（比 OpenAI 便宜 10 倍）
- 质量不错，中文支持好

**配置步骤**：

1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 充值（最低 ¥10，够用很久）
4. 创建 API Key：
   - 进入"API Keys"页面
   - 点击"创建新的 API Key"
   - **复制 Key**（只显示一次！）

5. 需要配置的 Secrets：

```
OPENAI_API_KEY = sk-xxxxxxxxxxxxxx （DeepSeek 的 Key）
OPENAI_BASE_URL = https://api.deepseek.com/v1
```

**费用估算**：
- 每天约 10-20 次 API 调用
- 每次约 ¥0.001-0.002
- **每天约 ¥0.01-0.02**
- **¥10 可以用 1-2 年**

---

### 方案 B：使用 OpenAI（需要翻墙 + 海外信用卡）

1. 访问 https://platform.openai.com/
2. 注册账号（需要海外手机号验证）
3. 绑定海外信用卡
4. 创建 API Key
5. 需要配置的 Secrets：

```
OPENAI_API_KEY = sk-xxxxxxxxxxxxxx
OPENAI_BASE_URL = https://api.openai.com/v1 （可不填，默认值）
```

**费用估算**：
- 每天约 $0.01-0.02
- $5 可以用几个月

---

## 每日邮件内容与数量

每日邮件默认最多包含 3 篇论文和 5 个 GitHub 项目。系统会先抓取更大的候选池，再按相关性和项目 stars 分别筛选；邮件中的数量是实际精选数量，不是候选池总量。

如需调整配额，可在本地 `.env` 或 GitHub Actions 环境中设置：

```
MAX_DAILY_PAPERS=3
MAX_DAILY_REPOS=5
```

每条内容包含真实热度信息：论文显示主题关键词命中数和 arXiv 分类，项目显示 GitHub stars 和主要语言；随后附带“问题、方法或功能、关注价值、适合读者”的中文解读。

## 第四步：在 GitHub 配置 Secrets

### 1. 进入你的 GitHub 仓库

访问：`https://github.com/你的用户名/embodied-ai-daily`

### 2. 进入 Settings

点击仓库顶部的 `Settings`（设置）标签

### 3. 进入 Secrets 设置

左侧菜单：`Secrets and variables` → `Actions`

### 4. 添加 Secrets

点击 `New repository secret`，逐个添加以下配置：

#### Gmail + DeepSeek 示例（推荐）

| Name | Value（示例） |
|------|--------------|
| `SENDER_EMAIL` | `zhangsan@gmail.com` |
| `SENDER_PASSWORD` | `abcdabcdabcdabcd`（16位，无空格） |
| `RECEIVER_EMAIL` | `zhangsan@gmail.com` |
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `OPENAI_API_KEY` | `sk-xxxxxxxxxxxxxx`（DeepSeek Key） |
| `OPENAI_BASE_URL` | `https://api.deepseek.com/v1` |

#### QQ 邮箱 + DeepSeek 示例（国内推荐）

| Name | Value（示例） |
|------|--------------|
| `SENDER_EMAIL` | `12345678@qq.com` |
| `SENDER_PASSWORD` | `abcd1234efgh5678`（16位授权码） |
| `RECEIVER_EMAIL` | `12345678@qq.com` |
| `SMTP_SERVER` | `smtp.qq.com` |
| `SMTP_PORT` | `587` |
| `OPENAI_API_KEY` | `sk-xxxxxxxxxxxxxx`（DeepSeek Key） |
| `OPENAI_BASE_URL` | `https://api.deepseek.com/v1` |

---

## 第五步：启用 GitHub Actions

### 1. 进入 Actions 页面

点击仓库顶部的 `Actions` 标签

### 2. 启用工作流

如果看到提示：`Workflows aren't being run on this forked repository`

点击绿色按钮：`I understand my workflows, go ahead and enable them`

### 3. 手动触发第一次运行（测试）

1. 点击左侧的 `Daily Digest`
2. 点击右侧的 `Run workflow` 下拉框
3. 点击绿色的 `Run workflow` 按钮
4. 等待 2-3 分钟

### 4. 查看运行日志

1. 刷新页面，会看到一个运行记录
2. 点击进去查看详细日志
3. 如果看到 `✓ 邮件发送成功`，说明配置正确！

### 5. 查收邮件

检查你的收件箱（如果没有，查看垃圾邮件文件夹）

---

## 第六步：修改推送时间（可选）

默认是每天 **北京时间 09:00** 推送。

如果想改时间，编辑 `.github/workflows/daily-digest.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 01:00 = 北京时间 09:00
```

**时间对照表**（北京时间 → cron 表达式）：

| 北京时间 | cron 表达式 | 说明 |
|---------|------------|------|
| 08:00 | `0 0 * * *` | 早餐前 |
| 09:00 | `0 1 * * *` | 上班路上 |
| 12:00 | `0 4 * * *` | 午休时间 |
| 18:00 | `0 10 * * *` | 下班路上 |
| 20:00 | `0 12 * * *` | 晚上学习 |

修改后，commit + push 即可生效。

---

## 常见问题排查

### ❌ 问题 1：没有收到邮件

**排查步骤**：

1. 检查 GitHub Actions 日志是否有报错
2. 确认邮箱配置正确（特别是 `SENDER_PASSWORD`）
3. 查看垃圾邮件文件夹
4. 尝试用同样的配置本地运行一次（见 README 本地测试部分）

### ❌ 问题 2：邮件发送失败，报 Authentication failed

**原因**：邮箱密码错误

**解决**：
- Gmail：检查是否用的"应用专用密码"，不是邮箱登录密码
- QQ：检查是否用的"授权码"，不是邮箱登录密码
- 确认 Secrets 中没有多余的空格

### ❌ 问题 3：OpenAI API 报错

**原因**：API Key 错误或余额不足

**解决**：
1. 检查 API Key 是否正确
2. 检查账户余额
3. 如果使用 DeepSeek，确认 `OPENAI_BASE_URL` 设置正确

### ❌ 问题 4：GitHub Actions 没有自动运行

**原因**：
- Fork 的仓库默认禁用 Actions
- 工作流文件有语法错误

**解决**：
1. 进入 Actions 页面手动启用
2. 检查 `.github/workflows/daily-digest.yml` 格式
3. 手动触发一次测试

### ❌ 问题 5：收到的邮件内容为空

**原因**：当天没有匹配关键词的新内容

**解决**：
- 正常现象，不是每天都有相关论文
- 可以修改关键词，扩大筛选范围
- 可以修改 `fetch_content.py` 中的 `days_back=1` 为 `days_back=2`，看最近 2 天的内容

---

## 推送到 GitHub（如果还没有）

如果你是本地创建的项目，需要先推送到 GitHub：

```bash
# 1. 在 GitHub 上创建一个新仓库
# 仓库名：embodied-ai-daily
# 不要初始化 README

# 2. 在本地执行
git remote add origin https://github.com/你的用户名/embodied-ai-daily.git
git branch -M main
git push -u origin main
```

---

## 下一步优化建议

配置完成后，你可以考虑：

1. **调整关键词**：编辑 `fetch_content.py` 的 `KEYWORDS` 列表
2. **增加数据源**：添加 Twitter、Reddit、HackerNews 等
3. **本地备份**：定期把邮件内容保存为 Markdown
4. **分享给同事**：让团队一起用

---

**如有问题，随时问我！**

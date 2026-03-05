# 红绿贴纸实时脑暴工具

一个支持多用户实时同步的脑暴工具，使用 Flask + Flask-SocketIO 构建。

## 功能特性

- 🟥 红色贴纸（痛点区域）
- 🟩 绿色贴纸（经验区域）
- 🔄 实时同步：多个用户可以同时使用，所有贴纸即时同步
- 📥 导出功能：支持导出 CSV 格式

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py
```

访问 http://localhost:5000

## 部署到云平台

### 选项 1: Render（推荐 - 免费）

1. **注册账号**: https://render.com
2. **创建 Web Service**:
   - 登录后点击 "New" → "Web Service"
   - 连接您的 GitHub 仓库
   - 设置以下配置:
     - Name: `red-green-brainstorm`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app --worker-class eventlet -w 1 --bind :$PORT`
   - 点击 "Create Web Service"

3. **等待部署完成**，Render 会提供访问 URL

### 选项 2: Railway（免费）

1. **注册账号**: https://railway.app
2. **创建新项目**: 
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择您的仓库
3. **配置环境变量**:
   - 在项目设置中添加 `PORT` = `5000`
4. **部署完成**后访问提供的 URL

### 选项 3: Fly.io（免费）

1. **安装 CLI**: `brew install flyctl` (macOS)
2. **登录**: `flyctl auth login`
3. **创建应用**:
   ```bash
   flyctl launch
   ```
4. **部署**:
   ```bash
   flyctl deploy
   ```

## 注意事项

- 免费云平台会在一段时间无活动后进入休眠状态
- 免费平台的 Web Service 重启后数据会丢失（内存中的 stickers 列表会清空）
- 如需持久化存储，需要连接数据库（如 Redis、PostgreSQL）

## 技术栈

- 后端: Flask + Flask-SocketIO
- 前端: HTML + CSS + JavaScript (Socket.io-client)
- 部署: Gunicorn + Eventlet

## 许可证

MIT

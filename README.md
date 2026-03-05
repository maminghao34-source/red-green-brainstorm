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

## 部署到 Render

1. 访问 https://render.com
2. 创建 Web Service，连接此仓库
3. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind :$PORT`
4. 部署完成后访问提供的 URL

## 技术栈

- 后端: Flask + Flask-SocketIO
- 前端: HTML + CSS + JavaScript
- 部署: Gunicorn

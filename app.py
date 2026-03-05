import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import csv
import io
from supabase import create_client, Client

app = Flask(__name__)

# Supabase 配置
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://xogphwdskolzyjznzhbk.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhvZ3Bod2Rza29senlqem56aGJrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4OTM1NzQsImV4cCI6MjA4NzQ2OTU3NH0.Q_7FNbC1H0bZ5KQ3YyJ8KJh8YvBqY5xG7nR9tWpY0oU')

# 初始化 Supabase 客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'brainstorm-secret-key-prod')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """健康检查路由"""
    return jsonify({'status': 'ok'}), 200

@app.route('/export')
def export():
    # 从 Supabase 获取所有贴纸
    response = supabase.table('stickers').select('*').execute()
    stickers = response.data
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['类型', '内容', '时间'])
    
    for sticker in stickers:
        color_type = '痛点' if sticker['color'] == 'red' else '经验'
        writer.writerow([color_type, sticker['content'], sticker['timestamp']])
    
    output.seek(0)
    return jsonify({
        'data': output.getvalue(),
        'filename': f'brainstorm_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    })

@socketio.on('connect')
def handle_connect():
    # 从 Supabase 获取所有贴纸
    response = supabase.table('stickers').select('*').order('id').execute()
    stickers = response.data
    emit('init_stickers', {'stickers': stickers})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('submit_sticker')
def handle_submit_sticker(data):
    content = data.get('content', '').strip()
    color = data.get('color', 'red')
    
    if not content:
        emit('error', {'message': '请输入内容'})
        return
    
    # 创建贴纸数据
    sticker_data = {
        'content': content,
        'color': color,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 保存到 Supabase
    response = supabase.table('stickers').insert(sticker_data).execute()
    
    if response.data:
        sticker = response.data[0]
        emit('new_sticker', sticker, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

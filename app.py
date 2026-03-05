import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import csv
import io

app = Flask(__name__)

# 使用环境变量或默认密钥
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'brainstorm-secret-key-prod')

# 配置SocketIO，启用CORS（不使用eventlet以避免兼容性问题）
socketio = SocketIO(app, cors_allowed_origins="*")

# 存储贴纸数据（注意：免费平台重启后会重置）
stickers = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """健康检查路由"""
    return jsonify({'status': 'ok'}), 200

@app.route('/export')
def export():
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
    
    sticker = {
        'id': len(stickers) + 1,
        'content': content,
        'color': color,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    stickers.append(sticker)
    emit('new_sticker', sticker, broadcast=True)

if __name__ == '__main__':
    # 本地开发环境
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

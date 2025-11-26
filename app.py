#!/usr/bin/env python3
"""
Polymarket Web Application - Flask Backend
提供REST API接口和市场数据服务
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api

from api.routes import api_bp
from config import config as app_config


def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__,
                static_folder='frontend',
                static_url_path='',
                template_folder='frontend')

    # 配置CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
            "methods": ["GET", "POST", "PUT", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # 配置限流
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["100 per minute"]
    )
    limiter.init_app(app)

    # 注册API蓝图
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # 首页路由
    @app.route('/')
    def index():
        """首页 - 市场列表界面"""
        return render_template('index.html')

    @app.route('/settings')
    def settings():
        """设置页面"""
        return render_template('settings.html')

    @app.route('/about')
    def about():
        """关于页面"""
        return render_template('about.html')

    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': '请求的资源不存在'
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': '服务器内部错误'
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 500

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'success': False,
            'error': {
                'code': 'RATE_LIMIT_EXCEEDED',
                'message': f'请求频率超限: {e.description}'
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 429

    return app


if __name__ == '__main__':
    # 验证配置
    if not app_config.validate():
        print("配置验证失败，请检查环境变量设置")
        exit(1)

    # 创建应用
    app = create_app()

    # 运行应用
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    port = int(os.getenv('PORT', 5000))

    print(f"启动Polymarket Web应用...")
    print(f"访问地址: http://localhost:{port}")
    print(f"调试模式: {debug_mode}")

    app.run(host='0.0.0.0', port=port, debug=debug_mode)
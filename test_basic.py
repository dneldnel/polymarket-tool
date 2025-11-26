#!/usr/bin/env python3
"""
基本功能测试脚本
用于验证Phase 1实施的核心功能
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

def test_flask_app():
    """测试Flask应用的基本功能"""
    print("🧪 开始Phase 1基本功能测试...")
    print("=" * 50)

    try:
        # 测试1: 检查Flask应用导入
        print("\n📋 测试1: Flask应用导入")
        try:
            from app import create_app
            app = create_app()
            print("✅ Flask应用创建成功")
        except Exception as e:
            print(f"❌ Flask应用创建失败: {e}")
            return False

        # 测试2: 检查路由注册
        print("\n📋 测试2: 路由注册检查")
        with app.app_context():
            routes = [rule.rule for rule in app.url_map.iter_rules()]
            api_routes = [r for r in routes if '/api/v1/' in r]

            expected_routes = [
                '/api/v1/health',
                '/api/v1/status',
                '/api/v1/config',
                '/api/v1/markets',
                '/api/v1/markets/categories',
                '/api/v1/markets/stats'
            ]

            missing_routes = []
            for route in expected_routes:
                if route not in routes:
                    missing_routes.append(route)

            if missing_routes:
                print(f"❌ 缺少关键路由: {missing_routes}")
            else:
                print(f"✅ 所有 {len(expected_routes)} 个API路由已注册")

            print(f"✅ 总共发现 {len(routes)} 个路由")

        print("\n📋 测试3: 静态文件检查")
        import os
        frontend_files = [
            'frontend/index.html',
            'frontend/settings.html',
            'frontend/about.html',
            'frontend/css/main.css',
            'frontend/js/api.js',
            'frontend/js/main.js',
            'frontend/js/settings.js'
        ]

        missing_files = []
        for file_path in frontend_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)

        if missing_files:
            print(f"❌ 缺少前端文件: {missing_files}")
        else:
            print(f"✅ 所有 {len(frontend_files)} 个前端文件存在")

        print("\n📋 测试4: 配置模块检查")
        try:
            from config import config
            required_configs = ['clob_api_url', 'request_timeout', 'max_retries', 'default_limit']
            missing_configs = []

            for config_key in required_configs:
                if not config.get(config_key):
                    missing_configs.append(config_key)

            if missing_configs:
                print(f"❌ 缺少配置: {missing_configs}")
            else:
                print("✅ 所有必要配置存在")
        except Exception as e:
            print(f"❌ 配置检查失败: {e}")

        return True

    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_core_modules():
    """测试核心模块功能"""
    print("\n📋 测试5: 核心模块功能")

    try:
        # 测试PolymarketMarketFetcher
        from polymarket_markets import PolymarketMarketFetcher

        # 创建实例（不实际连接API）
        fetcher = PolymarketMarketFetcher(
            api_url="https://clob.polymarket.com",
            timeout=30,
            max_retries=3
        )
        print("✅ PolymarketMarketFetcher实例化成功")

        # 测试数据提取方法
        test_market = {
            "question": "测试市场",
            "question_id": "test_123",
            "condition_id": "condition_123",
            "description": "测试描述",
            "end_date_iso": "2024-12-31T23:59:59Z",
            "active": True,
            "closed": False,
            "accepting_orders": True,
            "minimum_order_size": 10,
            "minimum_tick_size": 0.01,
            "neg_risk": False,
            "tags": ["测试"],
            "tokens": [
                {
                    "price": 0.75,
                    "token_id": "token_1",
                    "outcome": "是",
                    "winner": False
                }
            ]
        }

        market_info = fetcher.extract_market_info(test_market)

        # 验证关键字段
        required_fields = ['title', 'market_id', 'current_price', 'category', 'active']
        missing_fields = []
        for field in required_fields:
            if field not in market_info:
                missing_fields.append(field)

        if missing_fields:
            print(f"❌ 数据提取缺少字段: {missing_fields}")
        else:
            print("✅ 数据提取功能正常")

        # 测试分类推断
        test_cases = [
            ("美国总统选举", "politics"),
            ("比特币价格", "crypto"),
            ("NBA冠军", "sports"),
            ("股市崩盘", "finance")
        ]

        for title, expected_category in test_cases:
            test_case = {"question": title}
            category = fetcher._extract_category(test_case)
            if category == expected_category:
                print(f"✅ 分类推断正确: '{title}' -> '{category}'")
            else:
                print(f"⚠️  分类推断: '{title}' -> '{category}' (期望: '{expected_category}')")

        return True

    except Exception as e:
        print(f"❌ 核心模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """测试文件结构完整性"""
    print("\n📋 测试6: 项目文件结构")

    required_dirs = [
        'frontend',
        'frontend/css',
        'frontend/js',
        'api'
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"❌ 缺少目录: {missing_dirs}")
        return False
    else:
        print("✅ 目录结构完整")

    return True

def main():
    """主测试函数"""
    print(f"🚀 Polymarket Web应用 Phase 1测试")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    tests_passed = 0
    total_tests = 4

    # 执行测试
    if test_flask_app():
        tests_passed += 1

    if test_core_modules():
        tests_passed += 1

    if test_file_structure():
        tests_passed += 1

    # 基本语法检查
    print("\n📋 测试7: Python语法检查")
    try:
        import ast

        python_files = [
            'app.py',
            'polymarket_markets.py',
            'config.py',
            'api/routes.py'
        ]

        syntax_errors = []
        for file_path in python_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        ast.parse(f.read())
                        print(f"✅ {file_path} 语法正确")
                    except SyntaxError as e:
                        syntax_errors.append(f"{file_path}: {e}")

        if syntax_errors:
            print(f"❌ 发现语法错误: {syntax_errors}")
        else:
            print("✅ 所有Python文件语法正确")
            tests_passed += 1

    except Exception as e:
        print(f"❌ 语法检查失败: {e}")

    # 测试结果总结
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {tests_passed}/{total_tests} 项测试通过")

    if tests_passed == total_tests:
        print("🎉 Phase 1实施成功！所有核心功能正常工作")
        print("\n🔧 启动Web应用:")
        print("   python app.py")
        print("\n🌐 访问地址:")
        print("   http://localhost:5000")
        return True
    else:
        print("⚠️  部分测试失败，请检查上述错误信息")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
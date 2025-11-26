"""
API路由定义
提供RESTful API端点用于市场数据访问
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask import Flask
from polymarket_markets import PolymarketMarketFetcher
from config import config as app_config

# 创建API蓝图
api_bp = Blueprint('api', __name__)

# 全局市场获取器实例
market_fetcher = None


def get_market_fetcher():
    """获取市场数据获取器实例"""
    global market_fetcher
    if market_fetcher is None:
        market_fetcher = PolymarketMarketFetcher(
            api_url=app_config.get("clob_api_url"),
            timeout=app_config.get("request_timeout", 30),
            max_retries=app_config.get("max_retries", 3)
        )
    return market_fetcher


def create_response(success=True, data=None, message="操作成功", error=None):
    """创建标准API响应格式"""
    response = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat()
    }

    if success:
        response['data'] = data
        response['message'] = message
    else:
        response['error'] = error

    return response


@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    try:
        fetcher = get_market_fetcher()
        # 简单测试API连接
        test_markets = fetcher.get_markets(limit=1)

        return jsonify(create_response(
            success=True,
            data={
                'status': 'healthy',
                'clob_api_connected': bool(test_markets),
                'timestamp': datetime.utcnow().isoformat()
            },
            message="系统运行正常"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'HEALTH_CHECK_FAILED',
                'message': f'健康检查失败: {str(e)}'
            }
        )), 500


@api_bp.route('/status', methods=['GET'])
def system_status():
    """系统状态端点"""
    try:
        fetcher = get_market_fetcher()

        # 获取系统信息
        system_info = {
            'application': 'Polymarket Web Tool',
            'version': '1.0.0',
            'environment': app_config.get('flask_env', 'production'),
            'clob_api_url': app_config.get('clob_api_url'),
            'request_timeout': app_config.get('request_timeout', 30),
            'max_retries': app_config.get('max_retries', 3),
            'default_limit': app_config.get('default_limit', 50)
        }

        return jsonify(create_response(
            success=True,
            data=system_info,
            message="系统状态获取成功"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'STATUS_FETCH_FAILED',
                'message': f'状态获取失败: {str(e)}'
            }
        )), 500


@api_bp.route('/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    try:
        # 返回非敏感配置信息
        safe_config = {
            'clob_api_url': app_config.get('clob_api_url'),
            'request_timeout': app_config.get('request_timeout', 30),
            'max_retries': app_config.get('max_retries', 3),
            'default_limit': app_config.get('default_limit', 50),
            'log_level': app_config.get('log_level', 'INFO')
        }

        return jsonify(create_response(
            success=True,
            data=safe_config,
            message="配置获取成功"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'CONFIG_FETCH_FAILED',
                'message': f'配置获取失败: {str(e)}'
            }
        )), 500


@api_bp.route('/config', methods=['PUT'])
def update_config():
    """更新配置"""
    try:
        config_data = request.get_json()

        if not config_data:
            return jsonify(create_response(
                success=False,
                error={
                    'code': 'INVALID_REQUEST',
                    'message': '请求体不能为空'
                }
            )), 400

        # 验证并更新配置
        updatable_fields = [
            'request_timeout', 'max_retries',
            'default_limit', 'log_level'
        ]

        updated_fields = []
        for field in updatable_fields:
            if field in config_data:
                value = config_data[field]

                # 基本验证
                if field in ['request_timeout', 'max_retries', 'default_limit']:
                    if not isinstance(value, int) or value <= 0:
                        return jsonify(create_response(
                            success=False,
                            error={
                                'code': 'INVALID_VALUE',
                                'message': f'{field} 必须是正整数'
                            }
                        )), 400

                app_config.set(field, value)
                updated_fields.append(field)

        return jsonify(create_response(
            success=True,
            data={
                'updated_fields': updated_fields,
                'current_config': {
                    'clob_api_url': app_config.get('clob_api_url'),
                    'request_timeout': app_config.get('request_timeout', 30),
                    'max_retries': app_config.get('max_retries', 3),
                    'default_limit': app_config.get('default_limit', 50),
                    'log_level': app_config.get('log_level', 'INFO')
                }
            },
            message=f"配置更新成功: {', '.join(updated_fields)}"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'CONFIG_UPDATE_FAILED',
                'message': f'配置更新失败: {str(e)}'
            }
        )), 500


@api_bp.route('/markets', methods=['GET'])
def get_markets():
    """获取市场列表（支持分页和筛选）"""
    try:
        fetcher = get_market_fetcher()

        # 获取查询参数
        limit = request.args.get('limit', type=int)
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', type=str)
        active_only = request.args.get('active_only', type=lambda v: v.lower() == 'true')

        # 设置默认限制
        if limit is None:
            limit = app_config.get('default_limit', 50)

        # 验证参数
        if limit and limit > 1000:
            return jsonify(create_response(
                success=False,
                error={
                    'code': 'INVALID_LIMIT',
                    'message': 'limit不能超过1000'
                }
            )), 400

        if page and page < 1:
            return jsonify(create_response(
                success=False,
                error={
                    'code': 'INVALID_PAGE',
                    'message': 'page必须大于0'
                }
            )), 400

        # 获取原始市场数据
        raw_markets = fetcher.get_markets(limit=None if limit == -1 else limit)

        if not raw_markets:
            return jsonify(create_response(
                success=True,
                data={
                    'markets': [],
                    'pagination': {
                        'page': page,
                        'limit': limit,
                        'total': 0,
                        'total_pages': 0,
                        'has_more': False
                    }
                },
                message="未获取到市场数据"
            )), 200

        # 提取市场信息
        markets_info = []
        for market in raw_markets:
            market_info = fetcher.extract_market_info(market)
            markets_info.append(market_info)

        # 应用筛选条件
        if category:
            markets_info = [m for m in markets_info if m.get('category', '').lower() == category.lower()]

        if active_only:
            markets_info = [m for m in markets_info if m.get('active', False)]

        # 应用分页
        total = len(markets_info)
        page_size = limit if limit and limit > 0 else total
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        paginated_markets = markets_info[start_idx:end_idx]
        has_more = end_idx < total

        return jsonify(create_response(
            success=True,
            data={
                'markets': paginated_markets,
                'pagination': {
                    'page': page,
                    'limit': page_size,
                    'total': total,
                    'total_pages': total_pages,
                    'has_more': has_more
                },
                'filters_applied': {
                    'category': category,
                    'active_only': active_only
                }
            },
            message=f"成功获取 {len(paginated_markets)} 个市场数据"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'MARKETS_FETCH_FAILED',
                'message': f'获取市场数据失败: {str(e)}'
            }
        )), 500


@api_bp.route('/markets/<market_id>', methods=['GET'])
def get_market_detail(market_id):
    """获取单个市场详情"""
    try:
        fetcher = get_market_fetcher()

        # 获取所有市场数据
        raw_markets = fetcher.get_markets(limit=None)

        if not raw_markets:
            return jsonify(create_response(
                success=False,
                error={
                    'code': 'NO_MARKETS_DATA',
                    'message': '无法获取市场数据'
                }
            )), 404

        # 查找指定市场
        target_market = None
        for market in raw_markets:
            market_info = fetcher.extract_market_info(market)
            if market_info.get('market_id') == market_id or market_info.get('condition_id') == market_id:
                target_market = market_info
                break

        if not target_market:
            return jsonify(create_response(
                success=False,
                error={
                    'code': 'MARKET_NOT_FOUND',
                    'message': f'未找到市场ID: {market_id}'
                }
            )), 404

        return jsonify(create_response(
            success=True,
            data=target_market,
            message="市场详情获取成功"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'MARKET_DETAIL_FAILED',
                'message': f'获取市场详情失败: {str(e)}'
            }
        )), 500


@api_bp.route('/markets/categories', methods=['GET'])
def get_market_categories():
    """获取所有市场分类"""
    try:
        fetcher = get_market_fetcher()

        # 获取少量市场数据来推断分类
        raw_markets = fetcher.get_markets(limit=100)

        if not raw_markets:
            return jsonify(create_response(
                success=True,
                data={
                    'categories': []
                },
                message="未获取到市场数据，无法推断分类"
            )), 200

        # 提取所有分类
        categories = set()
        for market in raw_markets:
            market_info = fetcher.extract_market_info(market)
            category = market_info.get('category', 'other')
            categories.add(category)

        # 统计各分类的市场数量
        category_counts = {}
        for category in categories:
            category_counts[category] = 0

        for market in raw_markets:
            market_info = fetcher.extract_market_info(market)
            category = market_info.get('category', 'other')
            category_counts[category] += 1

        # 按数量排序
        sorted_categories = sorted(
            category_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        result = [
            {
                'name': category,
                'count': count,
                'display_name': {
                    'politics': '政治',
                    'sports': '体育',
                    'crypto': '加密货币',
                    'finance': '金融',
                    'other': '其他'
                }.get(category, category)
            }
            for category, count in sorted_categories
        ]

        return jsonify(create_response(
            success=True,
            data={
                'categories': result,
                'total_categories': len(result)
            },
            message=f"成功获取 {len(result)} 个市场分类"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'CATEGORIES_FETCH_FAILED',
                'message': f'获取分类失败: {str(e)}'
            }
        )), 500


@api_bp.route('/markets/stats', methods=['GET'])
def get_market_stats():
    """获取市场统计信息"""
    try:
        fetcher = get_market_fetcher()

        # 获取市场数据
        raw_markets = fetcher.get_markets(limit=1000)

        if not raw_markets:
            return jsonify(create_response(
                success=True,
                data={
                    'total_markets': 0,
                    'active_markets': 0,
                    'closed_markets': 0,
                    'categories': {}
                },
                message="无市场数据"
            )), 200

        # 统计信息
        total_markets = len(raw_markets)
        active_markets = 0
        closed_markets = 0
        category_counts = {}
        accepting_orders = 0

        for market in raw_markets:
            market_info = fetcher.extract_market_info(market)

            if market_info.get('active', False):
                active_markets += 1

            if market_info.get('closed', False):
                closed_markets += 1

            if market_info.get('accepting_orders', False):
                accepting_orders += 1

            category = market_info.get('category', 'other')
            category_counts[category] = category_counts.get(category, 0) + 1

        stats = {
            'total_markets': total_markets,
            'active_markets': active_markets,
            'closed_markets': closed_markets,
            'accepting_orders': accepting_orders,
            'categories': category_counts,
            'last_updated': datetime.utcnow().isoformat()
        }

        return jsonify(create_response(
            success=True,
            data=stats,
            message="市场统计信息获取成功"
        )), 200

    except Exception as e:
        return jsonify(create_response(
            success=False,
            error={
                'code': 'STATS_FETCH_FAILED',
                'message': f'获取统计信息失败: {str(e)}'
            }
        )), 500
#!/usr/bin/env python3
"""
调试脚本 - 测试extract_market_info方法的行为
"""

import json
import logging
from polymarket_markets import PolymarketMarketFetcher

def debug_extract_info():
    """调试extract_market_info方法"""
    print("=== 调试extract_market_info方法 ===")
    
    # 创建获取器并设置详细日志
    fetcher = PolymarketMarketFetcher()
    fetcher.logger.setLevel(logging.DEBUG)
    
    # 初始化客户端
    if not fetcher.initialize_client():
        print("初始化客户端失败")
        return
    
    # 获取市场数据
    print("正在获取市场数据...")
    markets_data = fetcher.client.get_markets()
    
    if not markets_data or "data" not in markets_data:
        print("未获取到市场数据")
        return
    
    markets = markets_data["data"]
    print(f"获取到 {len(markets)} 个市场")
    
    # 测试前3个市场的数据提取
    for i, market in enumerate(markets[:3]):
        print(f"\n{'='*80}")
        print(f"测试市场 {i+1}:")
        print(f"{'='*80}")
        
        # 显示原始数据的关键字段
        print("原始数据关键字段:")
        key_fields = ['question', 'description', 'category', 'tokens', 'active', 'closed']
        for field in key_fields:
            if field in market:
                value = market[field]
                if field == 'tokens' and isinstance(value, list):
                    print(f"  {field}: {len(value)} 个代币")
                    if value:
                        print(f"    第一个代币: {json.dumps(value[0], ensure_ascii=False)}")
                else:
                    print(f"  {field}: {value}")
            else:
                print(f"  {field}: [缺失]")
        
        # 提取市场信息
        print("\n提取的市场信息:")
        market_info = fetcher.extract_market_info(market)
        
        # 显示提取的信息
        info_fields = ['title', 'description', 'category', 'current_price', 'price_range', 'end_date_formatted', 'active', 'closed']
        for field in info_fields:
            if field in market_info:
                print(f"  {field}: {market_info[field]}")
            else:
                print(f"  {field}: [缺失]")
    
    # 测试边界情况
    print(f"\n{'='*80}")
    print("测试边界情况:")
    print(f"{'='*80}")
    
    # 测试空数据
    print("\n1. 测试空字典:")
    empty_market = {}
    empty_info = fetcher.extract_market_info(empty_market)
    print(f"  结果: {empty_info}")
    
    # 测试只有部分字段的数据
    print("\n2. 测试只有部分字段:")
    partial_market = {
        "question": "测试问题",
        "active": True,
        "closed": False
    }
    partial_info = fetcher.extract_market_info(partial_market)
    print(f"  结果: {partial_info}")
    
    # 测试没有tokens的数据
    print("\n3. 测试没有tokens的数据:")
    no_tokens_market = {
        "question": "无代币市场",
        "description": "这是一个没有代币的市场",
        "active": True,
        "closed": False
    }
    no_tokens_info = fetcher.extract_market_info(no_tokens_market)
    print(f"  结果: {no_tokens_info}")
    
    # 测试有tokens但价格为空的数据
    print("\n4. 测试有tokens但价格为空的数据:")
    weird_tokens_market = {
        "question": "奇怪代币市场",
        "active": True,
        "closed": False,
        "tokens": [
            {"outcome": "是", "price": None},
            {"outcome": "否", "price": ""}
        ]
    }
    weird_tokens_info = fetcher.extract_market_info(weird_tokens_market)
    print(f"  结果: {weird_tokens_info}")

if __name__ == "__main__":
    debug_extract_info()
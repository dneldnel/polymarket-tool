#!/usr/bin/env python3
"""
调试脚本 - 查看API返回的实际数据结构
"""

import json
from py_clob_client.client import ClobClient

def debug_api_response():
    """调试API响应数据结构"""
    print("=== 调试API响应数据结构 ===")
    
    # 创建客户端
    client = ClobClient("https://clob.polymarket.com")
    
    # 获取市场数据
    print("正在获取市场数据...")
    markets_data = client.get_simplified_markets()
    
    if not markets_data:
        print("错误: 未能获取到市场数据")
        return
    
    print(f"API响应类型: {type(markets_data)}")
    print(f"API响应键: {markets_data.keys() if isinstance(markets_data, dict) else 'N/A'}")
    
    if "data" in markets_data:
        markets = markets_data["data"]
        print(f"市场数据类型: {type(markets)}")
        print(f"市场数量: {len(markets) if isinstance(markets, list) else 'N/A'}")
        
        if markets and len(markets) > 0:
            # 显示第一个市场的完整结构
            first_market = markets[0]
            print(f"\n第一个市场的数据结构:")
            print(f"类型: {type(first_market)}")
            print(f"键: {first_market.keys() if isinstance(first_market, dict) else 'N/A'}")
            
            print(f"\n第一个市场的完整数据:")
            print(json.dumps(first_market, indent=2, ensure_ascii=False))
            
            # 显示前3个市场的基本信息
            print(f"\n前3个市场的基本信息:")
            for i, market in enumerate(markets[:3]):
                print(f"\n市场 {i+1}:")
                if isinstance(market, dict):
                    for key, value in market.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  市场类型: {type(market)}")
                    print(f"  市场内容: {market}")
        else:
            print("市场数据为空")
    else:
        print("API响应中没有'data'字段")
        print("完整API响应:")
        print(json.dumps(markets_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    debug_api_response()
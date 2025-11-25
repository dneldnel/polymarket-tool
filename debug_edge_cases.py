#!/usr/bin/env python3
"""
调试脚本 - 测试可能导致"未知标题"的边缘情况
"""

import json
from polymarket_markets import PolymarketMarketFetcher

def debug_edge_cases():
    """调试可能导致问题的边缘情况"""
    print("=== 调试边缘情况 ===")
    
    # 创建获取器
    fetcher = PolymarketMarketFetcher()
    
    # 模拟各种可能导致"未知标题"的情况
    edge_cases = [
        {
            "name": "完全空的market",
            "market": {}
        },
        {
            "name": "question字段为None",
            "market": {"question": None}
        },
        {
            "name": "question字段为空字符串",
            "market": {"question": ""}
        },
        {
            "name": "question字段不存在",
            "market": {"description": "只有描述"}
        },
        {
            "name": "tokens为空列表",
            "market": {
                "question": "正常标题",
                "tokens": []
            }
        },
        {
            "name": "tokens为None",
            "market": {
                "question": "正常标题",
                "tokens": None
            }
        },
        {
            "name": "tokens中有异常价格数据",
            "market": {
                "question": "正常标题",
                "tokens": [
                    {"outcome": "是", "price": None},
                    {"outcome": "否", "price": ""}
                ]
            }
        },
        {
            "name": "正常数据但active字段异常",
            "market": {
                "question": "正常标题",
                "active": None,
                "closed": None,
                "tokens": [
                    {"outcome": "是", "price": 0.5},
                    {"outcome": "否", "price": 0.5}
                ]
            }
        }
    ]
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"\n{'='*80}")
        print(f"测试案例 {i}: {test_case['name']}")
        print(f"{'='*80}")
        
        print("输入数据:")
        print(json.dumps(test_case['market'], indent=2, ensure_ascii=False))
        
        print("\n提取结果:")
        try:
            market_info = fetcher.extract_market_info(test_case['market'])
            
            # 检查关键字段
            key_fields = ['title', 'current_price', 'price_range', 'category', 'active', 'closed']
            for field in key_fields:
                value = market_info.get(field, '缺失')
                print(f"  {field}: {value}")
                
            # 检查是否出现"未知标题"
            if market_info.get('title') == '未知标题':
                print("  ⚠️  警告: 出现未知标题!")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
    
    # 测试真实API中可能存在的问题数据
    print(f"\n{'='*80}")
    print("测试真实API数据中的潜在问题")
    print(f"{'='*80}")
    
    # 初始化客户端并获取真实数据
    if fetcher.initialize_client():
        try:
            markets_data = fetcher.client.get_markets()
            if markets_data and "data" in markets_data:
                markets = markets_data["data"]
                print(f"获取到 {len(markets)} 个真实市场数据")
                
                # 查找可能有问题的市场
                problem_markets = []
                for i, market in enumerate(markets[:50]):  # 只检查前50个
                    question = market.get("question", "")
                    tokens = market.get("tokens", [])
                    
                    # 检查潜在问题
                    has_issue = False
                    issue_desc = []
                    
                    if not question or question.strip() == "":
                        has_issue = True
                        issue_desc.append("空标题")
                    
                    if not tokens:
                        has_issue = True
                        issue_desc.append("无代币")
                    else:
                        # 检查代币价格
                        for j, token in enumerate(tokens):
                            price = token.get("price")
                            if price is None or price == "":
                                has_issue = True
                                issue_desc.append(f"代币{j+1}价格异常")
                    
                    if has_issue:
                        problem_markets.append((i, market, issue_desc))
                
                print(f"\n发现 {len(problem_markets)} 个可能有问题的市场:")
                for i, (idx, market, issues) in enumerate(problem_markets[:5]):  # 只显示前5个
                    print(f"\n问题市场 {i+1} (索引 {idx}):")
                    print(f"  问题: {', '.join(issues)}")
                    print(f"  标题: {market.get('question', '无标题')}")
                    print(f"  代币数: {len(market.get('tokens', []))}")
                    
                    # 测试这个有问题的市场
                    try:
                        market_info = fetcher.extract_market_info(market)
                        print(f"  提取结果: title='{market_info.get('title')}', price={market_info.get('current_price')}")
                    except Exception as e:
                        print(f"  提取错误: {e}")
                        
        except Exception as e:
            print(f"获取真实数据失败: {e}")
    else:
        print("无法初始化客户端")

if __name__ == "__main__":
    debug_edge_cases()
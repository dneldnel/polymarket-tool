#!/usr/bin/env python3
"""
调试脚本 - 专门测试价格处理问题
"""

def test_price_processing():
    """测试价格处理的边界情况"""
    print("=== 测试价格处理问题 ===")
    
    # 模拟不同的代币价格情况
    test_cases = [
        {
            "name": "正常价格",
            "tokens": [
                {"outcome": "是", "price": 0.65},
                {"outcome": "否", "price": 0.35}
            ]
        },
        {
            "name": "包含None价格",
            "tokens": [
                {"outcome": "是", "price": None},
                {"outcome": "否", "price": 0.35}
            ]
        },
        {
            "name": "包含空字符串价格",
            "tokens": [
                {"outcome": "是", "price": ""},
                {"outcome": "否", "price": 0.35}
            ]
        },
        {
            "name": "所有价格都是None",
            "tokens": [
                {"outcome": "是", "price": None},
                {"outcome": "否", "price": None}
            ]
        },
        {
            "name": "混合问题价格",
            "tokens": [
                {"outcome": "是", "price": None},
                {"outcome": "否", "price": ""},
                {"outcome": "可能", "price": 0.5}
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n测试案例: {test_case['name']}")
        tokens = test_case['tokens']
        
        try:
            # 当前的有问题的实现
            prices = [token.get("price", 0) for token in tokens]
            print(f"  提取的价格: {prices}")
            price_range = f"{min(prices):.4f} - {max(prices):.4f}"
            print(f"  价格范围: {price_range}")
        except Exception as e:
            print(f"  错误: {e}")
        
        try:
            # 修复后的实现
            prices = []
            for token in tokens:
                price = token.get("price", 0)
                # 处理None和空字符串
                if price is None or price == "":
                    price = 0
                # 确保是数字
                try:
                    price = float(price)
                except (ValueError, TypeError):
                    price = 0
                prices.append(price)
            
            print(f"  修复后提取的价格: {prices}")
            if prices:
                price_range = f"{min(prices):.4f} - {max(prices):.4f}"
                print(f"  修复后价格范围: {price_range}")
            else:
                print(f"  修复后价格范围: 无数据")
        except Exception as e:
            print(f"  修复后错误: {e}")

if __name__ == "__main__":
    test_price_processing()
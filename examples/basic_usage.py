#!/usr/bin/env python3
"""
基本使用示例
演示如何使用Polymarket市场数据获取工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polymarket_markets import PolymarketMarketFetcher


def example_basic_usage():
    """基本使用示例"""
    print("=== Polymarket市场数据获取工具 - 基本使用示例 ===")
    
    # 创建市场获取器
    fetcher = PolymarketMarketFetcher()
    
    # 获取前10个市场
    print("\n1. 获取前10个市场:")
    markets = fetcher.get_simplified_markets(limit=10)
    
    if markets:
        # 提取关键信息
        markets_info = []
        for market in markets:
            market_info = fetcher.extract_market_info(market)
            markets_info.append(market_info)
        
        # 显示结果
        fetcher.display_markets_table(markets_info)
    else:
        print("未能获取到市场数据")


def example_with_filtering():
    """筛选功能示例"""
    print("\n=== 筛选功能示例 ===")
    
    fetcher = PolymarketMarketFetcher()
    
    # 获取所有市场
    markets = fetcher.get_simplified_markets(limit=None)
    
    if markets:
        # 提取关键信息
        markets_info = []
        for market in markets:
            market_info = fetcher.extract_market_info(market)
            markets_info.append(market_info)
        
        # 按分类统计
        categories = {}
        for market in markets_info:
            category = market.get("category", "未知")
            categories[category] = categories.get(category, 0) + 1
        
        print("\n市场分类统计:")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}个市场")
        
        # 显示活跃市场数量
        active_markets = sum(1 for market in markets_info if market.get("active", False))
        print(f"\n活跃市场: {active_markets}/{len(markets_info)}")


def example_export_data():
    """数据导出示例"""
    print("\n=== 数据导出示例 ===")
    
    fetcher = PolymarketMarketFetcher()
    
    # 获取前5个市场并导出
    markets = fetcher.get_simplified_markets(limit=5)
    
    if markets:
        markets_info = []
        for market in markets:
            market_info = fetcher.extract_market_info(market)
            markets_info.append(market_info)
        
        # 导出到JSON文件
        filename = "example_markets.json"
        fetcher.export_to_json(markets_info, filename)
        print(f"数据已导出到: {filename}")


if __name__ == "__main__":
    # 运行所有示例
    example_basic_usage()
    example_with_filtering()
    example_export_data()
    
    print("\n=== 示例完成 ===")
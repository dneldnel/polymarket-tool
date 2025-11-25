#!/usr/bin/env python3
"""
Polymarket 市场数据获取工具 - 主入口
获取Polymarket上所有可下注的预测市场标题和基本信息
"""

import argparse
import sys
from datetime import datetime

from polymarket_markets import PolymarketMarketFetcher
from config import config


def setup_argparse() -> argparse.ArgumentParser:
    """设置命令行参数解析"""
    parser = argparse.ArgumentParser(
        description="Polymarket 市场数据获取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py                          # 显示前50个市场
  python main.py -l 20                    # 显示前20个市场
  python main.py --all                    # 显示所有市场
  python main.py --export-json            # 导出数据到JSON文件
  python main.py --category politics      # 只显示政治类市场
  python main.py --show-config            # 显示当前配置
  python main.py --api-url https://clob.polymarket.com  # 自定义API URL
        """
    )
    
    parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=config.get("default_limit", 50),
        help=f"限制显示的市场数量 (默认: {config.get('default_limit', 50)})"
    )
    
    parser.add_argument(
        "--all", 
        action="store_true",
        help="显示所有市场（忽略限制）"
    )
    
    parser.add_argument(
        "--export-json", 
        action="store_true",
        help="导出数据到JSON文件"
    )
    
    parser.add_argument(
        "--category",
        type=str,
        help="按分类筛选市场（如: politics, sports, crypto等）"
    )
    
    parser.add_argument(
        "--active-only",
        action="store_true",
        help="只显示活跃市场"
    )
    
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="显示当前配置"
    )
    
    parser.add_argument(
        "--api-url",
        type=str,
        help="自定义CLOB API URL"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出模式"
    )
    
    return parser


def filter_markets_by_category(markets_info: list, category: str) -> list:
    """按分类筛选市场"""
    if not category:
        return markets_info
    
    filtered = [market for market in markets_info if market.get("category", "").lower() == category.lower()]
    return filtered


def filter_active_markets(markets_info: list) -> list:
    """筛选活跃市场"""
    return [market for market in markets_info if market.get("active", False)]


def main():
    """主函数"""
    parser = setup_argparse()
    args = parser.parse_args()
    
    # 显示配置
    if args.show_config:
        config.print_config()
        return
    
    # 验证配置
    if not config.validate():
        print("配置验证失败，请检查环境变量设置")
        sys.exit(1)
    
    # 更新API URL（如果通过命令行指定）
    if args.api_url:
        config.set("clob_api_url", args.api_url)
    
    print(f"{'='*80}")
    print("Polymarket 市场数据获取工具")
    print(f"{'='*80}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建市场获取器
    fetcher = PolymarketMarketFetcher(
        api_url=config.get("clob_api_url"),
        timeout=config.get("request_timeout", 30),
        max_retries=config.get("max_retries", 3)
    )
    
    # 设置日志级别
    if args.verbose:
        fetcher.logger.setLevel("DEBUG")
    
    # 获取市场数据
    limit = None if args.all else args.limit
    markets = fetcher.get_markets(limit)
    
    if not markets:
        print("错误: 未能获取到市场数据")
        sys.exit(1)
    
    # 提取关键信息
    markets_info = []
    for market in markets:
        market_info = fetcher.extract_market_info(market)
        markets_info.append(market_info)
    
    # 应用筛选条件
    if args.category:
        markets_info = filter_markets_by_category(markets_info, args.category)
        print(f"按分类 '{args.category}' 筛选，剩余 {len(markets_info)} 个市场")
    
    if args.active_only:
        markets_info = filter_active_markets(markets_info)
        print(f"筛选活跃市场，剩余 {len(markets_info)} 个市场")
    
    # 显示结果
    if markets_info:
        fetcher.display_markets_table(markets_info)
        
        # 导出数据
        if args.export_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"polymarket_markets_{timestamp}.json"
            fetcher.export_to_json(markets_info, filename)
    else:
        print("没有符合筛选条件的市场数据")
    
    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
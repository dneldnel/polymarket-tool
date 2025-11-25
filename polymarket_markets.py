#!/usr/bin/env python3
"""
Polymarket Market Data Fetcher
获取Polymarket上所有可下注的预测市场标题和基本信息
"""

import os
import sys
import json
import logging
import argparse
from typing import List, Dict, Optional
from datetime import datetime

import requests
from dotenv import load_dotenv
from tabulate import tabulate

# 尝试导入py-clob-client，如果失败则提供安装提示
try:
    from py_clob_client.client import ClobClient
    from py_clob_client.constants import AMOY
except ImportError:
    print("错误: 未找到py-clob-client库")
    print("请运行: pip install py-clob-client")
    sys.exit(1)


class PolymarketMarketFetcher:
    """Polymarket市场数据获取器"""
    
    def __init__(self, api_url: str = None, timeout: int = 30, max_retries: int = 3):
        """
        初始化市场数据获取器
        
        Args:
            api_url: CLOB API URL
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.api_url = api_url or os.getenv("CLOB_API_URL", "https://clob.polymarket.com")
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """设置日志记录"""
        logging.basicConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def initialize_client(self) -> bool:
        """初始化CLOB客户端"""
        try:
            self.client = ClobClient(self.api_url)
            self.logger.info(f"成功连接到Polymarket CLOB API: {self.api_url}")
            return True
        except Exception as e:
            self.logger.error(f"初始化CLOB客户端失败: {e}")
            return False
    
    def get_markets(self, limit: int = None) -> List[Dict]:
        """
        获取完整市场列表（包含标题、价格等信息）
        
        Args:
            limit: 限制返回的市场数量（None表示获取所有）
            
        Returns:
            市场数据列表
        """
        if not self.client:
            if not self.initialize_client():
                return []
        
        try:
            self.logger.info("正在获取完整市场列表...")
            markets_data = self.client.get_markets()
            
            if not markets_data or "data" not in markets_data:
                self.logger.warning("未获取到市场数据")
                return []
            
            markets = markets_data["data"]
            self.logger.info(f"成功获取到 {len(markets)} 个市场")
            
            # 如果指定了限制，则截取前N个市场
            if limit and len(markets) > limit:
                markets = markets[:limit]
                self.logger.info(f"限制显示前 {limit} 个市场")
            
            return markets
            
        except Exception as e:
            self.logger.error(f"获取市场数据失败: {e}")
            return []
    
    def get_simplified_markets(self, limit: int = None) -> List[Dict]:
        """
        获取简化市场列表（仅包含基本信息）
        
        Args:
            limit: 限制返回的市场数量（None表示获取所有）
            
        Returns:
            市场数据列表
        """
        if not self.client:
            if not self.initialize_client():
                return []
        
        try:
            self.logger.info("正在获取简化市场列表...")
            markets_data = self.client.get_simplified_markets()
            
            if not markets_data or "data" not in markets_data:
                self.logger.warning("未获取到市场数据")
                return []
            
            markets = markets_data["data"]
            self.logger.info(f"成功获取到 {len(markets)} 个市场")
            
            # 如果指定了限制，则截取前N个市场
            if limit and len(markets) > limit:
                markets = markets[:limit]
                self.logger.info(f"限制显示前 {limit} 个市场")
            
            return markets
            
        except Exception as e:
            self.logger.error(f"获取市场数据失败: {e}")
            return []
    
    def extract_market_info(self, market: Dict) -> Dict:
        """
        从市场数据中提取关键信息
        
        Args:
            market: 原始市场数据
            
        Returns:
            提取的市场信息
        """
        try:
            # 基础信息
            question = market.get("question", "未知标题")
            if question is None or (isinstance(question, str) and question.strip() == ""):
                question = "未知标题"
            market_info = {
                "title": question,
                "description": market.get("description", "无描述"),
                "market_id": market.get("question_id", market.get("condition_id", "未知ID")),
                "condition_id": market.get("condition_id", "未知条件ID"),
                "category": self._extract_category(market),
                "volume": 0,  # 完整API响应中没有成交量数据
                "liquidity": 0,  # 完整API响应中没有流动性数据
                "end_date": market.get("end_date_iso"),
                "game_start_time": market.get("game_start_time"),
                "active": market.get("active", False),
                "closed": market.get("closed", False),
                "accepting_orders": market.get("accepting_orders", False),
                "minimum_order_size": market.get("minimum_order_size", 0),
                "minimum_tick_size": market.get("minimum_tick_size", 0),
                "neg_risk": market.get("neg_risk", False),
                "tags": market.get("tags", [])
            }
            
            # 处理代币信息
            tokens = market.get("tokens", [])
            if tokens:
                # 获取第一个代币的价格作为参考
                first_token = tokens[0]
                price = first_token.get("price", 0)
                # 处理None和空字符串
                if price is None or price == "":
                    price = 0
                # 确保是数字
                try:
                    price = float(price)
                except (ValueError, TypeError):
                    price = 0
                market_info["current_price"] = price
                market_info["token_id"] = first_token.get("token_id", "未知代币ID")
                market_info["outcome"] = first_token.get("outcome", "未知结果")
                market_info["winner"] = first_token.get("winner", False)
                
                # 计算所有代币的价格信息
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
                
                if prices:
                    market_info["price_range"] = f"{min(prices):.4f} - {max(prices):.4f}"
                else:
                    market_info["price_range"] = "无数据"
                market_info["total_tokens"] = len(tokens)
                
                # 如果有赢家，显示获胜结果
                winners = [token for token in tokens if token.get("winner", False)]
                if winners:
                    market_info["winning_outcome"] = winners[0].get("outcome", "未知")
                else:
                    market_info["winning_outcome"] = "未确定"
            else:
                market_info["current_price"] = 0
                market_info["token_id"] = "无代币"
                market_info["outcome"] = "无结果"
                market_info["winner"] = False
                market_info["price_range"] = "无数据"
                market_info["total_tokens"] = 0
                market_info["winning_outcome"] = "无数据"
            
            # 格式化日期
            if market_info["end_date"]:
                try:
                    end_date = datetime.fromisoformat(market_info["end_date"].replace('Z', '+00:00'))
                    market_info["end_date_formatted"] = end_date.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    market_info["end_date_formatted"] = market_info["end_date"]
            else:
                market_info["end_date_formatted"] = "无到期时间"
            
            # 格式化游戏开始时间
            if market_info["game_start_time"]:
                try:
                    start_time = datetime.fromisoformat(market_info["game_start_time"].replace('Z', '+00:00'))
                    market_info["game_start_formatted"] = start_time.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    market_info["game_start_formatted"] = market_info["game_start_time"]
            else:
                market_info["game_start_formatted"] = "无开始时间"
            
            return market_info
            
        except Exception as e:
            self.logger.error(f"提取市场信息失败: {e}")
            return {
                "title": "数据解析错误",
                "market_id": "错误",
                "current_price": 0,
                "volume": 0,
                "liquidity": 0,
                "end_date_formatted": "错误"
            }
    
    def _extract_category(self, market: Dict) -> str:
        """从市场数据中提取分类信息"""
        # 尝试从不同字段提取分类
        if "category" in market:
            return market["category"]
        
        # 从标题中推断分类
        question = market.get("question", "")
        description = market.get("description", "")
        
        # 处理None值
        if question is None:
            question = ""
        if description is None:
            description = ""
            
        question = question.lower()
        description = description.lower()
        text = f"{question} {description}"
        
        if any(keyword in text for keyword in ["election", "president", "politics", "vote", "congress"]):
            return "politics"
        elif any(keyword in text for keyword in ["bitcoin", "ethereum", "crypto", "btc", "eth"]):
            return "crypto"
        elif any(keyword in text for keyword in ["nba", "nfl", "mlb", "soccer", "sports", "game", "team"]):
            return "sports"
        elif any(keyword in text for keyword in ["stock", "market", "economy", "fed", "inflation"]):
            return "finance"
        else:
            return "other"
    
    def display_markets_table(self, markets_info: List[Dict], show_all: bool = False):
        """
        以表格形式显示市场信息
        
        Args:
            markets_info: 市场信息列表
            show_all: 是否显示所有字段
        """
        if not markets_info:
            print("没有可显示的市场数据")
            return
        
        # 准备表格数据
        table_data = []
        for i, market in enumerate(markets_info, 1):
            # 截断标题以适应表格
            title = market["title"]
            if len(title) > 60:
                title = title[:57] + "..."
            
            # 状态显示
            status = "活跃" if market.get("active", False) else "已关闭"
            if market.get("closed", False):
                status = "已结算"
            
            row = [
                i,
                title,
                f"${market['current_price']:.4f}",
                market["price_range"],
                market["category"],
                market["end_date_formatted"],
                status,
                market["total_tokens"]
            ]
            table_data.append(row)
        
        # 表格标题
        headers = ["序号", "标题", "当前价格", "价格区间", "分类", "到期时间", "状态", "选项数"]
        
        # 显示表格
        print(f"\n{'='*140}")
        print(f"Polymarket 预测市场列表 (共 {len(markets_info)} 个市场)")
        print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*140}")
        
        print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="left"))
        
        # 显示统计信息
        active_markets = sum(1 for market in markets_info if market.get("active", False))
        closed_markets = sum(1 for market in markets_info if market.get("closed", False))
        accepting_orders = sum(1 for market in markets_info if market.get("accepting_orders", False))
        
        # 分类统计
        categories = {}
        for market in markets_info:
            category = market["category"]
            categories[category] = categories.get(category, 0) + 1
        
        print(f"\n统计信息:")
        print(f"  - 活跃市场: {active_markets}/{len(markets_info)}")
        print(f"  - 已结算市场: {closed_markets}/{len(markets_info)}")
        print(f"  - 接受订单: {accepting_orders}/{len(markets_info)}")
        
        print(f"\n分类分布:")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {category}: {count} 个市场")
        
        # 显示前几个市场的详细信息（可选）
        if show_all and len(markets_info) > 0:
            print(f"\n前3个市场详细信息:")
            for i, market in enumerate(markets_info[:3], 1):
                print(f"\n市场 {i}: {market['title']}")
                print(f"  描述: {market['description'][:100]}{'...' if len(market['description']) > 100 else ''}")
                print(f"  市场ID: {market['market_id']}")
                print(f"  条件ID: {market['condition_id']}")
                print(f"  游戏开始时间: {market['game_start_formatted']}")
                print(f"  最小订单大小: ${market['minimum_order_size']}")
                print(f"  最小价格变动: ${market['minimum_tick_size']}")
                print(f"  风险类型: {'负风险' if market['neg_risk'] else '标准'}")
                print(f"  标签: {', '.join(market['tags'])}")
    
    def export_to_json(self, markets_info: List[Dict], filename: str = "polymarket_markets.json"):
        """导出市场数据到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(markets_info, f, ensure_ascii=False, indent=2)
            self.logger.info(f"市场数据已导出到: {filename}")
        except Exception as e:
            self.logger.error(f"导出数据失败: {e}")
    
    def run(self, limit: int = None, export_json: bool = False):
        """运行市场数据获取流程"""
        self.logger.info("开始获取Polymarket市场数据...")
        
        # 获取市场数据
        markets = self.get_markets(limit)
        if not markets:
            self.logger.error("未能获取到市场数据")
            return
        
        # 提取关键信息
        markets_info = []
        for market in markets:
            market_info = self.extract_market_info(market)
            markets_info.append(market_info)
        
        # 显示结果
        self.display_markets_table(markets_info)
        
        # 导出数据
        if export_json:
            self.export_to_json(markets_info)


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="获取Polymarket预测市场数据")
    parser.add_argument("--limit", "-l", type=int, help="限制显示的市场数量")
    parser.add_argument("--export-json", action="store_true", help="导出数据到JSON文件")
    parser.add_argument("--api-url", help="CLOB API URL")
    
    args = parser.parse_args()
    
    # 创建并运行市场获取器
    fetcher = PolymarketMarketFetcher(api_url=args.api_url)
    fetcher.run(limit=args.limit, export_json=args.export_json)


if __name__ == "__main__":
    main()
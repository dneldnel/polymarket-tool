# Polymarket 市场数据获取工具

一个用于获取Polymarket预测市场数据的Python工具，可以列出所有可下注的预测市场标题和基本信息。

## 功能特性

- 📊 **获取市场列表** - 获取Polymarket上所有可下注的预测市场
- 🔍 **市场信息** - 显示市场标题、价格、成交量、流动性等基本信息
- 🎯 **筛选功能** - 按分类、活跃状态筛选市场
- 📈 **数据导出** - 支持导出市场数据到JSON文件
- ⚙️ **配置管理** - 支持环境变量和命令行参数配置
- 🐛 **错误处理** - 完善的错误处理和日志记录

## 安装

### 1. 克隆或下载项目

```bash
git clone <repository-url>
cd polymarket-tool
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量（可选）

复制环境变量模板文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Polymarket CLOB API Configuration
CLOB_API_URL=https://clob.polymarket.com

# Application Settings
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
MAX_RETRIES=3
DEFAULT_LIMIT=50
```

## 使用方法

### 基本使用

显示前50个市场（默认）：

```bash
python main.py
```

### 命令行选项

```bash
# 显示帮助信息
python main.py --help

# 限制显示的市场数量
python main.py --limit 20
python main.py -l 10

# 显示所有市场
python main.py --all

# 按分类筛选
python main.py --category politics
python main.py --category sports
python main.py --category crypto

# 只显示活跃市场
python main.py --active-only

# 导出数据到JSON文件
python main.py --export-json

# 详细输出模式
python main.py --verbose

# 显示当前配置
python main.py --show-config

# 自定义API URL
python main.py --api-url https://clob.polymarket.com
```

### 组合使用示例

```bash
# 显示前20个活跃的政治类市场并导出数据
python main.py -l 20 --category politics --active-only --export-json

# 显示所有加密货币市场
python main.py --all --category crypto
```

## 输出示例

```
================================================================================
Polymarket 市场数据获取工具
================================================================================
开始时间: 2024-01-01 12:00:00

+--------+--------------------------------------------------------------------------------+--------------+---------------+--------------+----------+---------------------+--------+
| 序号   | 标题                                                                          | 当前价格     | 24h成交量     | 流动性       | 分类     | 到期时间            | 活跃   |
+--------+--------------------------------------------------------------------------------+--------------+---------------+--------------+----------+---------------------+--------+
| 1      | 谁将赢得2024年美国总统大选？                                                   | $0.5200      | $1,234,567.89 | $5,678,901.23| politics | 2024-11-05 23:59:59 | 是     |
| 2      | 比特币价格在2024年底会超过10万美元吗？                                         | $0.3500      | $987,654.32   | $4,321,098.76| crypto   | 2024-12-31 23:59:59 | 是     |
| 3      | 湖人队会赢得2024年NBA总冠军吗？                                                | $0.1500      | $123,456.78   | $987,654.32  | sports   | 2024-06-30 23:59:59 | 是     |
+--------+--------------------------------------------------------------------------------+--------------+---------------+--------------+----------+---------------------+--------+

统计信息:
  - 活跃市场: 3/3
  - 总成交量: $2,345,678.99
  - 总流动性: $10,987,654.31

完成时间: 2024-01-01 12:00:05
```

## 数据结构

每个市场包含以下信息：

- **标题 (title)**: 预测市场的问题描述
- **市场ID (market_id)**: 市场的唯一标识符
- **条件ID (condition_id)**: 条件标识符
- **当前价格 (current_price)**: 当前市场价格（美元）
- **24h成交量 (volume)**: 24小时内的交易量
- **流动性 (liquidity)**: 市场流动性总额
- **分类 (category)**: 市场分类（政治、体育、加密货币等）
- **到期时间 (end_date_formatted)**: 市场结算时间
- **活跃状态 (active)**: 市场是否活跃

## 配置说明

### 环境变量

在 `.env` 文件中设置：

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `CLOB_API_URL` | CLOB API URL | `https://clob.polymarket.com` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `REQUEST_TIMEOUT` | 请求超时时间（秒） | `30` |
| `MAX_RETRIES` | 最大重试次数 | `3` |
| `DEFAULT_LIMIT` | 默认显示市场数量 | `50` |

### 命令行参数

所有配置都可以通过命令行参数覆盖，使用 `--help` 查看完整选项列表。

## 错误处理

- **网络错误**: 自动重试机制
- **API错误**: 详细的错误信息和日志记录
- **配置错误**: 配置验证和友好的错误提示

## 开发

### 项目结构

```
polymarket-tool/
├── main.py                 # 主入口脚本
├── polymarket_markets.py   # 市场数据获取核心逻辑
├── config.py              # 配置管理模块
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量模板
└── README.md             # 项目文档
```

### 扩展功能

可以轻松扩展以下功能：

- 添加更多数据字段
- 实现实时数据更新
- 添加图表显示
- 集成其他数据源
- 添加Web界面

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个工具。

## 免责声明

本工具仅用于教育和研究目的。使用Polymarket进行交易存在风险，请谨慎投资。
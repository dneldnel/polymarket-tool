# Polymarket 市场数据获取工具

一个现代化的Polymarket预测市场数据工具，同时提供命令行界面(CLI)和Web应用界面，用于获取和分析Polymarket上的预测市场数据。

## 🌟 功能特性

### CLI工具功能
- 📊 **获取市场列表** - 获取Polymarket上所有可下注的预测市场
- 🔍 **市场信息** - 显示市场标题、价格、成交量、流动性等基本信息
- 🎯 **筛选功能** - 按分类、活跃状态筛选市场
- 📈 **数据导出** - 支持导出市场数据到JSON文件
- ⚙️ **配置管理** - 支持环境变量和命令行参数配置
- 🐛 **错误处理** - 完善的错误处理和日志记录

### Web应用功能
- 🌐 **现代化Web界面** - 响应式设计，支持桌面和移动设备
- 📱 **用户友好界面** - 直观的表格展示和数据可视化
- 🔍 **实时搜索和筛选** - 动态搜索、分类筛选、活跃状态筛选
- 📄 **分页浏览** - 高效的数据分页和导航
- 💾 **多种导出格式** - JSON和CSV格式数据导出
- ⚙️ **可视化配置管理** - 通过Web界面管理应用设置
- 📊 **实时统计** - 市场数量、活跃状态等统计信息
- 🚀 **RESTful API** - 完整的API接口供第三方使用

## 安装

### 1. 克隆或下载项目

```bash
git clone <repository-url>
cd polymarket-tool
```

### 2. 创建虚拟环境并安装依赖

推荐使用 Python 虚拟环境来管理项目依赖：

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或者在 Windows 上使用：venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

**注意：** 每次运行程序前都需要先激活虚拟环境。

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

**首先激活虚拟环境：**

```bash
source venv/bin/activate  # Linux/macOS
# 或者在 Windows 上使用：venv\Scripts\activate
```

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

### 快速开始

如果您已经设置好虚拟环境，可以按以下步骤快速开始：

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 运行程序查看帮助
python main.py --help

# 3. 显示前10个市场
python main.py --limit 10
```

### 组合使用示例

```bash
# 显示前20个活跃的政治类市场并导出数据
python main.py -l 20 --category politics --active-only --export-json

# 显示所有加密货币市场
python main.py --all --category crypto
```

## 🌐 Web应用启动和使用

### 快速启动

```bash
# 1. 确保虚拟环境已激活
source venv/bin/activate

# 2. 安装依赖（如果还未安装）
pip install -r requirements.txt

# 3. 启动Web应用
python app.py
```

应用启动成功后，将显示类似以下信息：
```
启动Polymarket Web应用...
访问地址: http://localhost:5000
调试模式: True
 * Running on http://0.0.0.0:5000
```

### 访问应用

在浏览器中打开以下地址：
- **主页（市场列表）**: http://localhost:5000
- **设置页面**: http://localhost:5000/settings
- **关于页面**: http://localhost:5000/about

### 环境变量配置

如果需要自定义配置，可以创建 `.env` 文件：

```bash
# 复制模板文件
cp .env.example .env

# 编辑配置
nano .env
```

可选的环境变量：
```env
# Flask应用配置
FLASK_ENV=development          # 运行环境: development/production
PORT=5000                       # 监听端口

# Polymarket API配置
CLOB_API_URL=https://clob.polymarket.com
REQUEST_TIMEOUT=30                # API请求超时（秒）
MAX_RETRIES=3                     # 最大重试次数
DEFAULT_LIMIT=50                  # 默认显示数量
LOG_LEVEL=INFO                     # 日志级别
```

### 生产环境部署

对于生产环境部署，建议：

```bash
# 1. 设置生产环境变量
export FLASK_ENV=production
export PORT=5000

# 2. 使用WSGI服务器启动
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

# 3. 或使用Docker部署
docker build -t polymarket-web .
docker run -p 5000:5000 polymarket-web
```

### 故障排除

**问题1: ModuleNotFoundError: No module named 'flask'**
```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

**问题2: 端口已被占用**
```bash
# 检查端口占用
lsof -i :5000

# 或修改端口
export PORT=5001
python app.py
```

**问题3: API连接失败**
```bash
# 检查网络连接
curl https://clob.polymarket.com

# 验证API URL
curl -I https://clob.polymarket.com/health
```

## 🌐 Web应用使用指南

### 📱 界面导览

#### 1. 市场列表页面（主页）
- **访问地址**: http://localhost:5000
- **主要功能**:
  - 📊 **实时数据展示**: 显示所有市场的基本信息（标题、价格、分类、状态等）
  - 🔍 **智能搜索**: 在搜索框中输入关键词，实时筛选市场
  - 🎯 **筛选功能**:
    - 分类筛选：政治、体育、加密货币、金融、其他
    - 活跃状态筛选：仅显示当前可交易市场
    - 显示数量：选择每页显示的市场数量（10/20/50/100个）
  - 📄 **分页浏览**: 使用底部控件浏览大量市场数据
  - 💾 **数据导出**:
    - JSON导出：包含所有筛选数据的完整JSON文件
    - CSV导出：Excel兼容的CSV格式文件

#### 2. 设置页面
- **访问地址**: http://localhost:5000/settings
- **配置选项**:
  - 请求超时时间：API请求的最大等待时间（1-300秒）
  - 最大重试次数：失败请求的重试次数（0-10次）
  - 默认显示数量：页面默认显示的市场数量（10-1000个）
  - 日志级别：DEBUG/INFO/WARNING/ERROR
- **系统监控**:
  - API连接状态：显示与Polymarket API的连接状态
  - 环境信息：当前运行环境和版本信息
  - 实时健康检查：点击"刷新状态"按钮检查系统状态

#### 3. 关于页面
- **访问地址**: http://localhost:5000/about
- **包含内容**:
  - 📖 功能介绍：详细的功能特性说明
  - 🚀 API文档：完整的RESTful API接口文档
  - ⚠️ 免责声明：使用风险提示和注意事项

### 🔧 高级功能

#### 实时数据刷新
- 点击右上角的"刷新"按钮获取最新数据
- 系统会自动更新统计信息和市场状态

#### 数据筛选技巧
1. **组合筛选**：可以同时使用搜索和分类筛选
2. **精确搜索**：支持搜索市场标题和描述中的关键词
3. **状态筛选**：勾选"仅显示活跃市场"查看当前可交易市场
4. **URL分享**：筛选状态会反映在URL中，可以分享链接

#### 数据导出
1. **应用筛选**：先使用筛选器找到感兴趣的数据
2. **选择格式**：点击"导出JSON"或"导出CSV"按钮
3. **自动下载**：文件会自动下载到默认下载目录
4. **时间戳**：导出文件名包含时间戳，避免覆盖

### 性能优化建议

#### 大数据量处理
- 使用筛选功能减少一次显示的数据量
- 选择合适的"显示数量"设置（推荐50-100个）
- 避免同时进行多个操作

#### 浏览器兼容性
- **推荐浏览器**: Chrome、Firefox、Safari、Edge 最新版本
- **移动设备**: iOS Safari、Chrome Mobile、Firefox Mobile
- **需要JavaScript**: 所有功能都需要启用JavaScript

#### 网络要求
- 稳定的网络连接用于访问Polymarket API
- 如果遇到加载缓慢，可以尝试：
  - 刷新页面
  - 检查网络连接
  - 减少同时打开的标签页

## 🚀 RESTful API接口

Web应用提供完整的RESTful API接口，供第三方开发者使用：

### 核心端点

```bash
# 获取市场列表
GET /api/v1/markets?limit=50&category=politics&active_only=true

# 获取单个市场详情
GET /api/v1/markets/{market_id}

# 获取市场分类
GET /api/v1/markets/categories

# 获取市场统计
GET /api/v1/markets/stats

# 获取配置
GET /api/v1/config

# 更新配置
PUT /api/v1/config

# 健康检查
GET /api/v1/health

# 系统状态
GET /api/v1/status
```

### API响应格式

```json
{
  "success": true,
  "data": {...},
  "message": "操作成功",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

详细的API文档请访问Web应用的"关于"页面。

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
├── venv/                   # Python虚拟环境目录
├── app.py                  # Flask Web应用主入口
├── main.py                 # CLI工具主入口脚本
├── polymarket_markets.py   # 市场数据获取核心逻辑
├── config.py              # 配置管理模块
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量模板
├── frontend/              # Web应用前端资源
│   ├── index.html         # 主页面（市场列表）
│   ├── settings.html      # 设置页面
│   ├── about.html         # 关于页面
│   ├── css/
│   │   └── main.css       # 样式文件
│   └── js/
│       ├── api.js         # API通信模块
│       ├── main.js        # 主页面功能
│       └── settings.js    # 设置页面功能
├── api/                   # 后端API模块
│   ├── __init__.py
│   └── routes.py          # API路由定义
├── examples/              # 使用示例
├── debug_*.py            # 调试脚本
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
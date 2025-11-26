/**
 * API通信模块
 * 提供与后端API的通信功能
 */

class PolymarketAPI {
    constructor(baseURL = '/api/v1') {
        this.baseURL = baseURL;
        this.defaultTimeout = 30000; // 30秒
    }

    /**
     * 发送HTTP请求的通用方法
     * @param {string} endpoint - API端点
     * @param {Object} options - 请求选项
     * @returns {Promise} Promise对象
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            timeout: this.defaultTimeout,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error?.message || `HTTP ${response.status}: ${response.statusText}`);
            }

            return data;
        } catch (error) {
            console.error(`API请求失败: ${endpoint}`, error);
            throw error;
        }
    }

    /**
     * GET请求
     */
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url);
    }

    /**
     * POST请求
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * PUT请求
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // ==================== 市场数据相关API ====================

    /**
     * 获取市场列表
     * @param {Object} params - 查询参数
     * @param {number} params.limit - 限制返回数量
     * @param {number} params.page - 页码
     * @param {string} params.category - 分类筛选
     * @param {boolean} params.active_only - 仅显示活跃市场
     * @returns {Promise} 市场数据
     */
    async getMarkets(params = {}) {
        return this.get('/markets', params);
    }

    /**
     * 获取单个市场详情
     * @param {string} marketId - 市场ID
     * @returns {Promise} 市场详情
     */
    async getMarketDetail(marketId) {
        return this.get(`/markets/${marketId}`);
    }

    /**
     * 获取市场分类列表
     * @returns {Promise} 分类数据
     */
    async getMarketCategories() {
        return this.get('/markets/categories');
    }

    /**
     * 获取市场统计信息
     * @returns {Promise} 统计数据
     */
    async getMarketStats() {
        return this.get('/markets/stats');
    }

    // ==================== 配置相关API ====================

    /**
     * 获取当前配置
     * @returns {Promise} 配置数据
     */
    async getConfig() {
        return this.get('/config');
    }

    /**
     * 更新配置
     * @param {Object} configData - 配置数据
     * @returns {Promise} 更新结果
     */
    async updateConfig(configData) {
        return this.put('/config', configData);
    }

    // ==================== 系统相关API ====================

    /**
     * 健康检查
     * @returns {Promise} 健康状态
     */
    async healthCheck() {
        return this.get('/health');
    }

    /**
     * 获取系统状态
     * @returns {Promise} 系统状态
     */
    async getSystemStatus() {
        return this.get('/status');
    }

    // ==================== 数据导出功能 ====================

    /**
     * 导出市场数据为JSON
     * @param {Object} params - 筛选参数
     * @returns {Promise} Blob对象
     */
    async exportToJSON(params = {}) {
        try {
            const response = await this.get('/markets', { ...params, limit: -1 });
            const markets = response.data.markets;

            const jsonString = JSON.stringify(markets, null, 2);
            const blob = new Blob([jsonString], { type: 'application/json' });
            return blob;
        } catch (error) {
            console.error('导出JSON失败:', error);
            throw error;
        }
    }

    /**
     * 导出市场数据为CSV
     * @param {Object} params - 筛选参数
     * @returns {Promise} Blob对象
     */
    async exportToCSV(params = {}) {
        try {
            const response = await this.get('/markets', { ...params, limit: -1 });
            const markets = response.data.markets;

            // CSV头部
            const headers = [
                '标题', '当前价格', '价格区间', '分类', '到期时间',
                '状态', '活跃', '已关闭', '选项数', '描述'
            ];

            // CSV数据
            const csvRows = [headers.join(',')];

            markets.forEach(market => {
                const row = [
                    `"${this.escapeCsv(market.title)}"`,
                    market.current_price,
                    `"${market.price_range}"`,
                    market.category,
                    `"${market.end_date_formatted}"`,
                    market.active ? '活跃' : '非活跃',
                    market.active ? '是' : '否',
                    market.closed ? '是' : '否',
                    market.total_tokens,
                    `"${this.escapeCsv(market.description)}"`
                ];
                csvRows.push(row.join(','));
            });

            const csvString = csvRows.join('\n');
            const blob = new Blob(['\uFEFF' + csvString], { type: 'text/csv;charset=utf-8;' });
            return blob;
        } catch (error) {
            console.error('导出CSV失败:', error);
            throw error;
        }
    }

    /**
     * 转义CSV字段中的特殊字符
     * @param {string} field - 字段值
     * @returns {string} 转义后的值
     */
    escapeCsv(field) {
        if (typeof field !== 'string') return '';
        return field.replace(/"/g, '""').replace(/\n/g, '\\n').replace(/\r/g, '\\r');
    }

    /**
     * 下载文件
     * @param {Blob} blob - 文件数据
     * @param {string} filename - 文件名
     */
    downloadFile(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    // ==================== 辅助方法 ====================

    /**
     * 格式化时间戳
     * @param {string} timestamp - ISO时间戳
     * @returns {string} 格式化后的时间
     */
    formatTimestamp(timestamp) {
        try {
            const date = new Date(timestamp);
            return date.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        } catch (error) {
            return timestamp;
        }
    }

    /**
     * 格式化价格
     * @param {number} price - 价格
     * @returns {string} 格式化后的价格
     */
    formatPrice(price) {
        if (typeof price !== 'number' || isNaN(price)) return '$0.0000';
        return `$${price.toFixed(4)}`;
    }

    /**
     * 获取状态的显示文本
     * @param {Object} market - 市场对象
     * @returns {string} 状态文本
     */
    getStatusText(market) {
        if (market.closed) return '已结算';
        if (market.active) return '活跃';
        return '非活跃';
    }

    /**
     * 获取状态的CSS类
     * @param {Object} market - 市场对象
     * @returns {string} CSS类名
     */
    getStatusClass(market) {
        if (market.closed) return 'status-closed';
        if (market.active) return 'status-active';
        return 'status-inactive';
    }

    /**
     * 获取分类的显示名称
     * @param {string} category - 分类标识
     * @returns {string} 显示名称
     */
    getCategoryDisplayName(category) {
        const categoryMap = {
            'politics': '政治',
            'sports': '体育',
            'crypto': '加密货币',
            'finance': '金融',
            'other': '其他'
        };
        return categoryMap[category] || category;
    }

    /**
     * 获取分类的CSS类
     * @param {string} category - 分类标识
     * @returns {string} CSS类名
     */
    getCategoryClass(category) {
        return `category-${category}`;
    }
}

// 创建全局API实例
window.polymarketAPI = new PolymarketAPI();
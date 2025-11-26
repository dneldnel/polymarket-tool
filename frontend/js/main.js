/**
 * 主页面JavaScript功能
 * 处理市场列表显示、筛选、分页等功能
 */

// 全局变量
let currentPage = 1;
let currentFilters = {};
let allMarkets = [];
let totalPages = 1;

// DOM元素
const elements = {
    loadingIndicator: document.getElementById('loading-indicator'),
    errorAlert: document.getElementById('error-alert'),
    errorMessage: document.getElementById('error-message'),
    marketsTable: document.getElementById('markets-table'),
    marketsTbody: document.getElementById('markets-tbody'),
    searchInput: document.getElementById('search-input'),
    categoryFilter: document.getElementById('category-filter'),
    limitSelect: document.getElementById('limit-select'),
    activeFilter: document.getElementById('active-filter'),
    applyFiltersBtn: document.getElementById('apply-filters'),
    clearFiltersBtn: document.getElementById('clear-filters'),
    refreshBtn: document.getElementById('refresh-data'),
    exportJsonBtn: document.getElementById('export-json'),
    exportCsvBtn: document.getElementById('export-csv'),
    paginationControls: document.getElementById('pagination-controls'),
    paginationInfo: document.getElementById('pagination-info'),
    showingStart: document.getElementById('showing-start'),
    showingEnd: document.getElementById('showing-end'),
    totalItems: document.getElementById('total-items'),
    marketCount: document.getElementById('market-count'),

    // 统计卡片
    totalMarkets: document.getElementById('total-markets'),
    activeMarkets: document.getElementById('active-markets'),
    closedMarkets: document.getElementById('closed-markets'),
    lastUpdate: document.getElementById('last-update')
};

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadCategories();
    loadMarketStats();
    loadMarkets();
});

/**
 * 初始化事件监听器
 */
function initializeEventListeners() {
    // 筛选器事件
    elements.applyFiltersBtn.addEventListener('click', applyFilters);
    elements.clearFiltersBtn.addEventListener('click', clearFilters);
    elements.refreshBtn.addEventListener('click', refreshData);

    // 搜索事件（防抖）
    let searchTimeout;
    elements.searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            if (elements.searchInput.value.trim()) {
                applyFilters();
            }
        }, 500);
    });

    // 导出事件
    elements.exportJsonBtn.addEventListener('click', exportJSON);
    elements.exportCsvBtn.addEventListener('click', exportCSV);

    // 分页事件
    elements.paginationControls.addEventListener('click', function(e) {
        if (e.target.classList.contains('page-link')) {
            const page = e.target.dataset.page;
            if (page && !isNaN(page)) {
                currentPage = parseInt(page);
                loadMarkets();
            }
        }
    });

    // 回车键搜索
    elements.searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            applyFilters();
        }
    });
}

/**
 * 显示加载指示器
 */
function showLoading() {
    elements.loadingIndicator.style.display = 'block';
    elements.errorAlert.style.display = 'none';
    elements.marketsTable.style.display = 'none';
}

/**
 * 隐藏加载指示器
 */
function hideLoading() {
    elements.loadingIndicator.style.display = 'none';
    elements.marketsTable.style.display = 'table';
}

/**
 * 显示错误信息
 * @param {string} message - 错误消息
 */
function showError(message) {
    hideLoading();
    elements.errorMessage.textContent = message;
    elements.errorAlert.style.display = 'block';
    elements.marketsTable.style.display = 'none';
}

/**
 * 隐藏错误信息
 */
function hideError() {
    elements.errorAlert.style.display = 'none';
}

/**
 * 加载市场分类
 */
async function loadCategories() {
    try {
        const response = await window.polymarketAPI.getMarketCategories();
        const categories = response.data.categories;

        // 清空现有选项（保留"所有分类"）
        elements.categoryFilter.innerHTML = '<option value="">所有分类</option>';

        // 添加分类选项
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.name;
            option.textContent = `${category.display_name} (${category.count})`;
            elements.categoryFilter.appendChild(option);
        });
    } catch (error) {
        console.error('加载分类失败:', error);
    }
}

/**
 * 加载市场统计信息
 */
async function loadMarketStats() {
    try {
        const response = await window.polymarketAPI.getMarketStats();
        const stats = response.data;

        // 更新统计卡片
        elements.totalMarkets.textContent = stats.total_markets || 0;
        elements.activeMarkets.textContent = stats.active_markets || 0;
        elements.closedMarkets.textContent = stats.closed_markets || 0;

        // 更新最后更新时间
        if (stats.last_updated) {
            elements.lastUpdate.textContent = window.polymarketAPI.formatTimestamp(stats.last_updated);
        } else {
            elements.lastUpdate.textContent = '未知';
        }
    } catch (error) {
        console.error('加载统计信息失败:', error);
    }
}

/**
 * 加载市场数据
 */
async function loadMarkets() {
    showLoading();
    hideError();

    try {
        // 构建查询参数
        const params = {
            page: currentPage,
            limit: parseInt(elements.limitSelect.value),
            ...currentFilters
        };

        const response = await window.polymarketAPI.getMarkets(params);
        const data = response.data;

        // 保存数据
        allMarkets = data.markets;
        totalPages = data.pagination.total_pages;

        // 渲染市场表格
        renderMarketsTable(data.markets);

        // 更新分页信息
        updatePagination(data.pagination);

        // 更新市场计数
        const filterText = Object.keys(currentFilters).length > 0 ? ' (筛选结果)' : '';
        elements.marketCount.textContent = `${data.markets.length} 个市场${filterText}`;

    } catch (error) {
        showError(`获取市场数据失败: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * 渲染市场表格
 * @param {Array} markets - 市场数据数组
 */
function renderMarketsTable(markets) {
    elements.marketsTbody.innerHTML = '';

    if (markets.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="7" class="text-center text-muted py-4">
                <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                暂无数据
            </td>
        `;
        elements.marketsTbody.appendChild(row);
        return;
    }

    markets.forEach(market => {
        const row = document.createElement('tr');

        // 格式化价格
        const price = window.polymarketAPI.formatPrice(market.current_price);

        // 格式化到期时间
        const endTime = market.end_date_formatted || '无到期时间';

        row.innerHTML = `
            <td>
                <div class="market-title" title="${market.title}">
                    ${market.title}
                </div>
            </td>
            <td>
                <span class="price">${price}</span>
            </td>
            <td>
                <span class="time-display">${market.price_range}</span>
            </td>
            <td>
                <span class="category-badge ${window.polymarketAPI.getCategoryClass(market.category)}">
                    ${window.polymarketAPI.getCategoryDisplayName(market.category)}
                </span>
            </td>
            <td>
                <span class="time-display">${endTime}</span>
            </td>
            <td>
                <span class="${window.polymarketAPI.getStatusClass(market)}">
                    ${window.polymarketAPI.getStatusText(market)}
                </span>
            </td>
            <td>
                <span class="badge bg-secondary">${market.total_tokens || 0}</span>
            </td>
        `;

        elements.marketsTbody.appendChild(row);
    });
}

/**
 * 更新分页控件
 * @param {Object} pagination - 分页信息
 */
function updatePagination(pagination) {
    const { page, limit, total, total_pages, has_more } = pagination;

    // 更新分页信息
    const start = (page - 1) * limit + 1;
    const end = Math.min(page * limit, total);
    elements.showingStart.textContent = start;
    elements.showingEnd.textContent = end;
    elements.totalItems.textContent = total;

    // 生成分页按钮
    elements.paginationControls.innerHTML = '';

    // 上一页按钮
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${page <= 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `
        <a class="page-link" href="#" data-page="${page - 1}" tabindex="-1">
            <i class="bi bi-chevron-left"></i>
        </a>
    `;
    elements.paginationControls.appendChild(prevLi);

    // 页码按钮
    const startPage = Math.max(1, page - 2);
    const endPage = Math.min(total_pages, page + 2);

    if (startPage > 1) {
        addPageButton(1);
        if (startPage > 2) {
            const ellipsis = document.createElement('li');
            ellipsis.className = 'page-item disabled';
            ellipsis.innerHTML = '<a class="page-link" href="#">...</a>';
            elements.paginationControls.appendChild(ellipsis);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        addPageButton(i);
    }

    if (endPage < total_pages) {
        if (endPage < total_pages - 1) {
            const ellipsis = document.createElement('li');
            ellipsis.className = 'page-item disabled';
            ellipsis.innerHTML = '<a class="page-link" href="#">...</a>';
            elements.paginationControls.appendChild(ellipsis);
        }
        addPageButton(total_pages);
    }

    // 下一页按钮
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${page >= total_pages ? 'disabled' : ''}`;
    nextLi.innerHTML = `
        <a class="page-link" href="#" data-page="${page + 1}">
            <i class="bi bi-chevron-right"></i>
        </a>
    `;
    elements.paginationControls.appendChild(nextLi);
}

/**
 * 添加页码按钮
 * @param {number} pageNum - 页码
 */
function addPageButton(pageNum) {
    const li = document.createElement('li');
    li.className = `page-item ${pageNum === currentPage ? 'active' : ''}`;
    li.innerHTML = `
        <a class="page-link" href="#" data-page="${pageNum}">${pageNum}</a>
    `;
    elements.paginationControls.appendChild(li);
}

/**
 * 应用筛选条件
 */
function applyFilters() {
    // 收集筛选条件
    currentFilters = {};

    const searchTerm = elements.searchInput.value.trim();
    if (searchTerm) {
        currentFilters.search = searchTerm;
    }

    const category = elements.categoryFilter.value;
    if (category) {
        currentFilters.category = category;
    }

    const activeOnly = elements.activeFilter.checked;
    if (activeOnly) {
        currentFilters.active_only = true;
    }

    // 重置到第一页
    currentPage = 1;

    // 重新加载数据
    loadMarkets();
}

/**
 * 清除筛选条件
 */
function clearFilters() {
    // 重置筛选器
    elements.searchInput.value = '';
    elements.categoryFilter.value = '';
    elements.activeFilter.checked = false;
    elements.limitSelect.value = '50';

    // 清除筛选条件
    currentFilters = {};
    currentPage = 1;

    // 重新加载数据
    loadMarkets();
}

/**
 * 刷新数据
 */
function refreshData() {
    loadMarketStats();
    loadMarkets();
}

/**
 * 导出JSON
 */
async function exportJSON() {
    try {
        const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
        const filename = `polymarket_markets_${timestamp}.json`;

        showLoading();
        const blob = await window.polymarketAPI.exportToJSON(currentFilters);
        window.polymarketAPI.downloadFile(blob, filename);

        // 显示成功消息
        showSuccessMessage(`JSON数据已导出到 ${filename}`);
    } catch (error) {
        showError(`导出JSON失败: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * 导出CSV
 */
async function exportCSV() {
    try {
        const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
        const filename = `polymarket_markets_${timestamp}.csv`;

        showLoading();
        const blob = await window.polymarketAPI.exportToCSV(currentFilters);
        window.polymarketAPI.downloadFile(blob, filename);

        // 显示成功消息
        showSuccessMessage(`CSV数据已导出到 ${filename}`);
    } catch (error) {
        showError(`导出CSV失败: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * 显示成功消息
 * @param {string} message - 成功消息
 */
function showSuccessMessage(message) {
    // 创建成功提示元素
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    alertDiv.innerHTML = `
        <i class="bi bi-check-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertDiv);

    // 3秒后自动移除
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

// 添加成功提示样式
const successStyle = document.createElement('style');
successStyle.textContent = `
    .alert-success {
        background-color: #d1e7dd;
        border-color: #badbcc;
        color: #0f5132;
    }
`;
document.head.appendChild(successStyle);
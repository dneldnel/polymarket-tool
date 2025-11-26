/**
 * 设置页面JavaScript功能
 * 处理配置管理、系统状态等功能
 */

// DOM元素
const elements = {
    loadingIndicator: document.getElementById('loading-indicator'),
    successAlert: document.getElementById('success-alert'),
    errorAlert: document.getElementById('error-alert'),
    successMessage: document.getElementById('success-message'),
    errorMessage: document.getElementById('error-message'),
    settingsForm: document.getElementById('settings-form'),
    saveSettingsBtn: document.getElementById('save-settings'),
    resetSettingsBtn: document.getElementById('reset-settings'),
    validateConfigBtn: document.getElementById('validate-config'),
    checkSystemStatusBtn: document.getElementById('check-system-status'),

    // 配置字段
    clobApiUrl: document.getElementById('clob-api-url'),
    requestTimeout: document.getElementById('request-timeout'),
    maxRetries: document.getElementById('max-retries'),
    defaultLimit: document.getElementById('default-limit'),
    logLevel: document.getElementById('log-level'),

    // 系统状态字段
    apiStatus: document.getElementById('api-status'),
    lastCheck: document.getElementById('last-check'),
    environment: document.getElementById('environment'),
    version: document.getElementById('version')
};

// 默认配置
const defaultConfig = {
    request_timeout: 30,
    max_retries: 3,
    default_limit: 50,
    log_level: 'INFO'
};

// 当前配置
let currentConfig = {};

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadCurrentConfig();
    checkSystemStatus();
});

/**
 * 初始化事件监听器
 */
function initializeEventListeners() {
    // 表单提交
    elements.settingsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        saveSettings();
    });

    // 按钮事件
    elements.saveSettingsBtn.addEventListener('click', saveSettings);
    elements.resetSettingsBtn.addEventListener('click', resetSettings);
    elements.validateConfigBtn.addEventListener('click', validateConfig);
    elements.checkSystemStatusBtn.addEventListener('click', checkSystemStatus);

    // 配置字段验证
    elements.requestTimeout.addEventListener('input', validateTimeout);
    elements.maxRetries.addEventListener('input', validateRetries);
}

/**
 * 显示加载指示器
 */
function showLoading() {
    elements.loadingIndicator.style.display = 'block';
    hideMessages();
}

/**
 * 隐藏加载指示器
 */
function hideLoading() {
    elements.loadingIndicator.style.display = 'none';
}

/**
 * 显示成功消息
 * @param {string} message - 成功消息
 */
function showSuccess(message) {
    hideLoading();
    elements.successMessage.textContent = message;
    elements.successAlert.style.display = 'block';
    elements.errorAlert.style.display = 'none';

    // 3秒后自动隐藏
    setTimeout(() => {
        elements.successAlert.style.display = 'none';
    }, 3000);
}

/**
 * 显示错误消息
 * @param {string} message - 错误消息
 */
function showError(message) {
    hideLoading();
    elements.errorMessage.textContent = message;
    elements.errorAlert.style.display = 'block';
    elements.successAlert.style.display = 'none';
}

/**
 * 隐藏所有消息
 */
function hideMessages() {
    elements.successAlert.style.display = 'none';
    elements.errorAlert.style.display = 'none';
}

/**
 * 加载当前配置
 */
async function loadCurrentConfig() {
    showLoading();

    try {
        const response = await window.polymarketAPI.getConfig();
        currentConfig = response.data;

        // 填充表单字段
        elements.clobApiUrl.value = currentConfig.clob_api_url || '';
        elements.requestTimeout.value = currentConfig.request_timeout || defaultConfig.request_timeout;
        elements.maxRetries.value = currentConfig.max_retries || defaultConfig.max_retries;
        elements.defaultLimit.value = currentConfig.default_limit || defaultConfig.default_limit;
        elements.logLevel.value = currentConfig.log_level || defaultConfig.log_level;

    } catch (error) {
        showError(`加载配置失败: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * 保存设置
 */
async function saveSettings() {
    if (!validateForm()) {
        return;
    }

    showLoading();

    try {
        // 收集表单数据
        const configData = {
            request_timeout: parseInt(elements.requestTimeout.value),
            max_retries: parseInt(elements.maxRetries.value),
            default_limit: parseInt(elements.defaultLimit.value),
            log_level: elements.logLevel.value
        };

        // 发送更新请求
        const response = await window.polymarketAPI.updateConfig(configData);

        // 更新当前配置
        currentConfig = { ...currentConfig, ...configData };

        showSuccess('配置保存成功！');

    } catch (error) {
        showError(`保存配置失败: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * 重置设置为默认值
 */
function resetSettings() {
    if (!confirm('确定要重置为默认设置吗？')) {
        return;
    }

    // 重置表单字段
    elements.requestTimeout.value = defaultConfig.request_timeout;
    elements.maxRetries.value = defaultConfig.max_retries;
    elements.defaultLimit.value = defaultConfig.default_limit;
    elements.logLevel.value = defaultConfig.log_level;

    showSuccess('已重置为默认设置');
}

/**
 * 验证配置
 */
async function validateConfig() {
    showLoading();

    try {
        // 收集表单数据
        const configData = {
            request_timeout: parseInt(elements.requestTimeout.value),
            max_retries: parseInt(elements.maxRetries.value),
            default_limit: parseInt(elements.defaultLimit.value),
            log_level: elements.logLevel.value
        };

        // 基本验证
        if (!validateForm()) {
            return;
        }

        // 测试API连接
        const healthResponse = await window.polymarketAPI.healthCheck();

        if (healthResponse.success && healthResponse.data.clob_api_connected) {
            showSuccess('配置验证成功！API连接正常。');
        } else {
            showError('配置验证失败：API连接异常。');
        }

    } catch (error) {
        showError(`配置验证失败: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * 检查系统状态
 */
async function checkSystemStatus() {
    elements.apiStatus.textContent = '检查中...';
    elements.apiStatus.className = 'badge bg-secondary';

    try {
        const healthResponse = await window.polymarketAPI.healthCheck();
        const statusResponse = await window.polymarketAPI.getSystemStatus();

        // 更新API状态
        if (healthResponse.success && healthResponse.data.clob_api_connected) {
            elements.apiStatus.textContent = '在线';
            elements.apiStatus.className = 'badge bg-success';
        } else {
            elements.apiStatus.textContent = '离线';
            elements.apiStatus.className = 'badge bg-danger';
        }

        // 更新系统信息
        const statusData = statusResponse.data;
        elements.lastCheck.textContent = window.polymarketAPI.formatTimestamp(healthResponse.data.timestamp);
        elements.environment.textContent = statusData.environment || '未知';
        elements.version.textContent = statusData.version || '未知';

    } catch (error) {
        elements.apiStatus.textContent = '错误';
        elements.apiStatus.className = 'badge bg-danger';
        elements.lastCheck.textContent = '检查失败';
        showError(`检查系统状态失败: ${error.message}`);
    }
}

/**
 * 验证表单
 * @returns {boolean} 验证结果
 */
function validateForm() {
    let isValid = true;

    // 验证请求超时时间
    if (!validateTimeout()) {
        isValid = false;
    }

    // 验证最大重试次数
    if (!validateRetries()) {
        isValid = false;
    }

    // 验证默认限制
    if (!validateLimit()) {
        isValid = false;
    }

    return isValid;
}

/**
 * 验证请求超时时间
 * @returns {boolean} 验证结果
 */
function validateTimeout() {
    const timeout = parseInt(elements.requestTimeout.value);

    if (isNaN(timeout) || timeout < 1 || timeout > 300) {
        elements.requestTimeout.classList.add('is-invalid');
        showFieldError(elements.requestTimeout, '请求超时时间必须是1-300之间的数字');
        return false;
    }

    elements.requestTimeout.classList.remove('is-invalid');
    return true;
}

/**
 * 验证最大重试次数
 * @returns {boolean} 验证结果
 */
function validateRetries() {
    const retries = parseInt(elements.maxRetries.value);

    if (isNaN(retries) || retries < 0 || retries > 10) {
        elements.maxRetries.classList.add('is-invalid');
        showFieldError(elements.maxRetries, '最大重试次数必须是0-10之间的数字');
        return false;
    }

    elements.maxRetries.classList.remove('is-invalid');
    return true;
}

/**
 * 验证默认限制
 * @returns {boolean} 验证结果
 */
function validateLimit() {
    const limit = parseInt(elements.defaultLimit.value);

    if (isNaN(limit) || limit < 10 || limit > 1000) {
        elements.defaultLimit.classList.add('is-invalid');
        showFieldError(elements.defaultLimit, '默认显示数量必须是10-1000之间的数字');
        return false;
    }

    elements.defaultLimit.classList.remove('is-invalid');
    return true;
}

/**
 * 显示字段错误
 * @param {HTMLElement} element - 表单元素
 * @param {string} message - 错误消息
 */
function showFieldError(element, message) {
    // 移除现有错误
    const existingError = element.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }

    // 添加新的错误消息
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    element.parentNode.appendChild(errorDiv);
}

// 添加样式
const customStyles = document.createElement('style');
customStyles.textContent = `
    .invalid-feedback {
        display: block;
        width: 100%;
        margin-top: 0.25rem;
        font-size: 0.875em;
        color: #dc3545;
    }

    .form-control.is-invalid {
        border-color: #dc3545;
        padding-right: calc(1.5em + 0.75rem);
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right calc(0.375em + 0.1875rem) center;
        background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
    }

    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }

    .badge {
        font-size: 0.75em;
    }
`;
document.head.appendChild(customStyles);
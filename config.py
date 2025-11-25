"""
配置文件管理模块
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv


class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置"""
        load_dotenv()
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        return {
            "clob_api_url": os.getenv("CLOB_API_URL", "https://clob.polymarket.com"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "request_timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
            "max_retries": int(os.getenv("MAX_RETRIES", "3")),
            
            # 可选的身份验证配置
            "private_key": os.getenv("PRIVATE_KEY"),
            "clob_api_key": os.getenv("CLOB_API_KEY"),
            "clob_secret": os.getenv("CLOB_SECRET"),
            "clob_pass_phrase": os.getenv("CLOB_PASS_PHRASE"),
            
            # 显示配置
            "default_limit": int(os.getenv("DEFAULT_LIMIT", "50")),
            "table_format": os.getenv("TABLE_FORMAT", "grid"),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self._config[key] = value
    
    def validate(self) -> bool:
        """验证配置是否有效"""
        required_configs = ["clob_api_url"]
        
        for config_key in required_configs:
            if not self.get(config_key):
                print(f"错误: 缺少必需的配置项: {config_key}")
                return False
        
        # 验证URL格式
        api_url = self.get("clob_api_url")
        if not api_url.startswith(("http://", "https://")):
            print(f"错误: API URL格式不正确: {api_url}")
            return False
        
        return True
    
    def print_config(self):
        """打印当前配置（隐藏敏感信息）"""
        print("当前配置:")
        for key, value in self._config.items():
            if "key" in key.lower() or "secret" in key.lower() or "pass" in key.lower():
                display_value = "***隐藏***" if value else "未设置"
            else:
                display_value = value
            print(f"  {key}: {display_value}")


# 全局配置实例
config = Config()
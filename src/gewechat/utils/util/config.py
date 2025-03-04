import yaml
import os

def load_config(config_file=None):
    # 如果没有提供配置文件路径，则使用环境变量或默认路径
    if config_file is None:
        config_file = os.getenv('GEWECHAT_CONFIG_FILE', 'gewechat_client/config.yaml')
    
    # 加载 YAML 配置文件
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # 打印 配置
    return config

# 加载配置
config = load_config()
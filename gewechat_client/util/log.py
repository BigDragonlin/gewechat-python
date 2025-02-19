import logging
from .config import config
print(config["log"])
logging.basicConfig(
    level=config["log"]["level"],
    format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        logging.FileHandler(config["log"]["base_file"], encoding="utf-8")  # 文件输出
    ]
)
logger = logging.getLogger(__name__)

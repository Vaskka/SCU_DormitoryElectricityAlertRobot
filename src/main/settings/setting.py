import os

# 项目根目录
PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# resource 目录
RESOURCE_PATH = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "resource")

# mongodb 配置
MONGO_URI = "mongodb://localhost:27017/"

# db name
MONGO_DB_NAME = "elen"

# user collection
MONGO_USER_COLLECTION_NAME = "user"

# static

STATIC_TEXT = {
    "get_remain": "查电费",
    "turn_off_alert": "关预警",
    "turn_on_alert": "开预警"
}

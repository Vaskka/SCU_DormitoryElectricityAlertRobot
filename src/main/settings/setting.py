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
    "get_remain": {
        0: "查询电费",
        1: "查询电量",
        2: "查电费",
        3: "查电量",
        4: "剩余电费",
        5: "剩余电量"
    },
    "turn_off_alert": "关预警",
    "turn_on_alert": "开预警",


}

REPLY_TEXT = {
    "alert_to_register": "用户未注册，请输入 注册#校区#楼栋数#单元#房间号#子房间号 的格式进行注册，例如： 注册#江安校区#西园7舍#2单元#301#A",
}

# 暂存缓冲
TEMP = {}

# 房间id映射
ROOM_ID_DICT = None

# 图灵API
TULING_API_KEY = '34624e1582524038b38dc0bddce60d3a'

# 电量低的标准
LOW_LINE = 5

# 提醒频率
ALERT_HOURS = 3

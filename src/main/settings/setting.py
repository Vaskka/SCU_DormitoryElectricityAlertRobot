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

# 电量低的标准
LOW_LINE = 5

# 提醒频率
ALERT_HOURS = 3

# static text
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
    "search": {
        "campus": "有效校区",
        "area": "有效围合",
        "unit": "有效单元",
        "room": "有效房间",
        "subRoom": "有效子房间"
    },
    "help": "help"

}

REPLY_TEXT = {
    "alert_to_register": "用户未注册，请输入：\n\n注册#校区#楼栋数#单元#房间号#子房间号\n\n的格式进行注册，例如： 注册#江安校区#西园7舍#2单元#301#A",
    "help": "欢迎使用SCU寝室电量预警机器人～我叫Elen~\n跟Elen聊天的时候非关键指令会由Elen的图灵AI代替回复您哟，以下是关键指令：\n========\n[查询电费, 查询电量, 查电费, 查电量, 剩余电费, 剩余电量]任意发送其中之一即可查询剩余电量\n========\n[关预警, 开预警]分别代表关闭和开启低电量自动提醒功能，如果开启提醒，我会在电量低于" + str(LOW_LINE) + "度时提醒您及时缴费，频率为每" + str(ALERT_HOURS) + "小时一次，此功能默认开启。\n========\n[有效校区, %校区%-有效围合, %校区%-%围合%-有效单元]\n将%xxx%整体替换为过滤条件, 例如：\"江安校区-西园7舍-有效单元\"。每个指令代表获取有效的地址信息，您可以在注册前进行查询，以获取您想要绑定的有效寝室～"
}

# 暂存缓冲
TEMP = {}

# 房间id映射
ROOM_ID_DICT = None

# 图灵API
TULING_API_KEY = '34624e1582524038b38dc0bddce60d3a'



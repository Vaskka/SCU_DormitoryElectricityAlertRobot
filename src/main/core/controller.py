import json
import os
import time

import schedule as schedule
from wxpy import *

from src.main.core import model
from src.main.module.util import *
from src.main.module.db import MongodbHandlerImpl
from src.main.module.log import Log
from src.main.settings import setting

# 控制器类，组织各个模块
class Controller(object):
    # 全局机器人对象，未初始化
    bot = Bot()

    # 全局DAO对象，未初始化
    dao = None

    @staticmethod
    def ele_alert():
        """
        定时任务，更新电量，检查
        :return:
        """

        # 更新全部用户的电量数据
        _dao = MongodbHandlerImpl(setting.TEMP["MONGO_USER_NAME"], setting.TEMP["MONGO_PSW"])

        _dao.update_all_degree()

        # 遍历数据库，拿到全部alert为True且符合要求的wechat_name
        res = _dao.get_object_with_alert(True)

        name_list = []

        for user in res:
            if user["degree"] < setting.LOW_LINE:
                name_list.append((user["wechat_name"], user["degree"]))
            pass

        for row in name_list:
            friend = Controller.bot.friends().search(row[0])[0]
            friend.send("电量提示：当前电量%s度，电量较低请注意缴费。" % str(row[1]))

        pass

    def init(self):
        """
        初始化
        :return:
        """

        # 初始化日志
        Log.init_log()

        # 请求输入数据库用户名和密码
        mongo_user_name = input("请输入mongodb用户名：")
        mongo_psw = input('密码： ')

        # 默认学号and密码
        default_card_id = input("请输入默认学号：")
        default_psw = input("密码：")

        # 检查正确性
        if API.login(card_id=default_card_id, psw=default_psw) is None:
            Log.error("默认的学号或密码不正确")
            exit(1)
            pass
        # 暂存密码用户名
        setting.TEMP["MONGO_USER_NAME"] = mongo_user_name
        setting.TEMP["MONGO_PSW"] = mongo_psw
        setting.TEMP["DEFAULT_CARD_ID"] = default_card_id
        setting.TEMP["DEFAULT_PSW"] = default_psw

        # 初始化doo
        self.dao = MongodbHandlerImpl(mongo_user_name, mongo_psw)
        model.MainModel.dao = self.dao

        # 读取寝室信息数据
        self.read_room_info()

        # 初始化图灵
        self.tuling = Tuling(api_key=setting.TULING_API_KEY)

        # 初始化定时检查预警
        self._init_task()

        pass

    def run(self):
        """
        main run method
        :return:
        """
        if not self.is_debug:
            self.work()
        else:
            self.debug()
        pass

    def work(self):
        """
        非debug运行入口
        :return:
        """
        # 注册自动回复方法
        @self.bot.register(Friend, TEXT)
        def process(msg):

            wechat_obj_id = md5(msg.sender.name)
            wechat_name = str(msg.sender.name)

            # 检查注册
            check_register_result = check_if_register(msg.text)
            if check_register_result[0]:
                # 已经注册返回提示已经注册
                if model.MainModel.check_register(wechat_obj_id):
                    return "您已经注册！"

                # 注册
                res = model.MainModel.do_register(wechat_obj_id, wechat_name,
                                            campus=check_register_result[1][0],
                                            building=check_register_result[1][1],
                                            unit=check_register_result[1][2],
                                            room=check_register_result[1][3],
                                            sub_room=check_register_result[1][4])

                return res
                pass

            # 检查其他功能
            if msg.text in setting.STATIC_TEXT["get_remain"].values() or msg.text in setting.STATIC_TEXT.values():
                # 涉及机器人关键字
                # 首先检查注册状态
                if not self.dao.check_if_user_register(wechat_obj_id):
                    # 未注册，提示注册
                    return setting.REPLY_TEXT["alert_to_register"]
                    pass

                if msg.text in setting.STATIC_TEXT["get_remain"].values():
                    # 查余额
                    remain_res = model.MainModel.get_remain(wechat_obj_id)
                    return remain_res
                    pass
                elif msg.text == setting.STATIC_TEXT["turn_off_alert"]:
                    # 关预警
                    return model.MainModel.set_alert(wechat_obj_id, False)
                    pass
                elif msg.text == setting.STATIC_TEXT["turn_on_alert"]:
                    # 开预警
                    return model.MainModel.set_alert(wechat_obj_id, True)
                    pass
                pass
            pass

            # # 不是主要功能传递给图灵机器人做出回复
            self.tuling.do_reply(msg)

        while True:
            schedule.run_pending()
            time.sleep(1)
            pass
        pass

    def debug(self):
        """
        debug用
        :return:
        """

        pass

    @staticmethod
    def read_room_info():
        """
        读取寝室静态信息
        :return: ID_DICT
        """
        with open(os.path.join(setting.RESOURCE_PATH, "room_id.json"), "r", encoding="utf-8") as f:
            s = f.read()

        obj = json.loads(s)
        setting.ROOM_ID_DICT = obj["contents"]
        pass

    @staticmethod
    def _init_task():
        """
        初始化定时任务
        :return:
        """
        schedule.every(setting.ALERT_HOURS).hours.do(Controller.ele_alert)
        pass



    def __init__(self, is_debug=True):
        self.is_debug = is_debug

        # 图灵机器人对象
        self.tuling = None
        pass



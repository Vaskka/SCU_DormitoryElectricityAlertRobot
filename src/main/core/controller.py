import getpass
import os

from wxpy import *

from src.main.module.db import MongodbHandlerImpl
from src.main.module.log import Log
from src.main.settings import setting

# 控制器类，组织各个模块
class Controller(object):

    def init(self):
        """
        初始化
        :return:
        """

        # 初始化日志
        Log.init_log()

        # 请求输入数据库用户名和密码
        mongo_user_name = input("请输入mongodb用户名：")
        mongo_psw = getpass.getpass('密码： ')

        # 初始化doo
        self.dao = MongodbHandlerImpl(mongo_user_name, mongo_psw)

        # 初始化机器人
        self.bot = Bot()
        self.bot.enable_puid(os.path.join(setting.RESOURCE_PATH, 'wxpy_puid.pkl'))

        pass

    def run(self):
        """
        main run method
        :return:
        """
        if not self.debug:
            self.work()
        else:
            self.debug()
        pass

    def work(self):
        """
        非debug运行入口
        :return:
        """
        pass

    def debug(self):
        """
        debug用
        :return:
        """
        # 注册自动回复方法
        @self.bot.register(Friend, TEXT)
        def process(msg):

            wechat_obj_id = str(msg.sender.puid)
            wechat_name = str(msg.sender.name)

            if msg.text in setting.STATIC_TEXT.values():
                # 涉及机器人关键字
                # 首先检查注册状态
                if not self.dao.check_if_user_register(wechat_obj_id):
                    # 未注册

                    pass

                if msg.text == setting.STATIC_TEXT["get_remain"]:
                    # 查余额
                    pass
                elif msg.text == setting.STATIC_TEXT["turn_off_alert"]:
                    # 关预警
                    pass
                elif msg.text == setting.STATIC_TEXT["turn_on_alert"]:
                    # 开预警
                    pass
                pass
            pass



        while True:
            pass
        pass

    def __init__(self, is_debug=True):
        self.is_debug = is_debug

        # 机器人对象，未初始化
        self.bot = None

        # DAO对象，未初始化
        self.dao = None
        pass



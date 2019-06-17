from abc import ABCMeta, abstractmethod

import pymongo

from src.main.module.exception import WechatObjIdNotFoundException
from src.main.settings import setting


class DBHandler(metaclass=ABCMeta):
    """
    DAO
    """
    def __init__(self, username, psw):
        pass

    @abstractmethod
    def check_if_user_register(self, wechat_obj_id):
        """
        检查是否注册过
        :param wechat_obj_id: 唯一标识，由实现确定
        :return: boolean
        """
        pass

    @abstractmethod
    def register(self, wechat_obj_id, wechat_name, card_id, psw, campus, building, unit, room, sub_room, self_info):
        """
        注册
        :param wechat_obj_id: 唯一标识，由实现确定
        :param wechat_name: 用户名
        :param card_id: 学号
        :param psw: 密码
        :param campus: 校区id 1~3
        :param building: 楼id
        :param unit: 单元id
        :param room: 房间号
        :param sub_room: 子房间号
        :param self_info: 个人信息集合
        :return: None
        """
        pass

    @abstractmethod
    def from_id_get_card_psw(self, wechat_obj_id):
        """
        得到学号密码
        :param wechat_obj_id: 唯一标识，由实现确定
        :return: dict
        """
        pass

    @abstractmethod
    def get_electricity(self, wechat_obj_id):
        """
        查询电费
        :param wechat_obj_id: 唯一标识，由实现确定
        :return: float
        """
        pass

    @abstractmethod
    def set_alert(self, wechat_obj_id, alert):
        """
        设置预警功能
        :param wechat_obj_id:
        :param alert boolean 是否预警
        :return: None
        """
        pass


class MongodbHandlerImpl(DBHandler):
    """
    mongodb 实现
    """

    def set_alert(self, wechat_obj_id, alert):
        if not self.check_if_user_register(wechat_obj_id):
            raise WechatObjIdNotFoundException(wechat_obj_id)

        query = {"wechat_obj_id": wechat_obj_id}
        new_value = {"$set": {"alert": alert}}

        self.user_collection.update_one(query, new_value)
        pass

    def register(self, wechat_obj_id, wechat_name, card_id, psw, campus, building, unit, room, sub_room, self_info):
        result = {
            "wechat_obj_id": wechat_obj_id,
            "wechat_name": wechat_name,
            "card_id": card_id,
            "psw": psw,
            "campus": campus,
            "building": building,
            "unit": unit,
            "room": room,
            "sub_room": sub_room,
            "self_info": self_info,
            "degree": "",
            "alert": True
        }
        self.user_collection.insert_one(result)
        pass

    def from_id_get_card_psw(self, wechat_obj_id):
        if not self.check_if_user_register(wechat_obj_id):
            raise WechatObjIdNotFoundException(wechat_obj_id)

        query = {"wechat_obj_id": wechat_obj_id}
        result = self.user_collection.find(query)

        res = {
            "card_id": result[0]["card_id"],
            "psw": result[0]["psw"]
        }

        return res
        pass

    def get_electricity(self, wechat_obj_id):
        if not self.check_if_user_register(wechat_obj_id):
            raise WechatObjIdNotFoundException(wechat_obj_id)

        query = {"wechat_obj_id": wechat_obj_id}
        result = self.user_collection.find(query)

        return float(result[0]["degree"])
        pass

    def check_if_user_register(self, wechat_obj_id):
        query = {"wechat_obj_id": wechat_obj_id}
        result = self.user_collection.find(query)
        if len(result) == 0:
            return False
        return True
        pass

    def __init__(self, username, psw):
        DBHandler.__init__(self, username, psw)

        # 构造dao
        self.client = pymongo.MongoClient(setting.MONGO_URI)
        self.db = self.client[setting.MONGO_DB_NAME]
        self.user_collection = self.db[setting.MONGO_USER_COLLECTION_NAME]
        pass


from abc import ABCMeta, abstractmethod

import pymongo

from src.main.api.apis import API
from src.main.module import util
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
    def register(self, wechat_obj_id, wechat_name, campus, building, unit, room, sub_room, degree=None):
        """
        注册
        :param wechat_obj_id: 唯一标识，由实现确定
        :param wechat_name: 用户名
        :param campus: 校区id 1~3
        :param building: 楼id
        :param unit: 单元id
        :param room: 房间号
        :param sub_room: 子房间号
        :param degree 电度数，注册时默认None
        :return: None
        """
        pass

    @abstractmethod
    def get_electricity(self, wechat_obj_id):
        """
        查询电费api徐奥的字段
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

    @abstractmethod
    def update_degree(self, wechat_obj_id, degree):
        """
        更新电度
        :param wechat_obj_id: id
        :param degree: 电量
        :return: None
        """
        pass

    @abstractmethod
    def get_object_with_alert(self, alert):
        """
        查询指定alert的record
        :param alert: alert
        :return: records
        """
        pass

    @abstractmethod
    def update_all_degree(self):
        """
        更新全部用户的电度
        :return:
        """
        pass


class MongodbHandlerImpl(DBHandler):
    """
    mongodb 实现
    """

    def update_all_degree(self):

        res = self.user_collection.find()
        for user in res:
            curr_electron = API.get_electricity(campus=user["campus"]["id"], building=user["building"]["id"], unit=user["unit"]["id"], room=user["room"],
                                                sub_room=user["sub_room"], token=util.get_token())
            query = {"wechat_obj_id": user["wechat_obj_id"]}
            new_value = {"$set": {"degree": curr_electron}}

            self.user_collection.update_one(query, new_value)
            pass

        pass

    def get_object_with_alert(self, alert):
        query = {"alert": alert}
        return self.user_collection.find(query)
        pass

    def update_degree(self, wechat_obj_id, degree):
        if not self.check_if_user_register(wechat_obj_id):
            raise WechatObjIdNotFoundException(wechat_obj_id)

        query = {"wechat_obj_id": wechat_obj_id}
        new_value = {"$set": {"degree": degree}}

        self.user_collection.update_one(query, new_value)
        pass

    def set_alert(self, wechat_obj_id, alert):
        if not self.check_if_user_register(wechat_obj_id):
            raise WechatObjIdNotFoundException(wechat_obj_id)

        query = {"wechat_obj_id": wechat_obj_id}
        new_value = {"$set": {"alert": alert}}

        self.user_collection.update_one(query, new_value)
        pass

    def register(self, wechat_obj_id, wechat_name, campus, building, unit, room, sub_room, degree=None):
        result = {
            "wechat_obj_id": wechat_obj_id,
            "wechat_name": wechat_name,
            "campus": campus,
            "building": building,
            "unit": unit,
            "room": room,
            "sub_room": sub_room,
            "degree": degree,
            "alert": True
        }
        self.user_collection.insert_one(result)
        pass

    def get_electricity(self, wechat_obj_id):
        if not self.check_if_user_register(wechat_obj_id):
            raise WechatObjIdNotFoundException(wechat_obj_id)

        query = {"wechat_obj_id": wechat_obj_id}
        result = self.user_collection.find(query)

        return result[0]
        pass

    def check_if_user_register(self, wechat_obj_id):
        query = {"wechat_obj_id": wechat_obj_id}
        result = self.user_collection.find(query)
        if result.count() == 0:
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


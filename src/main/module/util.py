import hashlib

from src.main.api.apis import API
from src.main.settings import setting


def check_if_register(text):
    text = text.strip()

    text_arr = text.split('#')
    if text_arr[0] == "注册" and len(text_arr) == 6:
        return True, text_arr[1:]

    return False, None
    pass


def md5(s):
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return str(md.hexdigest())
    pass


def get_token():
    """
    开发中发现检查电费没有权限限制，只检查token的合法性，故这里用开发者自己的学号和密码获取到的token
    :return:
    """
    data = API.login(card_id=setting.TEMP["DEFAULT_CARD_ID"], psw=setting.TEMP["DEFAULT_PSW"])

    return str(data["token"])
    pass


class RoomUtil:

    @classmethod
    def find_real_campus_id(cls, campus):
        """
        查找校区id
        :param campus: 校区
        :return: 校区对应id
        """

        for cam in setting.ROOM_ID_DICT:
            if cam["name"] == campus:
                return cam["id"]

        return None
        pass

    @classmethod
    def find_real_building_id_and_unit_id(cls, campus_id, building, unit):
        """
        查找楼栋id
        :param campus_id: 校区id
        :param building: 楼栋
        :param unit 单元
        :return: building_id, unit_id
        """
        for cam in setting.ROOM_ID_DICT[campus_id - 1]["dorms"]:
            if cam["name"] == building:
                for _unit in cam["units"]:
                    if unit == _unit["name"]:
                        return _unit["dormId"], _unit["id"]

        return None
        pass

    pass

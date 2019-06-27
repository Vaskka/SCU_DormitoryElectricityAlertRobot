


# 定义与川大后台通信的接口
import json

import requests


class API(object):

    host = "http://202.115.35.195:8088/scu/rest"

    form_data = {
        "timestamp": "1560695163",
        "signature": "3fe9aa5c4529fc9c4f15879af17f2a3430eda02b",
        "nonce": "TCg5MG6mQseu7yV2XJVmt8DnyRQv66a4",
        "type": None,
        "contents": None
    }

    @classmethod
    def login(cls, **params):
        """
        川大后勤授权接口，传递学号和密码，返回个人信息dict（其中token用于其他接口的authorization）
        :param params: 学号 密码
        :return: dict
        """

        content = {
            "cardId": str(params["card_id"]),
            "pwd":str(params["psw"])
        }

        content_str = json.dumps(content)

        cls.form_data["type"] = "3"
        cls.form_data["contents"] = content_str

        res = requests.post(url=cls.host, data=cls.form_data)
        res_obj = json.loads(res.text)

        if res_obj["result"] is not 0:
            return None

        return res_obj["contents"]
        pass

    @classmethod
    def get_electricity(cls, **params):
        """
        川大后勤电费查询接口
        :param params: 传入寝室具体信息，需要authorization
        :return: float 电费余额
        """
        content = {"building":str(params["building"]),
                   "campus":str(params["campus"]),
                   "room": str(params["room"]),
                   "subRoom": str(params["sub_room"]),
                   "token": str(params["token"]),
                   "unit": str(params["unit"])}

        content_str = json.dumps(content)

        cls.form_data["type"] = "8"
        cls.form_data["contents"] = content_str

        res = requests.post(url=cls.host, data=cls.form_data)
        res_obj = json.loads(res.text)

        if res_obj["result"] is not 0:
            return None

        return float(res_obj["contents"]["degree"])
    pass

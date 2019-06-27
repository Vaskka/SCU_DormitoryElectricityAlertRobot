from src.main.api.apis import API
from src.main.module import db, util
from src.main.settings import setting


class MainModel(object):

    # 此处的 dao 在 Controller 初始化时动态注册
    dao = None

    @staticmethod
    def check_register(wechat_obj_id):
        """
        是否已经注册检查
        :param wechat_obj_id id
        :return: dict
        """
        return MainModel.dao.check_if_user_register(wechat_obj_id)
        pass

    @staticmethod
    def do_register( wechat_obj_id, wechat_name,campus, building, unit, room, sub_room):
        """
        执行登录
        :param wechat_obj_id: wechat_obj_id
        :param wechat_name: wechat_name
        :param campus: 校区
        :param building: 楼栋数
        :param unit: 单元
        :param room: 房间
        :param sub_room: 子房间
        :return:
        """

        # 检查寝室信息
        campus_id = util.RoomUtil.find_real_campus_id(campus)
        if campus_id is None:
            return "校区有误，请重新注册。"

        building_id, unit_id = util.RoomUtil.find_real_building_id_and_unit_id(campus_id, building, unit)
        if not building_id or not unit_id:
            return "楼栋号或单元号有误或不存在，请重新注册。"

        curr_electron = API.get_electricity(campus=campus_id, building=building_id, unit=unit_id, room=room, sub_room=sub_room, token=util.get_token())
        if curr_electron is None:
            return "房间号或子房间号有误或不存在，请重新注册。"
            pass

        # 执行注册
        MainModel.dao.register(wechat_obj_id, wechat_name,
                     building={"id": building_id, "content": building},
                     campus={"id": campus_id, "content": campus},
                     unit={"id": unit_id, "content": unit},
                     room=room,
                     sub_room=sub_room,
                     degree=curr_electron)

        if curr_electron < setting.LOW_LINE:
            return "注册成功，当前电量：%s度，剩余电量较低，请注意缴费。" % str(curr_electron)

        return "注册成功，当前电量：%s度。" % str(curr_electron)

        pass

    @staticmethod
    def get_remain(wechat_obj_id):
        """
        获取余额并更新
        :param wechat_obj_id:id
        :return:
        """

        data = MainModel.dao.get_electricity(wechat_obj_id)

        res = API.get_electricity(campus=data["campus"]["id"],
                                  building=data["building"]["id"],
                                  unit=data["unit"]["id"],
                                  room=data["room"],
                                  sub_room=data["sub_room"],
                                  token=util.get_token())

        MainModel.dao.update_degree(wechat_obj_id, res)

        if res < setting.LOW_LINE:
            return "当前电量：%s度，剩余电量较低，请注意缴费。" % str(res)

        return "当前电量：%s度。" % str(res)
        pass

    @staticmethod
    def set_alert(wechat_obj_id, tigger):

        MainModel.dao.set_alert(wechat_obj_id, tigger)

        if tigger:
            text = "开"
        else:
            text = "关"

        return "电量提醒已[%s]" % text
        pass


    pass

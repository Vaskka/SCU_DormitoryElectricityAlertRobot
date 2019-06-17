class DormitoryElectricityException(RuntimeError):
    pass


class WechatObjIdNotFoundException(DormitoryElectricityException):
    """
    用户不存在异常
    """
    def __init__(self, not_found_id):
        DormitoryElectricityException.__init__(self)
        self.not_found_id = not_found_id
    pass

    def __str__(self):
        return "未找到" + self.not_found_id + "的用户。"
        pass

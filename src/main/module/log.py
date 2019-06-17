import logging
import os

from src.main.settings import setting


class Log(object):
    logger = None

    @classmethod
    def init_log(cls):
        # 初始化日志系统
        logging.basicConfig(level=logging.INFO, format='%(asctime)s--%(name)s--%(levelname)s--%(message)s')
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(level=logging.INFO)

        # 文件日志
        handler = logging.FileHandler(os.path.join(setting.RESOURCE_PATH, "pipline.log"))
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s--%(name)s--%(levelname)s--%(message)s')
        handler.setFormatter(formatter)

        cls.logger.addHandler(handler)
        pass

    @classmethod
    def info(cls, message):
        cls.logger.setLevel(level=logging.INFO)
        cls.logger.info(str(message))
        pass

    @classmethod
    def warning(cls, message):
        cls.logger.setLevel(level=logging.WARNING)
        cls.logger.info(str(message))
        pass

    @classmethod
    def error(cls, message):
        cls.logger.setLevel(level=logging.ERROR)
        cls.logger.info(str(message))
        pass

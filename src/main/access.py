# 机器人入口
from wxpy import *

from src.main.core.controller import Controller


def main():

    if len(sys.argv) < 3:
        print("请指定--console参数，用法：--console [true/false]")
        exit(1)

    key = sys.argv[1]
    value = sys.argv[2]

    if key != "--console" or value not in ["true", "false"]:
        print("不支持的命令行参数，目前支持的参数 --console [true/false]")
        exit(2)

    if value == "true":
        console = True
    else:
        console = False

    app = Controller(is_debug=False, console=console)
    app.init()
    app.run()
    pass


if __name__ == '__main__':
    main()
    pass

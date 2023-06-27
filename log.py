import shutil


def info(text: str):
    # 获取终端的宽度
    terminal_width = shutil.get_terminal_size().columns
    # 定义要填充的字符
    fill_char = "="
    # 构建填充字符串
    fill_line = fill_char * terminal_width

    # 打印填充字符串并设置为绿色
    print("\033[0;32m" + fill_line + "\033[0m")
    # 打印绿色的文本
    print("\033[0;32m" + text + "\033[0m")
    # 打印填充字符串并设置为绿色
    print("\033[0;32m" + fill_line + "\033[0m")
    print("\n")


def warn(text: str):
    # 获取终端的宽度
    terminal_width = shutil.get_terminal_size().columns
    # 定义要填充的字符
    fill_char = "="
    # 构建填充字符串
    fill_line = fill_char * terminal_width

    # 打印填充字符串并设置为黄色
    print("\033[0;33m" + fill_line + "\033[0m")
    # 打印黄色的文本
    print("\033[0;33m" + text + "\033[0m")
    # 打印填充字符串并设置为黄色
    print("\033[0;33m" + fill_line + "\033[0m")
    print("\n")


def debug(text: str):
    # 获取终端的宽度
    terminal_width = shutil.get_terminal_size().columns
    # 定义要填充的字符
    fill_char = "="
    # 构建填充字符串
    fill_line = fill_char * terminal_width

    # 打印填充字符串并设置为蓝色
    print("\033[0;34m" + fill_line + "\033[0m")
    # 打印蓝色的文本
    print("\033[0;34m" + text + "\033[0m")
    # 打印填充字符串并设置为蓝色
    print("\033[0;34m" + fill_line + "\033[0m")
    print("\n")

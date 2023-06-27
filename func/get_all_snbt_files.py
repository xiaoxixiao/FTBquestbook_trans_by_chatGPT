import glob
import os


def get_all_snbt_files(directory) -> list:
    # os.path.join用于连接目录和文件名
    # os.path.expanduser用于展开"~"为用户的主目录
    path = os.path.join(os.path.expanduser(directory), '**/*.snbt')

    # glob.glob返回所有匹配的文件路径列表
    # 参数"recursive=True"允许对子目录进行递归搜索
    files = glob.glob(path, recursive=True)

    return files

def get_all_json_files(directory) -> list:
    # os.path.join用于连接目录和文件名
    # os.path.expanduser用于展开"~"为用户的主目录
    path = os.path.join(os.path.expanduser(directory), '**/*.json')

    # glob.glob返回所有匹配的文件路径列表
    # 参数"recursive=True"允许对子目录进行递归搜索
    files = glob.glob(path, recursive=True)

    return files

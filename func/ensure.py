import ast

import log


def ensure_equal_length(list1, list2):
    # 判断列表1和列表2长度是否一致
    if len(list1) == len(list2):
        log.info("列表长度一致，无需人工翻译")
        return list2
    else:
        while True:  # 使用while循环持续获取用户输入，直到输入的列表长度与列表1一致为止
            user_input = input("请输入人工翻译文本:" + "（请输入列表格式，元素数量需要" +
                               str(len(list1)) + "个元素)")
            try:
                # 尝试将用户输入的字符串转换为列表
                user_list = ast.literal_eval(user_input)
                # 检查转换后的对象是否是列表
                if isinstance(user_list, list):
                    # 如果用户输入的列表长度与列表1一致，则返回输入的列表
                    if len(user_list) == len(list1):
                        return user_list
                    else:
                        log.warn("非法字段，请输入列表并包含" + str(len(list1)) + "元素")
                else:
                    log.warn("非法字段，请输入列表格式")
            except (ValueError, SyntaxError):
                log.warn("非法字段，请输入列表格式")

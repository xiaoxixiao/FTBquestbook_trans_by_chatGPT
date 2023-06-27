import json

import log

import json


def flatten_json_list(json_str: str):
    decoded_list = json.loads(json_str)  # 解码 JSON 列表
    result = []
    result_list = []

    for item in decoded_list:
        if isinstance(item, str) and item.startswith('[') and item.endswith(']'):
            # 如果元素是字符串表示的列表，将其解码并添加到结果中
            result.extend(json.loads(item))
        else:
            # 否则，直接添加元素
            result.append(item)

    for item in result:
        # 如果item是一个列表，将其添加到结果列表中
        if isinstance(item, list):
            result_list.extend(item)
        # 否则，直接添加元素
        else:
            result_list.append(item)

    return result_list


def lists_to_dict(list1: list, list2: list):
    # 检查两个列表的长度是否相同
    if len(list1) != len(list2):
        raise ValueError("两个列表的长度不相同")

    # 使用 zip() 函数将两个列表的元素打包成元组，然后转换为字典
    return dict(zip(list1, list2))


def sort_dict_by_key_length(dictionary):
    # 使用 sorted() 函数和自定义排序函数对字典进行排序
    sorted_dict = sorted(dictionary.items(), key=lambda item: len(item[0]), reverse=True)

    # 将排序后的列表 of tuples 转换回字典
    return dict(sorted_dict)


def replace_translated(original_file: str, o_t_dict: dict):
    # 读取原始文件
    with open(original_file, "r", encoding="utf-8") as f:
        original_text: str = f.read()

    # 遍历字典
    for key, value in o_t_dict.items():
        original_text = original_text.replace(key, value)

    # 将替换后的文本写入文件
    with open(original_file, "w", encoding="utf-8") as f:
        f.write(original_text)



if __name__ == "__main__":
    # 读取translated_list.json文件  该文件是翻译后的文本
    with open("output/translated_list.json", "r", encoding="utf-8") as file:
        translated_list: list = json.loads(file.read())

    # 读取extracted_text.json文件  该文件是提取的文本
    with open("output/extract_text.json", "r", encoding="utf-8") as file:
        extracted_text: list = json.loads(file.read())

    # 将两个列表转换为字典
    extracted_trans_dict = lists_to_dict(extracted_text, translated_list)

    # 按照键的长度进行排序
    sorted_dict = sort_dict_by_key_length(extracted_trans_dict)

    log.info(text="排序后的字典为：" + str(sorted_dict))

    replace_translated("start_here.snbt", sorted_dict)

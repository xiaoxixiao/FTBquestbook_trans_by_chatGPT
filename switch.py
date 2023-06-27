import json
import time


def switch_origin_trans(original_to_translate_dict_path: str, original_file: str) -> str:
    # 将字典格式的txt文件转换为字典
    with open(original_to_translate_dict_path, 'r', encoding='utf-8') as f:
        original_to_translate_dict_ = f.read()
    original_to_translate_dict = json.loads(original_to_translate_dict_)
    print("原始文本与翻译文本对照字典为：", original_to_translate_dict, "\n\n==========")
    print("对照字典当前格式:", type(original_to_translate_dict))
    # 字典的键为原始文本，值为翻译后的文本
    # 将字典转换为列表
    dict_list = []
    for key, value in original_to_translate_dict.items():
        dict_list.append({key: value})
    print("字典列表为：", dict_list, "\n\n==========")
    # 以列表元素中字典键的长度排序，从长到短，排序时移动整个键值对
    dict_list.sort(key=lambda x: len(list(x.keys())[0]), reverse=True)

    print(type(dict_list), "排序后的字典列表为：", dict_list, "\n\n==========")
    # 将原始文件文本替换为翻译后的文本
    with open(original_file, 'r', encoding='utf-8') as f:
        original_text = f.read()
    print("读取原始文本 - done\n\n==========")
    # 遍历列表中的每个字典，将原始文本替换为翻译后的文本
    for item in dict_list:
        original_text = original_text.replace(list(item.keys())[0], list(item.values())[0])
        print("已将", list(item.keys())[0], "替换为", list(item.values())[0])
    print("替换原始文本 - done\n\n==========")
    trans_text = original_text
    print("替换后的文本为：", trans_text, "\n\n==========")

    return trans_text


if __name__ == "__main__":
    original_to_translate_dict_path = input("请输入原始文本与翻译文本对照字典：")
    # 打开原始文本与翻译文本对照字典
    with open(original_to_translate_dict_path, 'r', encoding='utf-8') as f:
        original_to_translate_dict = json.load(f)
    original_file = input("请输入原始文本文件：")

    switch_origin_trans(original_to_translate_dict_path=original_to_translate_dict_path, original_file=original_file)

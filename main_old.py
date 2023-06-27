import ast
import json
import time

import switch
import translater
from SnbtToJson import snbt_to_json


def read_json_file(file_path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_to_str(data: list) -> str:
    elements = []
    for i, item in enumerate(data):
        if isinstance(item, str):
            item_str = f'"{item}"'
        else:
            item_str = str(item)
        elements.append(item_str)

    list_str = ', '.join(elements)
    return f'[{list_str}]'


def save_text_to_file(text: str, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)


# 提取json中特定的键值对
def extract_text_from_json(data: dict) -> list:
    texts = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key in ['description', 'subtitle', 'title']:
                if isinstance(value, str):
                    texts.append(value)
                elif isinstance(value, list):
                    texts.extend(value)
            else:
                texts.extend(extract_text_from_json(value))
    elif isinstance(data, list):
        for item in data:
            texts.extend(extract_text_from_json(item))
    return texts


def make_original_translate_dict(original_list: str, translated_list: str) -> dict:
    def text_to_list(text):
        # 使用 ast.literal_eval() 将字符串转换为列表
        try:
            items = ast.literal_eval(text)
        except (SyntaxError, ValueError):
            items = []

        return items

    original_list = text_to_list(original_list)
    translated_list = text_to_list(translated_list)

    translation_dict = {}

    for original, translated in zip(original_list, translated_list):
        translation_dict[original] = translated

    return translation_dict


def main():
    wait_to_trans_file = snbt_to_json()
    # 出示文件为wait_to_trans_file减去前面的output/
    original_file = wait_to_trans_file.lstrip("output/")
    original_file = original_file.replace(".json", ".snbt")
    print("原始文件为：", original_file)

    # 读取json文件
    wait_to_trans_json = read_json_file(wait_to_trans_file)

    # 提取json中特定的键值对
    texts = extract_text_from_json(wait_to_trans_json)
    print("提取的文本为：", texts, '\n\n==========')
    texts_out_put_path = "output/extract_text.txt"
    with open(texts_out_put_path, 'w', encoding='utf-8') as f:
        f.write(str(texts))

    # 分割列表
    def split_list_by_length(lst, max_length):
        current_length = 0
        result = []
        temp = []

        for item in lst:
            item_length = len(item)

            # 如果添加新元素后长度超过 max_length
            if current_length + item_length > max_length:
                # 把之前的元素添加到结果列表中
                result.append(temp)
                # 开始新的列表
                temp = [item]
                # 重置当前长度
                current_length = item_length
            else:
                # 添加元素到当前列表中
                temp.append(item)
                # 增加当前长度
                current_length += item_length

        # 把最后的元素添加到结果列表中
        if temp:
            result.append(temp)

        return result

    text_list = split_list_by_length(lst=texts, max_length=1000)
    print(text_list)

    # 将列表中的每个元素转换为字符串，然后翻译
    trans_text_list = []
    i = 1

    for text in text_list:
        text_list_len = len(text)
        print("\n\n待翻译文本:" + str(text) + '\n', "列表长度:" + str(len(text_list)) + '\n\n==========')

        # 将待翻译列表遍历
        trans_text__list = []
        # 去除text中的空字符串，空集
        text = [text for text in text if text.strip()]
        for item_count, item in enumerate(text, start=1):
            item_wait_trans: str = f"{item_count}:" + str(item)
            trans_text__list.append(item_wait_trans)
            print(item_count)
        # 去除trans_text__list中的空字符串，空集
        trans_text__list = [text for text in trans_text__list if text.strip()]
        print("处理后的列表:", str(trans_text__list), f"\n==========列表长度:", str(len(trans_text__list)))

        trans_text = translater.translate_text(str(trans_text__list))
        trans_text_list.append(trans_text)

        trans_text = eval(trans_text)
        print("trans_text:" + str(trans_text) + '\n\n==========列表长度:', str(len(trans_text)))

        if len(trans_text__list) != len(trans_text):  # 如果翻译后的文本长度与原文不一致
            print("翻译后的文本长度与原文不一致")
            # 终止程序
            exit()

        # 保存翻译的文本到文件 -> output/trans_split/f'trans_text_{i}.txt'
        with open(f"output/trans_split/trans_text_{i}.txt", "w", encoding="utf-8") as file:
            file.write(str(trans_text))
        # 保存对照原文组
        with open(f"output/trans_split/original_text_{i}.txt", "w", encoding="utf-8") as file:
            file.write(str(text))
        i += 1
        # 休眠20s
        time.sleep(10)

    print("trans_text_list:" + str(trans_text_list) + '\n\n==========')

    trans = []

    # 遍历 trans_text_list
    for sublist in trans_text_list:
        print(type(sublist))
        if isinstance(sublist, str):  # 如果是字符串
            # 将字符串转换为列表
            sublist = ast.literal_eval(sublist)
        # 遍历每一个子列表
        for item in sublist:
            # 将每个元素添加到flattened_list中
            trans.append(item)

    trns = str(trans)

    # # 翻译
    # trns = translater.translate_text(text)
    # 保存翻译的文本到文件
    save_text_to_file(trns, wait_to_trans_file.replace(".json", "-zh.txt"))

    # 获取原文与翻译对照字典
    text = str(texts)
    original_translate_dict = make_original_translate_dict(text, trns)
    original_translate_dict_json = json.dumps(original_translate_dict, indent=4, ensure_ascii=False)
    original_translate_dict_str = str(original_translate_dict_json)
    save_text_to_file(original_translate_dict_str, "output/original_translate_dict.txt")
    original_translate_dict = read_json_file("output/original_translate_dict.txt")

    # 以键的长度对原始字典进行排序，并将结果存储为列表
    sorted_dict_items = sorted(original_translate_dict.items(), key=lambda x: len(x[0]), reverse=True)

    # 将排序后的列表转化为字典
    original_translate_dict = dict(sorted_dict_items)
    print("排序后的字典：", original_translate_dict)

    # # 将字典每个键值对提取出成为单独的字典，然后放入新的列表中
    # original_translate_dict_list = []
    # for key, value in original_translate_dict.items():
    #     original_translate_dict_list.append({key: value})
    #
    # # 读取列表中每个字典的键，根据键的长度进行排序，从长到短
    # original_translate_dict_list.sort(key=lambda x: len(list(x.keys())[0]), reverse=True)
    # print("排序后的列表：", original_translate_dict_list)
    #
    # # 将排序后的列表转换为字典
    # original_translate_dict = {}
    # for item in original_translate_dict_list:
    #     original_translate_dict.update(item)
    # print("排序后的字典：", original_translate_dict)

    trans_text_done = switch.switch_origin_trans(original_to_translate_dict_path="output/original_translate_dict.txt",
                                                 original_file=original_file)
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(trans_text_done)


if __name__ == '__main__':
    main()

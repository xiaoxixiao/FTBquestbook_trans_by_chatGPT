import ast
import json
import time

import lists_to_dict
import translater
from SnbtToJson import snbt_to_json
import log


def split_list_by_length(lst: list, max_length: int) -> list:
    result = []
    current_sublist = []

    for item in lst:
        current_sublist.append(item)

        # 如果添加新元素后子列表的元素数量超过 max_length
        if len(current_sublist) >= max_length:
            # 把之前的元素添加到结果列表中
            result.append(current_sublist)
            # 开始新的列表
            current_sublist = []

    # 把最后的元素添加到结果列表中
    if current_sublist:
        result.append(current_sublist)

    return result


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


def main():
    wait_to_trans_file, original_file_path = snbt_to_json()
    log.info(text="转换后的json文件地址:" + wait_to_trans_file)
    # 出示文件为wait_to_trans_file减去前面的output/
    original_file = wait_to_trans_file.lstrip("output/")
    original_file = original_file.replace(".json", ".snbt")
    log.info(text="原始文件为：" + original_file)

    # 读取json文件
    with open(wait_to_trans_file, 'r', encoding="utf-8") as file:
        wait_to_trans_json: str = file.read()

    # 提取json中特定的键值对
    wait_to_trans_json_dict: dict = json.loads(wait_to_trans_json)
    texts: list = extract_text_from_json(wait_to_trans_json_dict)
    # 移除空元素，如：["", ""] -> []
    texts = [text for text in texts if text.strip() != ""]
    log.info(text="提取的文本为：" + str(texts) + "提取的文本")
    texts_out_put_path: str = "output/extract_text.json"
    texts_json_list = json.dumps(texts, indent=4)
    # 保存提取的文本
    with open(texts_out_put_path, 'w', encoding='utf-8') as f:
        f.write(texts_json_list)

    # 分割列表
    split_texts = split_list_by_length(texts, 10)
    log.info(text="文本已分割完毕")
    # 保存分割后的文本
    with open("output/split_extract_text.json", 'w', encoding='utf-8') as f:
        json.dump(split_texts, f, indent=4)
    log.info("分割的文本为:" + str(json.dumps(split_texts, indent=4, ensure_ascii=False)))

    # 遍历分割后的文本，翻译
    def translate(lst: list):
        result = []
        for text in lst:
            log.info(text="正在翻译:" + json.dumps(text, indent=4, ensure_ascii=False))
            # 开始翻译  translated_text为翻译后的文本
            translated_text = translater.translate_text(str(text))
            time.sleep(15)
            log.info("翻译结果为:" + translated_text)
            try:
                logtext_ = json.loads(translated_text)
                log_text = json.dumps(logtext_, indent=4, ensure_ascii=False)
                log.info("格式化翻译结果:"+log_text)
            except Exception as e:
                log.warn("格式化翻译结果失败:"+str(e)+"可能需要重新翻译，或者手动翻译")
                translated_text = input("请输入人工翻译结果（可以按ctrl+c终止程序）:")

            # 判断前后列表长度是否相等
            translated_text_list0len: list = ast.literal_eval(translated_text)
            if len(text) != len(translated_text_list0len):
                log.warn("翻译前后列表长度不相等，可能需要重新翻译，或者手动翻译")
                translated_text = input("请输入人工翻译结果（可以按ctrl+c终止程序）:")
                translated_text_list0len: list = json.loads(translated_text)
                if len(text) != len(translated_text_list0len):
                    log.warn("翻译前后列表长度不相等，终止程序"+f"\n原始长度:{len(text)}\n翻译后长度:{len(translated_text_list0len)}")
                    exit()
            elif len(text) == len(translated_text_list0len):
                log.info("翻译前后列表长度相等，继续")
            # 将翻译结果添加到结果列表中
            translated_text = ast.literal_eval(translated_text)     # 转换为list
            result.append(translated_text)
            result = json.dumps(result, indent=4, ensure_ascii=False)   # 格式化输出, result为str
            log.info("当前列表:"+str(result))
            result = json.loads(result)  # 转换为list

        return result

    translated_texts = translate(split_texts)
    log.info("翻译结果为:" + str(json.dumps(translated_texts, indent=4, ensure_ascii=False)))
    with open("output/translated_text.json", 'w', encoding='utf-8') as f:
        json.dump(translated_texts, f, indent=4, ensure_ascii=False)

    with open("output/translated_text.json", "r", encoding="utf-8") as file:
        json_data: str = file.read()
    result = lists_to_dict.flatten_json_list(json_data)
    log.info(text="结果为：" + str(result) + "类型为：" + str(type(result)))
    trans_list = result

    # 读取json    output/extract_text.json    列表
    with open("output/extract_text.json", "r", encoding="utf-8") as file:
        extract_text: list = json.loads(file.read())

    # 将两个列表转换为字典
    extracted_trans_dict = lists_to_dict.lists_to_dict(extract_text, trans_list)

    # 按照键的长度进行排序
    sorted_dict = lists_to_dict.sort_dict_by_key_length(extracted_trans_dict)

    log.info(text="排序后的字典为：" + str(sorted_dict))

    # 将原始文件中的文本替换为翻译后的文本
    lists_to_dict.replace_translated(original_file_path, sorted_dict)


if __name__ == '__main__':
    main()

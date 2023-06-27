import json

import log


# def replace_text(original_json_str, extracted_texts_str, translated_texts_str):
#     # Convert JSON strings to Python data structures
#     original_json = json.loads(original_json_str)
#     extracted_texts = json.loads(extracted_texts_str)
#     translated_texts = json.loads(translated_texts_str)
#
#     if isinstance(original_json, dict):
#         new_json = {}
#         for key, value in original_json.items():
#             if isinstance(value, (dict, list)):
#                 new_json[key] = replace_text(json.dumps(value), extracted_texts_str, translated_texts_str)
#             else:
#                 for extracted, translated in zip(extracted_texts, translated_texts):
#                     if value == extracted.get(key, None):
#                         value = translated.get(key, None)
#                         break
#                 new_json[key] = value
#         return new_json
#
#     elif isinstance(original_json, list):
#         new_list = []
#         for item in original_json:
#             new_list.append(replace_text(json.dumps(item), extracted_texts_str, translated_texts_str))
#         return new_list
#
#     else:
#         return original_json

def replace_text(original_json_str, extracted_texts_str, translated_texts_str):
    # log.info(f"原始文本：{original_json_str}\n类型：{type(original_json_str)}")
    # log.info(f"提取文本：{extracted_texts_str}\n类型：{type(extracted_texts_str)}")
    # log.info(f"翻译文本：{translated_texts_str}\n类型：{type(translated_texts_str)}")
    # 将json字符串转为python字典
    original_json = json.loads(original_json_str)
    extracted_texts = json.loads(extracted_texts_str)
    translated_texts_str = json.loads(translated_texts_str)

    log.info(f"转换后原始文本类型：{type(original_json)}")
    log.info(f"转换后提取文本类型：{type(extracted_texts)}")
    log.info(f"转换后翻译文本类型：{type(translated_texts_str)}")

    # 遍历替换
    for dict1, dict2 in zip(extracted_texts, translated_texts_str):
        for key, value in dict1.items():
            original_json = find_and_replace_matching_dicts(original_json, key, value, dict2[key])

    return original_json


def find_and_replace_matching_dicts(d, target_key, target_value, new_value):
    # 如果d是字典
    if isinstance(d, dict):
        # 判断该字典是否包含目标键值对
        if d.get(target_key) == target_value:
            # 如果包含，替换该键值对
            d[target_key] = new_value
        # 对于字典中的每个值v，如果它也是一个字典或列表，递归调用此函数进行替换
        for v in d.values():
            find_and_replace_matching_dicts(v, target_key, target_value, new_value)
    # 如果d是列表
    elif isinstance(d, list):
        # 遍历列表的所有元素，对每个元素，如果它是一个字典或列表，递归调用此函数进行替换
        for item in d:
            find_and_replace_matching_dicts(item, target_key, target_value, new_value)
    return d

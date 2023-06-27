import ast
import os

import snbtlib

import translater
from func import get_all_snbt_files as Snbt
from func import find_keys_in_dict as Find
from func import split_list as Split
from func import ensure as Ensure
from func import replace as Replace
import log
import json


def main():
    # 第一步，读取源文件 需要获取的信息有：文件名 -- original_filename，文件内容 -- original_content
    # 遍历 input_here 文件夹，获取所有 .snbt 文件
    files = Snbt.get_all_snbt_files('input_here')
    log.info('已获取所有 .snbt 文件: ' + str(files))

    # 如果文件夹为空，退出程序
    if len(files) == 0:
        log.warn('文件夹为空，程序退出')
        exit(0)

    # 遍历files，读取文件内容
    for item in files:
        # 获取文件名
        original_filename = item.split('\\')[-1].split('.')[0]
        log.info(f"获取到的文件名为：{original_filename}")
        pass
        with open(item, 'r', encoding='utf-8') as f:
            original_content = f.read()
            # snbt内容转换为json
            json_context = snbtlib.loads(original_content, format=True)
            # 保存json，如果文件夹不存在，创建文件夹
            if not os.path.exists('output/snbt_json'):
                os.makedirs('output/snbt_json')
            with open("output/snbt_json/" + original_filename + '.json', 'w', encoding='utf-8') as f_i:
                f_i.write(json_context)

    # 遍历output/snbt_json文件夹，读取 .json 文件内容
    files_output = Snbt.get_all_json_files('output/snbt_json')
    for item in files_output:
        # 获取文件名
        original_filename = item.split('\\')[-1].split('.')[0]
        with open(item, 'r', encoding='utf-8') as f:
            original_content = f.read()
            # str内容转换为dict
            original_content_dict = json.loads(original_content)  # original_content_dict是原始文本字典
            # 递归查找 所有 title，subtitle，description 键值对
            result = Find.find_keys_in_dict(original_content_dict, ['title', 'subtitle', 'description'])
            result = json.dumps(result, ensure_ascii=False, indent=4)
            log.info('已获取所有: ' + str(result) + "\n列表元素数量为：" + str(len(json.loads(result))))
            # 保存提取结果，如果文件夹不存在，创建文件夹
            if not os.path.exists('output/extract'):
                os.makedirs('output/extract')
            with open("output/extract/" + original_filename + "_extract" + '.json', 'w', encoding='utf-8') as f__:
                f__.write(result)

            # 10个一组，进行翻译    result_是一个列表，子元素为10个一组的列表
            result_ = Split.split_list(json.loads(result), 10)
            result_translated = []

            # 遍历result_，进行翻译
            for item_ in result_:
                log.info("正在翻译：" + str(json.dumps(item_)))
                result = translater.translate_text(str(item_))

                result = result.replace('，', ',')
                log.info("翻译结果为：" + str(result) + str(type(result)))

                result = ast.literal_eval(result)
                result = Ensure.ensure_equal_length(item_, result)
                result_translated.extend(result)
                log.info(
                    "当前大列表为:" + str(result_translated) + '\n\n已翻译：' + str(result) + f'\n{str(type(result))}')

            # 翻译完成 保存翻译结果，如果文件夹不存在，创建文件夹
            if not os.path.exists('output/translate'):
                os.makedirs('output/translate')
            with open("output/translate/" + original_filename + '.json', 'w', encoding='utf-8') as f_:
                f_.write(json.dumps(result_translated, ensure_ascii=False, indent=4))

            # # 开始替换
            # original_json = json.dumps(original_content_dict, ensure_ascii=False, indent=4)
            # with open("output/extract/" + original_filename + "_extract" + '.json', 'r', encoding='utf-8') as f__:
            #     extracted_texts = f__.read()
            # with open("output/translate/" + original_filename + '.json', 'r', encoding='utf-8') as f_:
            #     translated_texts = f_.read()
            #
            # # 获取替换后的json
            # new_json = Replace.replace_text(original_json_str=original_json, extracted_texts_str=extracted_texts,
            #                                 translated_texts_str=translated_texts)
            # new_json = json.dumps(new_json, ensure_ascii=False, indent=4)
            # # 将json转为snbt
            # new_snbt = snbtlib.dumps(json.loads(new_json))
            # # 保存snbt
            # with open("output/" + original_filename + '.snbt', 'w', encoding='utf-8') as f_f:
            #     f_f.write(new_snbt)


            # 开始替换
            # 获取对应原始文本的json
            original_filename = original_filename.split('.')[0]
            with open("output/snbt_json/" + original_filename + '.json', 'r', encoding='utf-8') as f__:
                original_json = f__.read()
            log.info(f"以获取原始文本，文件名为：{original_filename}，类型为：{type(original_json)}")

            # 如果是str类型，转为dict
            if isinstance(original_json, str):
                original_json = json.loads(original_json)
                log.info(f"{original_filename}已转换为dict，类型为：{type(original_json)}")
            # 将dict转为json
            original_json = json.dumps(original_json, ensure_ascii=False, indent=4)
            log.info(f"{original_filename}已转换为json，类型为：{type(original_json)}")

            # 获取提取和翻译后的json
            with open("output/extract/" + original_filename + "_extract" + '.json', 'r', encoding='utf-8') as f__:
                extracted_texts = f__.read()
            with open("output/translate/" + original_filename + '.json', 'r', encoding='utf-8') as f_:
                translated_texts = f_.read()

            # 获取替换后的json
            new_json = Replace.replace_text(original_json_str=original_json, extracted_texts_str=extracted_texts,
                                            translated_texts_str=translated_texts)
            log.info(f"已获取替换后的json，类型为：{type(new_json)}")

            # 如果是str类型，转为dict
            if isinstance(new_json, str):
                new_json = json.loads(new_json)
                log.info(f"已转换为dict，类型为：{type(new_json)}")
            # 将dict转为snbt
            new_snbt = snbtlib.dumps(new_json)
            log.info(f"已转换为snbt，类型为：{type(new_snbt)}")
            # 保存snbt，如果文件夹不存在，创建文件夹
            if not os.path.exists('output'):
                os.makedirs('output')
            with open("output/" + original_filename + '.snbt', 'w', encoding='utf-8') as f_f:
                f_f.write(new_snbt)
            log.info(f"已保存snbt，文件名为：{original_filename}.snbt")


if __name__ == '__main__':
    main()

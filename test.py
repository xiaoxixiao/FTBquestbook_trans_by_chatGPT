# 开始替换
import json

import snbtlib

import log
from func import replace as Replace

item = "input_here/nether_things.snbt"
original_filename = item.split('/')[-1].split('.')[0]
log.info('正在处理文件：' + original_filename)

# 获取文件内容    original_content是原始文本
with open(item, 'r', encoding='utf-8') as f:
    original_content = f.read()
# 将str转换为json str
original_content = snbtlib.loads(original_content, format=True)
log.info('已获取文件内容：' + original_content)

# str内容转换为dict
if isinstance(original_content, str):
    original_content_dict = json.loads(original_content)  # original_content_dict是原始文本字典
    log.info('已将文件内容转换为字典：' + str(type(original_content_dict)))

# 将字典转换为json
original_json = json.dumps(original_content_dict, ensure_ascii=False, indent=4)
log.info('已将字典转换为json：' + str(type(original_json)))

# 获取提取的文本   获取翻译的文本
with open("output/extract/" + original_filename + "_extract" + '.json', 'r', encoding='utf-8') as f__:
    extracted_texts = f__.read()
with open("output/translate/" + original_filename + '.json', 'r', encoding='utf-8') as f_:
    translated_texts = f_.read()

# 获取替换后的json
new_json = Replace.replace_text(original_json_str=original_json, extracted_texts_str=extracted_texts,
                                translated_texts_str=translated_texts)
log.info(f"替换后的数据类型为：{str(type(new_json))}")
# 如果是str，转为dict
if str(type(new_json)) == "<class 'str'>":
    new_json = json.loads(new_json)
    log.info(f"已将str转换为dict：{str(type(new_json))}")
# 将dict转为snbt
new_snbt = snbtlib.dumps(new_json)
# 保存snbt
with open("output/" + original_filename + '.snbt', 'w', encoding='utf-8') as f_f:
    f_f.write(new_snbt)

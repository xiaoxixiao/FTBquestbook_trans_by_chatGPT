import json
import re


def snbt_to_json():
    snbtfile = input("请输入文件名：(例如：yourfile.snbt)")

    with open(snbtfile, 'r', encoding="utf-8") as file:
        # 读取文件内容
        js_code = file.read()

    pattern = r"(\})(\s*\n\s*\{)"
    fixed_text1 = re.sub(pattern, r"\1,\2", js_code)

    pattern = r'([a-zA-Z0-9_]+):(?=\s|$)'
    fixed_text2 = re.sub(pattern, r'"\1":', fixed_text1)

    pattern = r'\]((?:\s*,)*\s*\n)'
    fixed_text3 = re.sub(pattern, r'],\1', fixed_text2)

    pattern = r'\}((?:\s*(?!,|\n))*\s*\n)'
    fixed_text4 = re.sub(pattern, r'},\1', fixed_text3)

    # 对每一个匹配到的模式添加一个逗号
    fixed_text5 = re.sub(r'(true|false)(?=\s|$)', r'\1,', fixed_text4)

    # 将满足条件的 'd' 替换为逗号
    fixed_text6 = re.sub(r'd(?=\n)', ',', fixed_text5)

    # 将满足条件的 'b' 替换为逗号
    fixed_text7 = re.sub(r'b(?=\n)', ',', fixed_text6)

    # 将满足条件的 'f' 替换为逗号
    fixed_text8 = re.sub(r'f(?=\n)', ',', fixed_text7)

    # 对每一个匹配到的模式添加一个逗号
    fixed_text9 = re.sub(r'(?<=[a-z0-9""])(?=\n|$)', ',', fixed_text8)

    # 将大写字母 "L"（如果后面是空格或换行）替换为逗号
    fixed_text10 = re.sub(r'L(?=\s|$)', ',', fixed_text9)

    # 删除对象或列表的尾随逗号
    fixed_text11 = re.sub(r',\s*([}\]])', r'\1', fixed_text10)

    # 删除文本末尾的逗号
    fixed_text = re.sub(r',\s*$', '', fixed_text11)

    print(fixed_text)

    json_data = json.loads(fixed_text)

    output_name = snbtfile.replace(".snbt", ".json")
    putput_path = "output/" + output_name

    # 将转换后的数据写入文件
    with open(putput_path, 'w') as file:
        json.dump(json_data, file, indent=4)

    return putput_path, snbtfile


if __name__ == '__main__':
    snbt_to_json()

def replace_single_quotes_with_double_quotes(text: str) -> str:
    # 将单引号替换为双引号
    text = text.replace("'", '"')
    return text


if __name__ == "__main__":
    text_path = input("请输入文件路径：")
    with open(text_path, 'r', encoding="utf-8") as file:
        text = file.read()
    replace_text = replace_single_quotes_with_double_quotes(text)
    print("替换完成！" + str(replace_text))
    with open(text_path, 'w', encoding="utf-8") as file:
        file.write(replace_text)
    print("写入完成！")

def split_list(input_list, size):
    return [input_list[i:i+size] for i in range(0, len(input_list), size)]
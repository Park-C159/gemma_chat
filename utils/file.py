import os
import re


def append_to_file(filename, content):
    # 以追加模式打开文件
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content)


def check_file_exists(filepath):
    # 判断文件是否存在
    if os.path.exists(filepath):
        return True
    else:
        return False


def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()  # 读取文件的所有内容
        return content
    except FileNotFoundError:
        print(f"文件 '{filepath}' 未找到。")
        return None
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


def parse_conversation(text):
    # 去除前两行
    text = '\n'.join(text.splitlines()[2:])

    # 正则表达式匹配 <start_of_turn> 和 <end_of_turn> 之间的内容
    pattern = re.compile(r'<start_of_turn>(user|model)\n(.*?)<end_of_turn>', re.DOTALL)

    # 查找所有符合正则表达式的内容
    matches = pattern.findall(text)

    # 根据匹配的内容生成标记后的对话
    conversations = []
    for role, content in matches:
        if role == "user":
            conversations.append(f"#### 用户：\n{content.strip()}")
        elif role == "model":
            conversations.append(f"#### Gemma：\n{content.strip()}")

    return conversations


def delete_file(file_path):
    """Deletes a file at the given path."""
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False

import json
import os

def read_result(file_name):
    """
    读取并解析指定JSON文件名中的结果,将JSON数据解析为Python对象并返回。

    参数:
    file_name (str): 文件名。

    返回:
    对象: 解析自文件的JSON数据。
    """
    with open(file_name, 'r') as f:
        return json.load(f)



def is_want(disc):
    """
    判断给定的错误信息是否存在于预定义的错误列表中。

    参数:
    - disc (dict): 包含错误信息的字典，预期包含键 'error_message'。

    返回:
    - index (int): 如果错误信息存在于预定义的错误消息列表中，则返回其索引位置；
                   如果不存在，返回 -1。
    """
    # 预定义的错误消息列表
    error_msg = ["Undefined variable '__main__'","No name 'a' in module 'json'","Method 'foo' has no argument","Method 'bar' should have \"self\" as first argument" ]
    try:
        # 尝试获取给定错误信息在预定义错误消息列表中的索引位置。
        index = error_msg.index(disc['error_message'])
    except:
        # 如果给定的错误信息不在列表中，则设定索引为 -1。
        index = -1

    # 返回索引位置，用于指示错误信息是否需要特别处理。
    return index



def improve(result, improved_name):
    """
    根据分析结果生成改进后的代码示例，并保存到文件中。

    参数:
    result -- 包含错误信息的字典，用于生成改进代码。
    improved_name -- 保存改进后代码示例的文件名。

    返回:
    无返回值，但会生成一个包含改进代码示例的文件。
    """
    # 初始化改进后的错误列表和对应的改进代码列表
    improved = []
    improved_code = ["if __name__ == '__main__':","import json","    def foo(self):","    def bar(self,a):"]

    # 遍历分析结果中的错误信息
    for error in result['Error(s)']:
        # 使用walrus操作符在判断语句中同时赋值和检查索引
        if (index := is_want(error)) != -1:
            # 将错误行和对应的改进代码添加到改进后的错误列表中
            improved.append({
                'error_line': error['error_line'],
                'improved_result': improved_code[index]
            })

    # 将改进后的代码示例保存到文件中
    with open(improved_name, 'w') as f:
        json.dump({'improved_items':improved}, f,  ensure_ascii=False, indent=4)


def improve_code(file_name):
    """
    根据给定的文件名生成一个新的结果文件名，该文件名基于原始文件名添加'_result'后缀。
    这个函数首先会检查结果文件是否存在，如果不存在，则抛出一个文件找不到的异常。
    如果文件存在，它会读取结果文件的内容，并生成一个改进版本的文件，添加'_improved'后缀。

    参数:
    file_name (str): 原始文件的名称，用于生成结果和改进文件的名称。

    返回:
    str: 改进后文件的名称。
    """
    # 使用给定文件名生成结果文件名
    result_filename = f"{os.path.splitext(file_name)[0]}_result.json"

    # 确保读取的文件是之前生成的
    if not os.path.exists(result_filename):
        raise FileNotFoundError(f"{result_filename} does not exist.")

    # 读取结果文件的内容
    result = read_result(result_filename)

    # 生成改进文件的名称
    improved_name = f"{os.path.splitext(file_name)[0]}_improved.json"

    # 执行改进操作并保存到新的文件中
    improve(result, improved_name)

    # 返回改进文件的名称
    return improved_name



def main():
    file_name = 'test.py'
    print(improve_code(file_name))


if __name__ == '__main__':
    main()

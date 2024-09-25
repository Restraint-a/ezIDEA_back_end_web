from pylint.lint import Run
from pylint.reporters.text import TextReporter
import re, os
import json

def parse_pylint_rate(output):
    """
    解析pylint的代码评分部分（Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)）

    该函数通过正则表达式提取评分数据。

    参数：
    output(str)：pylint文件的输出字符串。

    返回：
    rates(list):包含一个字典（后续可考虑并行处理包含多个字典对象），字典中包含当前分数、上次分数和分数变化情况。
    """
    #正则表达式
    pattern = r"rated at (\d\.\d+)\/10 \(.*(\d+\.\d+)\/.*([+|-]\d+\.\d+)"
    #输出字符串中查找
    match = re.search(pattern, output)
    rates = []
    if match:
        #找出匹配的第1,2,3个结果
        current_score = match.group(1)
        previous_score = match.group(2)
        change = match.group(3)

        # 将评分信息组装成字典并添加到列表中
        rates.append({
            '当前分数': current_score,
            '上次分数': previous_score,
            '变化': change
        })
        return rates
    else:
        #没找到匹配的评分信息则返回None
        return None


def parse_pylint_output(output):
    """
    解析pylint的审查信息部分（uploads\test.py:2:0: C0304: Final newline missing (missing-final-newline)）

    该函数通过正则表达式提取评分数据。

    参数：
    output(str)：pylint文件的输出字符串。

    返回：
    rates(list):包含一个字典（后续可考虑并行处理包含多个字典对象），字典中包含文件名、出错行号、出错列号、错误码和错误信息。
    """
    results = []
    # 正则表达式
    pattern = r'uploads\\(\S+\.py):(\d+):(\d+): (\w+): (.+)\s\('

    # 将pylint的输出按行分割
    lines = output.split('\n')
    # 遍历每一行
    for line in lines:
        # 匹配行
        match = re.match(pattern, line.strip())
        if match:
            filename, line_num, col_num, error_code, message = match.groups()
            results.append({
                '文件名': filename,
                '出错行': int(line_num),
                '出错列': int(col_num),
                '错误码': error_code,
                '错误信息': message
            })

    return results

def process_file_out(filename):
    """
    调用pylint对给定的.py代码进行处理，并生成对应的报告文件。

    报告文件名基于原始文件名，增加扩展名为_report.txt。

    参数:
    - filename: 待处理的文件名
    """
    report_filename = f"{os.path.splitext(filename)[0]}_report.txt"
    with open(report_filename, "w") as f:
        reporter = TextReporter(f)
        Run([filename], reporter=reporter, exit=False)

def process_report(filename):
    """
    将pylint生成的报告进行处理，解析内容并保存结果为json文件。

    参数:
    filename (str): 输入文件的名称。

    返回:
    result_filename(str): 处理后生成的JSON文件的名称。
    """
    report_filename = f"{os.path.splitext(filename)[0]}_report.txt"
    with open(report_filename, 'r', encoding='utf-8') as file:
        output = file.read()

    # 解析输出
    parsed_results = parse_pylint_output(output)
    parsed_rates = parse_pylint_rate(output)

    #去除原扩展名并改为json
    result_filename = f"{os.path.splitext(filename)[0]}_result.json"

    #将解析后的结果和评分情况保存为json文件
    with open(result_filename, 'w', encoding='utf-8') as f:
        json.dump({'错误信息': parsed_results, '评分情况': parsed_rates}, f, ensure_ascii=False, indent=4)

    return result_filename
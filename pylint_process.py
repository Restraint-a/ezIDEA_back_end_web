from pylint.lint import Run
from pylint.reporters.text import TextReporter
import re, os


def parse_pylint_rate(output):
    # pattern = r"rated at (\d\.\d+/10) \(previous run: (\d+\.\d+/10), \+(\d+\.\d+)"
    #pattern = r"rated at (\d\.\d+)\/10 \(.*(\d+\.\d+)\/.*(\d+\.\d+)"
    pattern = r"rated at (\d\.\d+)\/10 \(.*(\d+\.\d+)\/.*([+|-]\d+\.\d+)"
    match = re.search(pattern, output)
    rates = []
    if match:
        #找出匹配的第1,2,3个结果
        current_score = match.group(1)
        previous_score = match.group(2)
        change = match.group(3)
        rates.append({
            '当前分数': current_score,
            '上次分数': previous_score,
            '变化': change
        })
        return rates
    else:
        return None


def parse_pylint_output(output):
    results = []
    pattern = r'uploads\\(\S+\.py):(\d+):(\d+): (\w+): (.+)\s\('

    lines = output.split('\n')
    for line in lines:
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


def process_report(filename):
    report_filename = f"{os.path.splitext(filename)[0]}_report.txt"
    with open(report_filename, 'r', encoding='utf-8') as file:
        output = file.read()

    # 解析输出
    parsed_results = parse_pylint_output(output)
    parsed_rates = parse_pylint_rate(output)
    result_filename = f"{os.path.splitext(filename)[0]}_result.txt"

    with open(result_filename, 'w',encoding='utf-8') as f:
        f.write(f"错误信息:\n")
        for result in parsed_results:
            for key,value in result.items():
                f.write(f'{key}:{value}\n')
        f.write('\n')

        f.write(f"本次评分情况:\n")
        for rate in parsed_rates:
            for key,value in rate.items():
                f.write(f'{key}:{value}\n')


def process_file_out(filename):
    report_filename = f"{os.path.splitext(filename)[0]}_report.txt"
    with open(report_filename, "w") as f:
        reporter = TextReporter(f)
        Run([filename], reporter=reporter, exit=False)

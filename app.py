from flask import Flask, request, send_file, jsonify, render_template
import os
from pylint_process import process_file_out, process_report
from improve_code import read_result,is_want,improve,improve_code

app = Flask(__name__)

# 定义上传文件保存目录
UPLOAD_FOLDER = 'uploads'
# 如果目录不存在，则创建
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    """
    渲染主页面
    """
    return render_template("index.html", title='File Upload Example')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    处理文件上传请求

    """
    # 检查请求中是否有文件部分
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 如果文件存在且文件类型允许
    if file and allowed_file(file.filename):
        # 保存上传的文件
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        process_file_out(filename)

        #result_filename = f"{os.path.splitext(filename)[0]}_result.txt"
        file_json = process_report(filename)
        #print(result_filename)
        # 返回处理后的文件供下载
        #return send_file(result_filename, as_attachment=True,attachment_filename=result_filename)
        return send_file(file_json, as_attachment=True)
    else:
        # 文件类型不允许
        return jsonify({'error': 'File type not allowed'}), 400


def allowed_file(filename):
    """
    检查文件类型是否允许
    """
    # 检查文件名中是否有 '.' 并且文件扩展名是否为 .py
    # 使用rsplit函数，从右向左分割一次（但分割后的列表仍是左向右排序）
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'py'

@app.route('/improve', methods=['POST'])
def improve_code_endpoint():
    """
    处理代码优化请求
    """
    # 获取前端传递的文件名
    data = request.get_json()
    if 'filename' not in data:
        return jsonify({'error': 'Filename not provided'}), 400

    filename = data['filename']
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # 生成改进后的文件
    try:
        improved_filename = improve_code(filepath)
        # 读取改进后的文件内容
        # with open(improved_filename, 'r') as f:
        #     improved_data = json.load(f)
        #
        # return jsonify(improved_data)
        # 使用send_file发送文件
        return send_file(improved_filename, as_attachment=True)
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # 启动Flask应用，调试模式设为True
    app.run(debug=True)

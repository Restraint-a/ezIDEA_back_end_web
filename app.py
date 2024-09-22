from flask import Flask, request, send_file, jsonify, render_template
import os
from pylint_process import process_file_out, process_report

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
    ---
    description: 上传文件并处理，然后返回处理后的文件
    parameters:
      - name: file
        in: formData
        description: The file to upload
        required: true
        type: file
    responses:
      200:
        description: Processed file is returned for download
      400:
        description: Bad request due to missing file, no selected file, or file type not allowed
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

        result_filename = f"{os.path.splitext(filename)[0]}_result.txt"
        process_report(filename)
        #print(result_filename)
        # 返回处理后的文件供下载
        return send_file(result_filename, as_attachment=True,attachment_filename=result_filename)
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


if __name__ == '__main__':
    # 启动Flask应用，调试模式设为True
    app.run(debug=True)

# -*- coding: utf-8 -*-
"""
@FileName: main.py
@Description: Duyu09's小型网盘后端Python代码
@Author: DuYu (@Duyu09)
@CreateTime: Dec. 17th, 2023. v1.0
@LastSaved: Dec. 17th, 2023. v1.0
"""

import os
from flask import Flask, send_file, request, jsonify, render_template

app = Flask(__name__, template_folder='./templates', static_folder='./static', static_url_path="/")
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 * 1024

file_directory = r'./collection'


@app.route('/', methods=['GET'])
def root():
    return send_file("static/index.html")
    # return render_template("index.html")


@app.route('/downloadFile', methods=['GET'])
def download_file():
    filename = request.args.get('fileName')
    file_path = os.path.join(file_directory, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)
    else:
        return jsonify({"status": 1, "description": "File Not Found."})


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        file.save(os.path.join(file_directory, file.filename))
        return jsonify({"status": 0, "description": "上传成功！"})
    except Exception as e:
        return jsonify({"status": 1, "description": str(e)})


@app.route('/fileList', methods=['GET'])
def get_files():
    if not os.path.exists(file_directory):
        return jsonify({"status": 1, 'description': 'Directory not found'})
    files = [file for file in os.listdir(file_directory) if os.path.isfile(os.path.join(file_directory, file))]
    files_return = []
    count = 0
    for item in files:
        files_return.append({"id": count, "file": item})
        count = count + 1
    return jsonify({"status": 0, 'fileList': files_return})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

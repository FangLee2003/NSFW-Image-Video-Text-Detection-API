from flask import Flask, request, jsonify, render_template
import werkzeug
from PIL import Image
import os
import shutil
from helpers.nsfwCheck import nsfw_check, nsfw_check_video
from helpers.offensiveDetection import offensive_detection
from flask import Response
import json

savingFolder = './uploaded'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/preds', methods=['POST', 'GET'])
def uploaded_form():
    # Xử lý request từ client, sau đó chạy mô hình để phát hiện nội dung NSFW.
    all_results = []

    # Lặp qua tất cả các input dạng text của người dùng
    for field, user_input in request.form.items():
        offensive_words = offensive_detection(user_input)

        if offensive_words:
            all_results.append({
                "field": field,  # Tên input bị phát hiện
                "offensive_words": offensive_words  # Danh sách từ tiêu cực
            })
    print(offensive_words)
    for field, files in request.files.lists():
        for file in files:
            filename = werkzeug.utils.secure_filename(file.filename)
            file_path = os.path.join(savingFolder, filename)
            file.save(file_path)

            print(f'Received file from field "{field}": {filename}')

            # Xác định loại file để chạy mô hình phù hợp
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                predictions = nsfw_check(file_path)  # Kiểm tra hình ảnh
            elif filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                predictions = nsfw_check_video(
                    file_path, frame_skip=30)  # 30 frames mới check 1 lần
            else:
                predictions = {"error": f"Unsupported file format: {filename}"}

            all_results.append({
                "field": field,  # Tên input chứa file
                "filename": filename,
                "predictions": predictions
            })

    print("___Deleting files____")
    delete_imgs()  # Xóa file sau khi xử lý

    return Response(
        json.dumps({"data": all_results}, ensure_ascii=False),
        mimetype="application/json; charset=utf-8"
    )


def delete_imgs():
    for imgname in os.listdir(savingFolder):
        img_path = os.path.join(savingFolder, imgname)
        os.remove(img_path)


if __name__ == '__main__':
    app.run(debug=True)

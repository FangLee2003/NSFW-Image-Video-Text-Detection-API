import datetime
import cv2
import os
from helpers.nudityDetection import nude_detection
from helpers.violenceDetection import violence_detection


def nsfw_check(img_path):
    """
    Kiểm tra mức độ NSFW của hình ảnh và xác định có chứa nội dung không phù hợp hay không.

    PARAMS::
    - img_path: Đường dẫn đến ảnh cần kiểm tra.

    RETURNS::
    - predicts: Dictionary chứa điểm số NSFW (nude, violence, natural).
    - isContainNude: Boolean - True nếu ảnh chứa nội dung khỏa thân (nude).
    - isContainViolence: Boolean - True nếu ảnh có nội dung bạo lực (violence).
    """
    # Lấy kết quả từ các mô hình detection
    nude_score = nude_detection(img_path)
    violence_score = violence_detection(img_path)
    # Giả sử trả về mảng [[drugs, violence, natural]]
    # nsfw_preds = violence_detection(img_path)

    predicts = {
        'nude_score': int(nude_score[img_path]['unsafe'] * 100),
        'violence_score': int(violence_score * 100)
        # 'violence_score': int(nsfw_preds[0][1] * 100),
        # 'natural_score': int(nsfw_preds[0][2] * 100)
    }

    return {
        "path": img_path,
        "isContainNude": predicts['nude_score'] > 85,
        "isContainViolence": predicts['violence_score'] > 60, # and predicts['natural_score'] < 25,
        "predicts": predicts,
    }


def nsfw_check_video(video_path, frame_skip=30):
    """
    PARAMS::
    - video_path: Đường dẫn tới video cần kiểm tra.
    - frame_skip: Số frame bỏ qua để giảm tải tính toán (mặc định mỗi 30 frames mới kiểm tra 1 frame).

    Returns::
    - result: Danh sách thời gian (giây) phát hiện nội dung NSFW hoặc "Video này an toàn".
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Không thể mở video."

    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Số khung hình mỗi giây
    nsfw_times = {}  # Danh sách lưu thời gian phát hiện NSFW

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Chỉ xử lý mỗi 'frame_skip' frame để tiết kiệm thời gian
        if frame_count % frame_skip == 0:
            temp_path = "temp_frame.jpg"
            cv2.imwrite(temp_path, frame)  # Lưu frame tạm thời
            nsfw_result = nsfw_check(temp_path)  # Gọi hàm phát hiện NSFW

            if nsfw_result["isContainNude"] or nsfw_result["isContainViolence"]:
                formatted_time = str(datetime.timedelta(seconds=frame_count/fps))
                nsfw_times[formatted_time] = "Nude" if nsfw_result["isContainNude"] else "Violence"

        frame_count += 1

    cap.release()
    # os.remove(temp_path)  # Xóa frame tạm sau khi xử lý

    if nsfw_times:
        return {
            "path": video_path,
            "type": "This video contains NSFW content",
            "timestamps": nsfw_times
        }
    return {
        "path": video_path,
        "type": "This video is safe!",
    }

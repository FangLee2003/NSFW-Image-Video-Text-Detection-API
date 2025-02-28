import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
""" os.path.dirname(__file__) lấy thư mục chứa file hiện tại -> ".." tới thư mục cha
-> os.path.abspath -> chuyển đường dẫn tương đối thành tuyệt đối
"""
OFFENSIVE_WORDS_PATH = os.path.join(BASE_DIR, "training", "vn_offensive_words.txt")

def load_data(data_path):
    if not os.path.exists(data_path):
        print(f"Error: {data_path} does not exist!")
        return set()

    words = []

    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("#"):
                words.append(line.strip().lower())

    return set(words)


def offensive_detection(text):
    offensive_words = load_data(OFFENSIVE_WORDS_PATH)

    words = text.lower().split()

    detected_words = [word for word in words if word in offensive_words]

    return detected_words

# NSFW & Offensive Content Detection API

## 📌 Overview

This project provides an API for detecting NSFW content in images and videos, as well as identifying offensive words in text inputs. The API processes multiple input fields from users, checking for inappropriate content and returning a detailed response.

## 🚀 Features

- **Detect offensive words** in text inputs using a predefined list of negative words.
- **Analyze images** to determine NSFW content using NudeNet and ViT Base Violence Detection.
- **Analyze videos** by extracting frames and checking for NSFW content.
- **Support multiple file uploads:** PNG, JPG, JPEG, MP4, AVI, MOV, MKV.
- **REST API interface** for easy integration.
- **Secure file handling**, processing, and automatic deletion after analysis.

## 🛠 Installation

### 1️⃣ Create a virtual environment & install dependencies

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Model Download

```sh
huggingface-cli download facebook/vit-violence-detection --local-dir models/vit-violence
```

### 3️⃣ Run the API

```sh
python app.py
```

## 📡 API Usage

### Endpoint: `/preds`

**Method:** `POST`

### 🔹 Request Format

**Form Fields:**

- `text_field_1`: Any text input to check for offensive words.
- `text_field_2`: Additional text inputs are also processed.
- `files`: Images or videos to analyze for NSFW content.

**Example Request (Using cURL):**

```sh
curl -X POST "http://127.0.0.1:5000/preds" \
  -F "name=hello" \
  -F "comment=Buổi sáng thật cặc" \
  -F "files=@image.jpg" \
  -F "files=@video.mp4"
```

### 🔹 Response Format

```json
{
  "data": [
    {
      "field": "comment",
      "offensive_words": ["cặc"]
    },
    {
      "field": "files",
      "filename": "image.jpg",
      "predictions": { "nsfw_score": 0.9 }
    }
  ]
}
```

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

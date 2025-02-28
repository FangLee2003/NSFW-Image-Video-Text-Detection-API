import datetime
import cv2
from helpers.preprocessImgs import prepare_img
from tensorflow import keras
import tensorflow as tf
import os
import torch
import numpy as np
from transformers import ViTForImageClassification, ViTFeatureExtractor
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
model_path = "./models/vit-violence"
labels = ["Non-Violence", "Violence"]

print("--------Loading the model---------")
# model = keras.models.load_model('./models')
model = ViTForImageClassification.from_pretrained(model_path)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_path)

# def violence_detection(img_path):
#     """
#     PARAMS::
#     - img_path a path for the image that I'm gonna to work on
#     Returns::
#     - return a numpy array with 3 values representing our 3 classes
#     0 for drugs, 1 for violence, 2 for natural
#     """

#     img = prepare_img(img_path)
#     preds = model.predict(img)
#     # print(f"{preds} \n {preds.shape} here is our predictions")
    
#     return preds

def violence_detection(img_path):
    # Load an image
    img = Image.open(img_path).convert('RGB')

    # Preprocess the image
    inputs = feature_extractor(images=np.array(img), return_tensors="pt")

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        predicted_class = labels[predicted_class_idx]

        probs = torch.nn.functional.softmax(logits, dim=-1)
        violence_score = probs[0][1].item()

    # Print the predicted class
    # print("Predicted class:", model.config.id2label[predicted_class_idx])
    
    return violence_score
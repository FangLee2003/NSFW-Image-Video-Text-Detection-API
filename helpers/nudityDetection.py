import os
from models.nudenet import NudeClassifier

print('----------Initializing the NudeClassifier----------')
clf = NudeClassifier()

def nude_detection(img_path):
    nudity_score = clf.classify(img_path)

    return nudity_score

# https://www.youtube.com/watch?v=4Zy4IUv_TWs
def nude_detection_video(vid_path):
    nudity_score = clf.classify_video(vid_path)

    return nudity_score
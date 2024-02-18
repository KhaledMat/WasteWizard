import cv2
import torch
from ultralytics import YOLO

# import ultralytics.yolo.v8.detect.predict

# Load the pretrained weights
weights_path = "./runs/detect/train/weights/last.pt"  # Replace with the path to your YOLOv8 weights file
model = YOLO(weights_path)

model.predict(source="0", show=True, conf=0.5)

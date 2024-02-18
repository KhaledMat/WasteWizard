from ultralytics import YOLO

# Path to the weights file
weights_path = "./runs/detect/train/weights/last.pt"

model = YOLO(weights_path)

model.predict(source="0", show=True, conf=0.5)

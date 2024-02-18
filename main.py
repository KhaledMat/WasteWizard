from ultralytics import YOLO

# Load the pretrained weights
weights_path = "./runs/detect/train/weights/best.pt"  # Replace with your weights path
model = YOLO(weights_path)

# Perform inference and store the results in a variable
results = model("./img.jpg")  # List of Results objects

# print(results)

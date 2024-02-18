from ultralytics import YOLO
import cv2

# Load the pretrained weights
weights_path = "./runs/detect/train/weights/best.pt"  # Replace with your weights path
model = YOLO(weights_path)

# Create VideoCapture object
cap = cv2.VideoCapture(0)  # 0 represents the first USB camera, 1 for the second, etc.

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture a single frame
    ret, frame = cap.read()

    # Check if frame captured successfully
    if ret:
        # Convert frame from BGR to RGB (YOLO uses RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform inference and store the results in a variable
        # Note: You may need to adjust the code depending on the exact YOLO model interface
        results = model.predict(source=frame_rgb)
        category = results[0].boxes.cls
        print(category)

        # Print results
        # The way to access results may vary; adjust according to your model's documentation
        print(results)

    else:
        print("Error: Failed to capture frame.")

    # Release the VideoCapture object
    cap.release()

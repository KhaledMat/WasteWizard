import cv2
import RPi.GPIO as GPIO

IR_PIN = 23
GPIO.setmode(GPIO.BCM)

GPIO.setup(IR_PIN, GPIO.IN)

# Create VideoCapture object
cap = cv2.VideoCapture(0)  # 0 represents the first USB camera, 1 for the second, and so on

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    while True:
        sensor_state = GPIO.input(IR_PIN)
        if sensor_state == GPIO.HIGH:

    # Capture a single frame
            ret, frame = cap.read()

    # Check if frame captured successfully
            if ret:
        # Save the captured frame as an image file
                cv2.imwrite('captured_image.jpg', frame)
                print("Image captured successfully.")
            else:
                print("Error: Failed to capture frame.")

            # Release the VideoCapture object
            cap.release()
            break

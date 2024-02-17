import picamera
import time

# Function to capture an image
def capture_image():
    with picamera.PiCamera() as camera:
        # Set resolution
        camera.resolution = (640, 480)  # Adjust resolution as needed
        # Start preview for a brief moment to initialize camera settings
        camera.start_preview()
        time.sleep(2)  # Wait for camera to initialize
        # Capture image
        camera.capture('test_image.jpg')  # Adjust file name as needed

if __name__ == "__main__":
    # Capture an image
    capture_image()
    print("Image captured successfully.")

import socket
from ultralytics import YOLO
import cv2
import numpy as np

# Load the pretrained YOLO model
weights_path = "./runs/detect/train/weights/best.pt"  # Update with your weights path
model = YOLO(weights_path)

# Setup server
host = "192.168.137.108"  # Listen on all network interfaces
port = 9990  # Arbitrary non-privileged port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print(f"Listening on {host}:{port}")


def process_image(image_bytes):
    # Convert bytes data to a numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Convert image to RGB (from BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Process the image with YOLO
    results = model(img_rgb)
    # Return results
    return results


try:
    while True:
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address}")

            # Receive the data in small chunks
            image_data = bytearray()
            while True:
                data = connection.recv(4096)
                if not data:
                    break
                image_data.extend(data)

            if image_data:
                # Process the image
                results = process_image(image_data)
                # Simplify the response (e.g., send back the number of detected objects)
                response = f"Detected objects: {len(results.pred[0])}"
                connection.sendall(response.encode("utf-8"))
            else:
                print("No data received.")

        finally:
            # Clean up the connection
            connection.close()

except KeyboardInterrupt:
    print("Server is shutting down.")
finally:
    server_socket.close()

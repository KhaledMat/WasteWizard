import cv2
import RPi.GPIO as GPIO
import time
import socket
import os

# Define GPIO pins
IN1 = 22
IN2 = 27
IN3 = 17
IN4 = 4
INPUT1_PIN = 26
INPUT2_PIN = 19
INPUT3_PIN = 13
INPUT4_PIN = 6
LOCK_PIN = 5
IR_PIN = 23
PWM_FREQUENCY = 1000  # 1 kHz

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(
    [INPUT1_PIN, INPUT2_PIN, INPUT3_PIN, INPUT4_PIN, LOCK_PIN],
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP,
)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
GPIO.setup(IR_PIN, GPIO.IN)

# Initialize PWM objects for In1 to In4
pwm_in1 = GPIO.PWM(IN1, PWM_FREQUENCY)
pwm_in2 = GPIO.PWM(IN2, PWM_FREQUENCY)
pwm_in3 = GPIO.PWM(IN3, PWM_FREQUENCY)
pwm_in4 = GPIO.PWM(IN4, PWM_FREQUENCY)


# Function to turn the motor clockwise
def clockwise(num):
    if num == 0:
        pwm_in1.start(70)
        pwm_in2.start(0)
    elif num == 1:
        pwm_in3.start(70)
        pwm_in4.start(0)


# Function to turn the motor counter-clockwise
def counterclockwise(num):
    if num == 0:
        pwm_in1.start(0)
        pwm_in2.start(70)
    elif num == 1:
        pwm_in3.start(0)
        pwm_in4.start(70)


# Stop the motor
def stop(num):
    if num == 0:
        pwm_in1.start(0)
        pwm_in2.start(0)
    elif num == 1:
        pwm_in3.start(0)
        pwm_in4.start(0)


def brake(num):
    if num == 0:
        pwm_in1.start(100)
        pwm_in2.start(100)
    elif num == 1:
        pwm_in3.start(100)
        pwm_in4.start(100)


def moveToContainer(container):
    if container == 0:
        GPIO.add_event_detect(INPUT1_PIN, GPIO.FALLING)
        while True:
            counterclockwise(0)
            if GPIO.event_detected(INPUT1_PIN):
                brake(0)
                break
    elif container == 1:
        GPIO.add_event_detect(INPUT2_PIN, GPIO.FALLING)
        while True:
            counterclockwise(0)
            if GPIO.event_detected(INPUT2_PIN):
                brake(0)
                break
    elif container == 2:
        GPIO.add_event_detect(INPUT3_PIN, GPIO.FALLING)
        while True:
            counterclockwise(0)
            if GPIO.event_detected(INPUT3_PIN):
                brake(0)
                break
    elif container == 3:
        GPIO.add_event_detect(INPUT4_PIN, GPIO.FALLING)
        while True:
            counterclockwise(0)
            if GPIO.event_detected(INPUT4_PIN):
                brake(0)
                break


def unlock():
    clockwise(1)
    time.sleep(5)
    stop(1)


def lock():
    GPIO.add_event_detect(LOCK_PIN, GPIO.RISING)
    while True:
        counterclockwise(1)
        if GPIO.event_detected(LOCK_PIN):
            brake(1)
            break


def send_file_over_socket(file_path, host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))

        # Open the file in binary mode and send it
        with open(file_path, "rb") as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)

        # Optionally, receive a response from the server
        response = client_socket.recv(1024).decode("utf-8")
        print(f"Response from server: {response}")

        return response
    finally:
        client_socket.close()
        print("Connection closed.")


def detectTrash():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ret, frame = cap.read()

    if ret:
        filename = "captured_trash.jpg"
        cv2.imwrite(filename, frame)
        print(f"Frame saved as {filename}.")

        host = "192.168.137.91"
        port = 9990
        response = send_file_over_socket(filename, host, port)

        trashType = int(response) if response.isdigit() else 1
        moveToContainer(trashType)
        unlock()
        time.sleep(10)
        lock()
    else:
        print("Error: Failed to capture frame.")

    cap.release()


# Main loop
try:
    while True:
        sensor_state = GPIO.input(IR_PIN)
        if sensor_state == GPIO.HIGH:
            detectTrash()
            print("Trash Detected.")

        # Monitoring input pins for changes can be added here if needed
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    GPIO.cleanup()

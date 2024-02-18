import RPi.GPIO as GPIO
import time
import cv2

# Define GPIO pins
IN1 = 26
IN2 = 19
IN3 = 13
IN4 = 6


INPUT1_PIN = 22
INPUT2_PIN = 27
INPUT3_PIN = 17
INPUT4_PIN = 4

LOCK_PIN = 5

IR_PIN = 23

PWM_FREQUENCY = 1000  # 1 kH


# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(INPUT2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(INPUT3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(INPUT4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set GPIO pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.setup(IR_PIN, GPIO.IN)

# Initialize PWM objects for In1 to In4
pwm_in1 = GPIO.PWM(IN1, PWM_FREQUENCY)
pwm_in2 = GPIO.PWM(IN2, PWM_FREQUENCY)
pwm_in3 = GPIO.PWM(IN3, PWM_FREQUENCY)
pwm_in4 = GPIO.PWM(IN4, PWM_FREQUENCY)

cap = cv2.VideoCapture(1)  # 0 represents the first USB camera, 1 for the second, and so on

# Function to turn the motor clockwise
def clockwise(num):
    if num == 0:
        pwm_in1.start(100)
        pwm_in2.start(0)
    elif num == 1:
        pwm_in3.start(100)
        pwm_in4.start(0)


# Function to turn the motor counter-clockwise
def counterclockwise(num):
    if num == 0:
        pwm_in1.start(0)
        pwm_in2.start(100)
    elif num == 1:
        pwm_in3.start(0)
        pwm_in4.start(100)


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
        print(0)
        GPIO.add_event_detect(INPUT1_PIN, GPIO.FALLING)
        while True:
            counterclockwise(0)
            if GPIO.event_detected(INPUT1_PIN):
                brake(0)
                break
    elif container == 1:
        print(1)
        GPIO.add_event_detect(INPUT2_PIN, GPIO.FALLING)
        while True:
            counterclockwise(0)
            if GPIO.event_detected(INPUT2_PIN):
                brake(0)
                break
    elif container == 2:
        print(2)
        GPIO.add_event_detect(INPUT3_PIN, GPIO.FALLING)
        while True:
            counterclockwise(0)
            if GPIO.event_detected(INPUT3_PIN):
                brake(0)
                break
    elif container == 3:
        print(3)
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


def detectTrash():
    # open cv capture video
    if not cap.isOpened():
        print("Error: Could not open camera.")
    else:
        while True:
            sensor_state = GPIO.input(IR_PIN)
            ret, frame = cap.read()
            if ret:
            # Save the captured frame as an image file
                cv2.imwrite('captured_image.jpg', frame)
                print("Image captured successfully.")
            else:
                print("Error: Failed to capture frame.")

            # Release the VideoCapture object
            cap.release()
            break

    # send file over web socket

    # get answer

    # find out the type of garbage
    trashType = 3
    moveToContainer(trashType)
    unlock()
    time.sleep(10)
    lock()


try:
    while True:
        sensor_state = GPIO.input(IR_PIN)
        print(sensor_state)
        if sensor_state == GPIO.HIGH:
            time.sleep(1)
            sensor_state = GPIO.input(IR_PIN)
            print(sensor_state)
            if sensor_state == GPIO.HIGH:
                time.sleep(1)
                sensor_state = GPIO.input(IR_PIN)
                print(sensor_state)
                if sensor_state == GPIO.HIGH:
                    time.sleep(1)
                    sensor_state = GPIO.input(IR_PIN)
                    print(sensor_state)
                    if sensor_state == GPIO.HIGH:
                        time.sleep(1)
                        sensor_state = GPIO.input(IR_PIN)
                        print(sensor_state)
                        if sensor_state == GPIO.HIGH:
                            print("Trash Detected.")
                            detectTrash()
                     



except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Cleanup GPIO pins
    GPIO.cleanup()

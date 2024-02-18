import RPi.GPIO as GPIO
import time

# Define GPIO pins
IN1 = 22
IN2 = 27
IN3 = 17
IN4 = 4

INPUT_PIN = 26

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set GPIO pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Function to turn the motor clockwise
def clockwise():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(2)

# Function to turn the motor counter-clockwise
def counterclockwise():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(2)

# Stop the motor
def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Test the motor
try:
    while True:
        # Check input state
        input_state = GPIO.input(INPUT_PIN)

        # If input is high, call clockwise() function
        if input_state == GPIO.HIGH:
            clockwise()
            print("Clockwise rotation")
        # If input is low, stop the motor and break the loop
        else:
            stop()
            print("Input is low. Stopping motor.")
            break

        # Wait a short duration before checking the input state again
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Cleanup GPIO pins
    GPIO.cleanup()
    
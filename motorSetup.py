import RPi.GPIO as GPIO
import time

# Define GPIO pins
IN1 = 22
IN2 = 27
IN3 = 17
IN4 = 4

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

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
    # Test clockwise rotation
    print("Clockwise rotation")
    clockwise()

    # Test counter-clockwise rotation
    print("Counter-clockwise rotation")
    counterclockwise()

    # Stop the motor
    print("Stopping motor")
    stop()

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Cleanup GPIO pins
    GPIO.cleanup()

import pigpio
import time

# Initialize pigpio
pi = pigpio.pi('piserver.local')

if not pi.connected:
    exit()

servo_pin = 19  # Using GPIO pin 19

# Example to set the servo to different positions
def set_servo_pulsewidth(pulsewidth):
    # Sets the hardware PWM. 0 stops PWM.
    pi.set_servo_pulsewidth(servo_pin, pulsewidth)

try:
    # Sweep the servo across its range
    while True:
        # Set to minimum position (adjust pulsewidth as needed)
        set_servo_pulsewidth(500)  # 0.5 ms
        time.sleep(1)
        # Set to middle position
        set_servo_pulsewidth(1500)  # 1.5 ms
        time.sleep(1)
        # Set to maximum position
        set_servo_pulsewidth(2500)  # 2.5 ms
        time.sleep(1)
except KeyboardInterrupt:
    # Clean up
    set_servo_pulsewidth(0)  # Stop PWM
    pi.stop()


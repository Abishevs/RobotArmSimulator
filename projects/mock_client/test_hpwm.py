from rpi_hardware_pwm import HardwarePWM
import time


# Constants for PWM
PWM_FREQUENCY = 50  # Frequency in Hz, 50 Hz for servo control
PERIOD = 1.0 / PWM_FREQUENCY  # Period in seconds (20 ms for 50 Hz)

# Servo pulse widths in seconds
MIN_PULSE_S = 0.5 / 1000  # Minimum pulse width (0.5 ms)
MAX_PULSE_S = 2.5 / 1000  # Maximum pulse width (2.5 ms)

def pulse_width_to_duty_cycle(pulse_width_s):
    """Convert pulse width in seconds to duty cycle percentage."""
    return (pulse_width_s / PERIOD) * 100


# Function to initialize the PWM device
def initialize_pwm(pwm_channel, frequency_hz):
    pwm = HardwarePWM(pwm_channel=3, hz=50, chip=2)
    pwm.start(0)  # Start with 0% duty cycle
    return pwm

# Function to set servo angle
# def set_servo_angle(pwm, angle):
#     if angle < 0 or angle > 180:
#         print("Angle out of range")
#         return
#
#     # Convert angle to duty cycle
#     # Note: These values might need fine-tuning for your specific servo
#     duty_cycle = angle / 18 + 2.5  # This converts angle (0-180) to duty cycle percentage (2.5-12.5 for 0-180 degrees)
#
#     pwm.change_duty_cycle(duty_cycle)

def set_servo_angle(pwm, angle):
    """Set servo to a specific angle using rpi_hardware_pwm."""
    if not 0 <= angle <= 180:
        print("Angle out of range")
        return

    # Map angle to pulse width
    pulse_s = MIN_PULSE_S + (angle / 180.0) * (MAX_PULSE_S - MIN_PULSE_S)
    duty_cycle = pulse_width_to_duty_cycle(pulse_s)
    
    pwm.change_duty_cycle(duty_cycle)
# Main code
if __name__ == "__main__":
    PWM_CHANNEL = 3  # Adjust your PWM channel here
    PWM_FREQUENCY = 50  # 50 Hz for servo

    # Initialize the PWM device
    pwm_device = initialize_pwm(PWM_CHANNEL, PWM_FREQUENCY)

    try:
        while True:
            angle = int(input("Enter angle (0 to 180): "))
            set_servo_angle(pwm_device, angle)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pwm_device.stop()

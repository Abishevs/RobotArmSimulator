import gpiozero
from time import sleep

MIN_PULSE = 0.5 / 1000
MAX_PULSE = 2.5 / 1000

def set_servo_angle(angle):
    if angle < 0 or angle > 180:
        print("Angle out of range")
        return 
        # Calculate the target pulse width for the given angle
    print(angle)
    target_pulse = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)

    # Convert the pulse width to a value between -1 and 1
    value = (target_pulse - MIN_PULSE) / (MAX_PULSE - MIN_PULSE) * 2 - 1

    # Set the servo to the calculated value
    servo.value = value
    sleep(1)  # Wait for the servo to move

servo = gpiozero.Servo(19, min_pulse_width=MIN_PULSE, max_pulse_width=MAX_PULSE) # , min_pulse_width=0.0005, max_pulse_width=0.0025)

while True:
    try:
        angle = int(input(">> "))
    except Exception as e:
        print(e)
        continue
    else:
        set_servo_angle(angle)
    # servo.mid()
    # servo.min()
    # sleep(1)
    # servo.mid()
    # sleep(1)
    # servo.max()
    # sleep(1)

import serial
import time

# Open serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Match the baud rate with the Arduino sketch

try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').rstrip()  # Read a line and strip trailing newline
            print(line)
        
        # value = input(">> ")  # Get input from the user
        
        # Check if the input is not empty and is a digit
        # if value.isdigit():
        #     ser.write(f"{value}\n".encode())  # Convert string to bytes and send
        # else:
        #     print("Please enter a valid number.")
            
        time.sleep(0.1)  # Small delay to prevent spamming
        
except KeyboardInterrupt:
    print("Program terminated!")
finally:
    ser.close()  # Ensure the serial connection is closed on exit


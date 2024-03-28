#include <Servo.h>

static const int servoPin1 = 17;
static const int servoPin2 = 19;
Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(115200); // Start the serial communication
  servo1.attach(servoPin1); // Attach the servo on pin 19 to the servo object
  servo2.attach(servoPin2);
  Serial.println("Enter servo position (0 to 180):");
}

void loop() {
	String inputString = ""; // String to store incoming data
	if (Serial.available()) {
		inputString = Serial.readStringUntil('\n'); // Read the incoming data until newline
		Serial.println(inputString.toInt());  // Echo back the received string
		int posDegrees = inputString.toInt();
		if (posDegrees >= 0 && posDegrees <= 180) {
			int pulseWidth = map(posDegrees, 0, 180, 500, 2500); // Map angle to pulse width
			servo1.writeMicroseconds(pulseWidth); // Set servo position more accurately
			servo2.writeMicroseconds(pulseWidth); // Set servo position more accurately
			// servo1.write(posDegrees); // Set the servo position
			Serial.print("Moving servo to ");
			Serial.println(posDegrees);
		} else {
			Serial.println("Position out of range. Please enter a value between 0 and 180.");
		}
		inputString = "";
	}
}
	// servo1.write(0);
	// delay(500);
	// servo1.write(90);
	// delay(500);
	// servo1.write(180);
	// delay(500);

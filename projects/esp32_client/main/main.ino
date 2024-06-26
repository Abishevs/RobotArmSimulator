#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include <ESPmDNS.h>
#include <ArduinoJson.h>
#include <Servo.h>

#include "config.h" 

static const int servoPin1 = 15;
static const int servoPin2 = 17;
static const int servoPin3 = 19;

Servo servo1;
Servo servo2;
Servo servo3;

const char* websocket_server = "ws://192.168.1.65:8000"; 

using namespace websockets;
WebsocketsClient client;

void setAngle(int servoId,int angle) {
	if (angle < 0 || angle > 180) {
		Serial.println("Angle out of range. Please enter a value between 0 and 180.");
		return;
	}
	int pulseWidth = map(angle, 0, 180, 500, 2500); // Map angle to pulse width

	switch (servoId) {
		case 1:
			servo1.writeMicroseconds(pulseWidth); 
			Serial.print("Moving servo1 to ");
			Serial.println(angle);
			break;
		case 2:
			servo2.writeMicroseconds(pulseWidth); 
			Serial.print("Moving servo2 to ");
			Serial.println(angle);
			break;
		case 3:
			servo3.writeMicroseconds(pulseWidth); 
			Serial.print("Moving servo3 to ");
			Serial.println(angle);
			break;
	}
}

void sendInitialPositions() {
	JsonDocument doc;

	doc["messageType"] = "positionUpdate";
	doc["identifier"] = "managed";

	JsonArray payload_positions = doc["payload"]["positions"].to<JsonArray>();

	JsonObject payload_positions_0 = payload_positions.add<JsonObject>();
	payload_positions_0["jointId"] = 1;
	payload_positions_0["currentAngle"] = 90;
	setAngle(1, 90);

	JsonObject payload_positions_1 = payload_positions.add<JsonObject>();
	payload_positions_1["jointId"] = 2;
	payload_positions_1["currentAngle"] = 90;
	setAngle(2, 90);

	JsonObject payload_positions_2 = payload_positions.add<JsonObject>();
	payload_positions_2["jointId"] = 3;
	payload_positions_2["currentAngle"] = 90;
	setAngle(3, 90);

	String output;

	doc.shrinkToFit();  // optional

	serializeJson(doc, output);
	client.send(output);
}

void onMessageCallback(WebsocketsMessage message) {
    Serial.print("Got Message: ");
    Serial.println(message.data());

    DynamicJsonDocument doc(1024); // Adjust the size based on the expected message size

    DeserializationError error = deserializeJson(doc, message.data()); // Use message.data() here

    if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.c_str());
        return;
    }

    // Check if the messageType is 'updatePosition'
    String messageType = doc["messageType"]; // Use String for comparison
    if (messageType == "positionUpdate") {
        // Process each position in the payload
        JsonArray positions = doc["payload"]["positions"].as<JsonArray>();
        for (JsonObject position : positions) {
            int jointId = position["jointId"]; // 1, 2, 3
            int currentAngle = position["currentAngle"]; // 45, 90, 135
            setAngle(jointId, currentAngle);
        }
    }
}

void setup() {
	Serial.begin(115200);

	// SEtup servos
	servo1.attach(servoPin1); 
	servo2.attach(servoPin2);
	servo3.attach(servoPin3);

	// Connect to WiFi
	WiFi.begin(ssid, password);
	while(WiFi.status() != WL_CONNECTED) {
		delay(1000);
		Serial.println("Connecting to WiFi...");
	}

	// Initialize mDNS
	if (!MDNS.begin("esp32")) {
		Serial.println("Error setting up MDNS responder!");
		while (1) {
			delay(1000);
		}
	}

	// Connect to WebSocket server
	client.onMessage(onMessageCallback);
	if (client.connect(websocket_server)) {
		Serial.println("Connected to the WebSocket server.");

		// Construct an initial JSON message
		sendInitialPositions();

	} else {
		Serial.println("Connection to WebSocket server failed.");
	}
}

// void getJson() {
// 	// generated by https://arduinojson.org/v7/assistant
// 	// String input;
// 	JsonDocument doc;
//
// 	DeserializationError error = deserializeJson(doc, input);
//
// 	if (error) {
// 		Serial.print("deserializeJson() failed: ");
// 		Serial.println(error.c_str());
// 		return;
// 	}
//
// 	const char* messageType = doc["messageType"]; // "positionUpdate"
// 	const char* identifier = doc["identifier"]; // "12345"
// 	const char* source = doc["source"]; // "GUI"
// 	const char* target = doc["target"]; // "ESP32"
//
// 	for (JsonObject payload_position : doc["payload"]["positions"].as<JsonArray>()) {
//
// 		int payload_position_jointId = payload_position["jointId"]; // 1, 2, 3
// 		int payload_position_currentAngle = payload_position["currentAngle"]; // 45, 90, 135
//
// 	}
//
// }


void loop() {
  client.poll();

}


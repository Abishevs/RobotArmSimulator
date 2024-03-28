# Makefile for Arduino sketches
# Update these variables according to your project

SKETCH := json_test/json_test.ino
PORT := /dev/ttyUSB0
FQBN := esp32:esp32:esp32

# Default target
all: upload

# Compile the sketch
build:
	arduino-cli compile --fqbn $(FQBN) $(SKETCH)

# Upload the sketch to the board
upload: build
	arduino-cli upload -p $(PORT) --fqbn $(FQBN) $(SKETCH)


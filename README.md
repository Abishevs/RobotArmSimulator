# Robotic Arm Simulation and Control Platform

## Description
A desktop GUI application is designed to control a real robotic arm.
The GUI communicates with a server, which maintains the "true state" of the arm
segment positions. When the first GUI client connects to the server, it
automatically becomes the "Controller," thereby gaining the ability to control
the robotic arm. Subsequent GUI clients can connect but are assigned a "Viewer"
role, allowing them to observe the current position of the arm.

The project is organized into various project directories, along with a
libs/commonlib folder where the JSON schema and logging are defined. Within the
projects folder, there are three seperate projects: robo_arm_sim (PySide6
GUI), server (via WebSocket), and esp32_client (written in Arduino).

## Table of Contents
- Installation
- Usage
- Project Directory Structure
- Future Plans
- Contributing
- License
- Acknowledgements
- Contact

## Installation
### Prerequestites
- Python 3.x
- Arduino framework / manual upload to ESP32

### Steps
1. Clone the repository
    ```bash
    git clone https://github.com/Abishevs/RobotArmSimulator.git 
    ```
2. Navigate to the project directory
    ```bash
    cd RobotArmSimulator 
    ```
3. Activate install/ start scripts
    ```bash
    source scripts/setup.sh
    ```

4. Install apps (same name as the dir of the project)
    ```bash
    install-app robo_arm_sim
    install-app server
    ```

5. ESP32 setup 
Update sample-config.h with your WIFI settings.
Compile Arduino file and upload to ESP32.

## Usage
### Starting apps
    ```bash
    start-app robo_arm_sim &
    start-app server
    ```


## Future plans include
- Devolopment of real robotic arm is ongoing to test it fully.
- version 2.0 of the software (GUI) is under devolement because
 software lacks feedback loop and restrictions of movement.

<iframe  width="560" height="315" src="https://www.youtube.com/embed/qluetKPBPwk?si=8fZOAtvAbCLjRqGj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Project directory structure
```bash
.
├── dev-requirements.txt
├── libs
│   └── commonlib
│       ├── pyproject.toml
│       └── src
│           ├── commonlib
│           │   ├── enums.py
│           │   ├── errors.py
│           │   ├── __init__.py
│           │   ├── json_schema.py
│           │   └── logger.py
│           └── json_schemas
│               ├── command.json
│               ├── error.json
│               ├── general.json
│               └── positionUpdate.json
├── projects
│   ├── esp32_client
│   │   ├── build.txt
│   │   ├── connect_serial.py
│   │   ├── main
│   │   │   ├── main.ino
│   │   │   └── sample-config.h
│   │   ├── Makefile
│   │   └── servo
│   │       └── servo.ino
│   ├── mock_client
│   │   ├── main.py
│   │   ├── pwm_test.py
│   │   ├── pyproject.toml
│   │   ├── requirements.txt
│   │   ├── src
│   │   │   └── mock_client
│   │   │       ├── client.py
│   │   │       └── __init__.py
│   │   └── test_hpwm.py
│   ├── robo_arm_sim
│   │   ├── main.py
│   │   ├── pyproject.toml
│   │   ├── requirements.txt
│   │   ├── src
│   │   │   └── robo_arm_sim
│   │   │       ├── constants.py
│   │   │       ├── controllers.py
│   │   │       ├── entities.py
│   │   │       ├── __init__.py
│   │   │       ├── robotic_arm.py
│   │   │       ├── ui
│   │   │       │   ├── __init__.py
│   │   │       │   ├── ui_angle_controll_widget.py
│   │   │       │   └── ui_mainwindow.py
│   │   │       ├── utils.py
│   │   │       └── views.py
│   │   └── ui_files
│   │       ├── controll_widget.ui
│   │       └── ui_main_window.ui
│   └── server
│       ├── main.py
│       ├── pyproject.toml
│       ├── requirements.txt
│       ├── sample-env
│       └── src
│           └── ws_server
│               ├── __init__.py
│               └── ws_server.py
├── sample-env
├── scripts
│   ├── install.sh
│   ├── setup.sh
│   ├── start.sh
│   └── win-start.sh
´´´


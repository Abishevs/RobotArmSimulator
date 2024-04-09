from typing import List


class MockServo:
    def __init__(self, index: int, current_angle: int = 90):
        self.current_angle: int = current_angle
        self.index: int = index

    def __str__(self):
        return f"MockServo({self.index}, current_angle: {self.current_angle}"


class WSMockClient:
    def __init__(self) -> None:
        self.servos: List[MockServo]

    def init_servos(self, index: int):
        for i in range(index):
            self.servos.append(MockServo(index))

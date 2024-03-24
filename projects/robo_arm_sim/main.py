import os
import sys

from PySide6.QtWidgets import QApplication

from robo_arm_sim.views import MainWindow
from commonlib.logger import LoggerConfig as Log

def main():
    os.environ['DEBUG_MODE'] = '1'
    Log.setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.complete_setup()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

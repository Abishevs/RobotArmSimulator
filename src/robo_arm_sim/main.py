import os
import sys

from PySide6.QtWidgets import QApplication

from robo_arm_sim.views import MainWindow
from commons.logger import LoggerConfig as Log

def main():
    os.environ['DEBUG_MODE'] = '1'
    Log.setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    


if __name__ == "__main__":
    main()

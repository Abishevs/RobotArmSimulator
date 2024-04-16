import os
import sys

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from robo_arm_sim.views import MainWindow
from commonlib.logger import setup_logging


def main():
    # setup logging
    base_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv()
    setup_logging(base_dir)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.complete_setup()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

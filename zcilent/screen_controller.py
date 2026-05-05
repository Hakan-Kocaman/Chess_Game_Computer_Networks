import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtUiTools import QUiLoader

class ScreenController:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loader = QUiLoader()

        self.stack=QStackedWidget()
        
        login_path = os.path.join(os.path.dirname(__file__), "connectscreen.ui")
        game_path = os.path.join(os.path.dirname(__file__), "main.ui")

        self.login_screen = self.loader.load(login_path)
        self.game_screen = self.loader.load(game_path)

        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.game_screen)
        self.stack.setCurrentIndex(0)
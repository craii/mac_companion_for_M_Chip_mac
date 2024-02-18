import sys
from pathlib import Path
sys.path.append(f"{Path(__file__).resolve().parent.parent}")

from chat_ui import *
from setting_ui import *

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)


class MainWindow(QMainWindow):
    def __init__(self,):
        super().__init__()

        self.setWindowTitle("Mac Companion")
        self.setMinimumHeight(770)
        self.setMinimumWidth(440)

        # tag::QTabWidget[]
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        # end::QTabWidget[]
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)
        if len(sys.argv) == 2:
            print(sys.argv)
            self.argv = sys.argv[1]
        else:
            self.argv = ""

        for menu in ["chat", "history", "setting"]:
            if menu == "chat":
                tabs.addTab(Chat(init_text=self.argv), "chat")
                # tabs.addTab(Chat(), "main")
            if menu == "setting":
                tabs.addTab(Setting(), "setting")
            else:
                pass
        self.setCentralWidget(tabs)


if __name__ in "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

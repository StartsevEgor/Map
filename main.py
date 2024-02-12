import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.params = {
            "ll": "37.530887,55.703118",
            "l": "map",
            "z": 17
        }
        self.getImage()
        self.initUI()

    def getImage(self):
        print(self.params)
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Карта')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def updateUI(self):
        self.getImage()

        self.pixmap = QPixmap(self.map_file)
        # self.image = QLabel(self)
        # self.image.move(0, 0)
        # self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
        # self.initUI()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Up, Qt.Key_Launch8]:
            self.params["z"] += 1 if self.params["z"] < 21 else 0
        if event.key() in [Qt.Key_Down, Qt.Key_Launch2]:
            self.params["z"] -= 1 if self.params["z"] > 0 else 0
        self.updateUI()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

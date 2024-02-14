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
            "spn": "0.001,0.001"
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
        spn_x, spn_y = list(map(float, self.params["spn"].split(",")))
        x, y = list(map(float, self.params["ll"].split(",")))
        if event.key() == Qt.Key_PageUp:
            print(-180 < x - spn_x * 2, x + spn_x * 2 < 180, -90 < y - spn_y * 2, y + spn_y * 2 < 90)
            self.params["spn"] = f"{spn_x * 2},{spn_y * 2}" if (-180 < x - spn_x * 2 and x + spn_x * 2 < 180 and -90 <
                                                                y - spn_y * 2 and y + spn_y * 2 < 90) else self.params[
                "spn"]
        if event.key() == Qt.Key_PageDown:
            self.params["spn"] = f"{spn_x / 2},{spn_y / 2}" if spn_x / 2 > 0.001 and spn_y / 2 > 0.001 else self.params[
                "spn"]
        if event.key() == Qt.Key_Up:
            self.params["ll"] = f'{x},{y + spn_y / 2}' if y + spn_y < 90 else self.params["ll"]
        if event.key() == Qt.Key_Down:
            self.params["ll"] = f'{x},{y - spn_y / 2}' if y - spn_y > -90 else self.params["ll"]
        if event.key() == Qt.Key_Right:
            self.params["ll"] = f'{x + spn_x / 2},{y}' if x + spn_x < 180 else self.params["ll"]
        if event.key() == Qt.Key_Left:
            self.params["ll"] = f'{x - spn_x / 2},{y}' if x - spn_x > -180 else self.params["ll"]
        self.updateUI()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

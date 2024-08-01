# drawing_utils.py

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class TransparentRectangle(QtWidgets.QWidget):
    def __init__(self, top_left, bottom_right, line_color=(255, 255, 0), line_thickness=5):
        super().__init__()

        self.top_left = top_left
        self.bottom_right = bottom_right
        self.line_color = QtGui.QColor(*line_color, 255)
        self.line_thickness = line_thickness

        # Configurar a janela
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

        # Configurar o tamanho da tela
        screen = QtWidgets.QApplication.primaryScreen()
        self.setGeometry(0, 0, screen.size().width(), screen.size().height())

        # Configurar o temporizador para verificar o teclado
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_keypress)
        self.timer.start(100)  # Verifica a cada 100 ms

        self.key_pressed = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        pen = QtGui.QPen(self.line_color)
        pen.setWidth(self.line_thickness)
        painter.setPen(pen)

        # Desenhar o retângulo
        painter.drawRect(QtCore.QRect(self.top_left[0], self.top_left[1], self.bottom_right[0] - self.top_left[0], self.bottom_right[1] - self.top_left[1]))

        # Adicionar coordenadas nos cantos
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(self.top_left[0] + 10, self.top_left[1] - 10, f"{self.top_left}")
        painter.drawText(self.bottom_right[0] + 10, self.top_left[1] - 10, f"({self.bottom_right[0]}, {self.top_left[1]})")
        painter.drawText(self.top_left[0] + 10, self.bottom_right[1] + 20, f"({self.top_left[0]}, {self.bottom_right[1]})")
        painter.drawText(self.bottom_right[0] + 10, self.bottom_right[1] + 20, f"{self.bottom_right}")

    def check_keypress(self):
        if self.key_pressed:
            self.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.key_pressed = True

def draw_transparent_rectangle_on_screen(top_left, bottom_right, line_color=(255, 255, 0), line_thickness=5):
    app = QtWidgets.QApplication(sys.argv)
    rectangle = TransparentRectangle(top_left, bottom_right, line_color, line_thickness)
    rectangle.show()
    sys.exit(app.exec_())

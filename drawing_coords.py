from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QPoint, QTimer
import sys
import pyautogui

class CursorOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cursor Overlay')
        self.setGeometry(0, 0, 1920, 1080)  
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  
        self.cursor_position = QPoint(0, 0)

        
        self.label = QLabel(self)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: yellow;")  
        self.label.setGeometry(0, 0, 200, 20)  

    def update_cursor_position(self, pos):

        self.cursor_position = pos
        self.label.setText(f"X: {self.cursor_position.x()} Y: {self.cursor_position.y()}")
        self.label.move(self.cursor_position.x() + 10, self.cursor_position.y() + 10) 

    def paintEvent(self, event):

        super().paintEvent(event)

def run_cursor_overlay():
    app = QApplication(sys.argv)
    window = CursorOverlay()
    window.showFullScreen()

    def update_position():
        pos = pyautogui.position()
       
        window.update_cursor_position(QPoint(int(pos.x), int(pos.y)))
        app.processEvents()

    
    timer = QTimer()
    timer.timeout.connect(update_position)
    timer.start(50)  

    sys.exit(app.exec_())

if __name__ == '__main__':
    run_cursor_overlay()

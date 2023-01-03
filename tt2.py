from PySide2.QtWidgets import QApplication, QMainWindow, QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('My PyQt Window')
        self.setGeometry(100, 100, 800, 600)
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    view = QWebEngineView()
    view.setHtml(window.render().toHtml())
    view.show()
    app.exec_()

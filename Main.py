from PyQt6.QtCore import QMessageAuthenticationCode
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
import sys
from Login import Login_Window
from MainWindow import Main_Window
import pickle
from UserProfile import User


class NoobStock(QMainWindow):
    def __init__(self):
        super().__init__()
        with open(
                "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/user.txt",
                "rb") as f:
            a = f.readlines()
            if a == []:
                self.login = Login_Window()
                self.login.initializeLoginUi(self)
            else:
                user = pickle.loads(a[0])
                self.createMainWindow(user)

    def createMainWindow(self, a):
        self.main = Main_Window(User(a))


if __name__ == '__main__':
    app = QApplication([])
    main = NoobStock()
    sys.exit(app.exec())

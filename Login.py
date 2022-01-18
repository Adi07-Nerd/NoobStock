from PyQt6.QtCore import QLine
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCheckBox, QLineEdit, QMessageBox, QPushButton, QStackedLayout, QWidget, QLabel
import sys
from Registration import Registration_Window
import pickle


class Login_Window(QWidget):
    def initializeLoginUi(self, papa):
        self.main = papa
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 230)
        self.componentUi()
        self.show()
        self.stack = QStackedLayout()
        self.stack.addWidget(self)

    def componentUi(self):
        self.l1 = QLabel("Login In", self)
        self.l1.move(180, 10)
        self.l1.setFont(QFont('Arial', 20))
        self.name = QLineEdit(self)
        self.name.move(110, 60)
        self.name.setPlaceholderText("Enter Name")
        self.name.resize(220, 20)

        self.passowrd = QLineEdit(self)
        self.passowrd.move(110, 90)
        self.passowrd.setPlaceholderText("Enter Password")
        self.passowrd.resize(220, 20)

        self.see = QCheckBox("Show password", self)
        self.see.move(110, 115)
        self.see.toggle()
        self.see.setChecked(False)
        self.see.stateChanged.connect(self.showPass)

        self.btn = QPushButton("Login", self)
        self.btn.move(100, 140)
        self.btn.resize(200, 40)
        self.btn.clicked.connect(self.clickLogin)
        self.btn1 = QPushButton("Register Now", self)
        self.btn1.clicked.connect(self.clickRegister)
        self.btn1.move(160, 195)

    def showPass(self, status):
        if status:
            self.passowrd.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passowrd.setEchoMode(QLineEdit.EchoMode.Password)

    def clickLogin(self):
        with open(
                "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/user.txt",
                "rb") as f:
            user_index = f.readlines()
            if user_index != []:
                user = pickle.loads(user_index[0])
                self.main.createMainWindow(user)
            else:
                QMessageBox.warning(self, "Invalid user",
                                    "Invalid user id or password",
                                    QMessageBox.StandardButton.Close,
                                    QMessageBox.StandardButton.Close)

    def clickRegister(self):
        self.stack.addWidget(Registration_Window(self))
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def closeEvent(self, event):
        value = QMessageBox.question(
            self, "Quit", "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes)
        event.accept(
        ) if value == QMessageBox.StandardButton.Yes else event.ignore()

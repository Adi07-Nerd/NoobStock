from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QLabel, QLineEdit, QMessageBox, QPushButton, QWidget
import pickle


class Registration_Window(QWidget):
    def __init__(self, a=None):
        super().__init__()
        self.initializeUi()
        self.main = a

    def initializeUi(self):
        """Initialize the window and display its contents to the screen"""
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Registration')
        self.displayWidgetsToCollectInfo()

    def displayWidgetsToCollectInfo(self):
        """Create widgets that will be used to collect informationfrom the user to create a new account."""
        # Create label for image
        new_user_image = "images/new_user_icon.png"
        try:
            with open(new_user_image):
                new_user = QLabel(self)
                pixmap = QPixmap(new_user_image)
                new_user.setPixmap(pixmap)
                new_user.move(150, 60)
        except FileNotFoundError:
            print("Image not found.")
        login_label = QLabel(self)
        login_label.setText("create new account")
        login_label.move(110, 20)
        login_label.setFont(QFont('Arial', 20))
        # Username and fullname labels and line edit widgets
        name_label = QLabel("username:", self)
        name_label.move(50, 180)
        self.name_entry = QLineEdit(self)
        self.name_entry.move(130, 180)
        self.name_entry.resize(200, 20)
        name_label = QLabel("full name:", self)
        name_label.move(50, 210)
        name_entry = QLineEdit(self)
        name_entry.move(130, 210)
        name_entry.resize(200, 20)
        # Create password and confirm password labels and line edit widgets
        pswd_label = QLabel("password:", self)
        pswd_label.move(50, 240)
        self.pswd_entry = QLineEdit(self)
        self.pswd_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.pswd_entry.move(130, 240)
        self.pswd_entry.resize(200, 20)
        confirm_label = QLabel("confirm:", self)
        confirm_label.move(50, 270)
        self.confirm_entry = QLineEdit(self)
        self.confirm_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_entry.move(130, 270)
        self.confirm_entry.resize(200, 20)
        # Create sign up button
        sign_up_button = QPushButton("sign up", self)
        sign_up_button.move(100, 310)
        sign_up_button.resize(200, 40)
        sign_up_button.clicked.connect(self.confirmSignUp)
        back_button = QPushButton("Back", self)
        back_button.move(0, 0)
        back_button.resize(50, 50)
        back_button.clicked.connect(self.backToLogin)

    def confirmSignUp(self):
        """When user presses sign up, check if the passwords match.If they match, then save username and password text to users.txt."""
        pswd_text = self.pswd_entry.text()
        confirm_text = self.confirm_entry.text()
        if pswd_text != confirm_text:
            # Display messagebox if passwords don't match
            QMessageBox.warning(
                self, "Error Message",
                "The passwords you entered do not match. Please try again.",
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        else:  # If passwords match, save passwords to file and return to login# and test if you can log in with new user information.
            with open(
                    "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/user.txt",
                    'wb') as f:
                user = {
                    "Name": "",
                    "NickName": "",
                    "Wallet": 10000,
                    "Favorites": [],
                    "MyStock": {},
                    "UserID": 0,
                    "SessionValid": True
                }
                f.write(pickle.dumps(user))
                f.close()
                self.close()
                self.main.main.createMainWindow(user)
                self.main.close()
                self.main.deleteLater()
                self.deleteLater()

    def backToLogin(self):
        QMessageBox.information(self, "Checking", "Im gettting a call",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)
        self.father.stack.setCurrentIndex(self.father.stack.currentIndex() - 1)

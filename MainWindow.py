from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QStackedLayout, QPushButton, QVBoxLayout, QWidget
from Home import HomeWindow, FavoriteWindow, StockWindow, UserWindow, SearchEngine
from commonFunction import tickerlist, displayMessage


class Main_Window(QWidget):
    def __init__(self, user):
        #################
        #ticker will store dictionary of all tickers
        #tickerModel has representation of tickers for search suggestion
        #stackNo dictionary will hold index at which perticular QWidget get inserted
        # userData will be used to store user class instance.
        #######
        super().__init__()
        self.tickers, self.tickerModel = tickerlist()
        self.stackNo = {}
        self.userData = user
        self.initializeUi()

    def initializeUi(self):
        self.setWindowTitle("Main Window preparation")
        self.setMinimumSize(1000, 800)
        self.createTabs()
        self.show()

    def createTabs(self):
        #topbar layout and adding search layout
        self.searchbox = self.createSearch()
        self.hbox = QGridLayout()
        self.btn = []
        self.btnNames = ["User", "Favorites", "Home", "MyStock"]
        for i in range(len(self.btnNames)):
            func = self.userSetting if i == 0 else (
                self.favoriteClicked if i == 1 else
                (self.homeClicked if i == 2 else self.stockClicked))
            btn = QPushButton(self.btnNames[i])
            btn.setFlat(True)
            btn.clicked.connect(func)
            self.btn.append(btn)
            self.hbox.addWidget(btn, 0, i)
        # self.hbox.addWidget(
        #     self.btn_user,
        #     0,
        #     0,
        # )

        # self.hbox.setSpacing(0)
        # self.hbox.addWidget(self.btn_fav, 0, 1)
        # self.hbox.addWidget(self.btn_home, 0, 2)
        # self.hbox.addWidget(self.btn_myStock, 0, 3)
        self.hbox.addWidget(QLabel("NoobStock"), 0, 4, 1, 4,
                            Qt.AlignmentFlag.AlignRight)

        # self.hbox.addLayout(searchLayout, 2, 2, 2, 4,
        #                     Qt.AlignmentFlag.AlignCenter)

        #creating stack layout
        self.stack = QStackedLayout()
        self.display = HomeWindow(self)
        self.display.setWindowTitle("Hey annoying")
        self.stack.addWidget(self.display)

        #combining topbar and stack widget
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.searchbox)
        self.vbox.addLayout(self.stack)
        self.vbox.setSpacing(0)
        self.vbox.alignment = Qt.AlignmentFlag.AlignLeft

        self.setLayout(self.vbox)

    def homeClicked(self):
        if not self.searchbox.isVisible():
            print("Im here")
            self.searchbox.show()
        self.colorChangeBtn(self.btnNames[2])
        self.stack.setCurrentIndex(
            0) if self.stack.currentIndex() != 0 else displayMessage(
                self, "Stop", "You're Already in Home Tab")

    def favoriteClicked(self):
        if not self.searchbox.isVisible():
            self.searchbox.show()

        self.colorChangeBtn(self.btnNames[1])
        if ("Fav" not in self.stackNo):
            self.stack.addWidget(FavoriteWindow(self))

        self.stack.setCurrentIndex(
            self.stackNo.setdefault("Fav")) if self.stack.currentIndex() != (
                self.stackNo.setdefault("Fav")) else displayMessage(
                    self, "Stop", "You're Already in Favorite Tab")

    def stockClicked(self):
        if not self.searchbox.isVisible():
            self.searchbox.show()
        self.colorChangeBtn(self.btnNames[3])
        if ("MyStock" not in self.stackNo):
            self.stack.addWidget(StockWindow(self))

        self.stack.setCurrentIndex(
            self.stackNo.get("MyStock")) if self.stack.currentIndex() != (
                self.stackNo.get("MyStock")) else displayMessage(
                    self, "Stop", "You're Already in MyStock Tab")

    def userSetting(self):
        if self.searchbox.isVisible():
            self.searchbox.hide()
        self.colorChangeBtn(self.btnNames[0])
        if ("User" not in self.stackNo):
            self.stack.addWidget(UserWindow(self))

        self.stack.setCurrentIndex(
            self.stackNo.get("User")) if self.stack.currentIndex != (
                self.stackNo.get("User")) else displayMessage(
                    self, "Stop", "You're Already in Settings Tab")

    def searchWindow(self, data):
        ############
        # 1.  Condition checks whether instances of search window already created or not if created than updateUi.
        # 2. Condition just add the Search Instance  in the dictionary only if it doesn't exist.
        # 3. Fectch the index of search and set it to current.
        #####
        #will use that object ot call function.
        if ("Search" in self.stackNo):
            obj = self.stack.widget(self.stackNo["Search"])
            obj.updateUi(data)

        if ("Search" not in self.stackNo):
            self.stack.addWidget(SearchEngine(self, data))

        self.stack.setCurrentIndex(
            self.stackNo.get("Search")) if self.stack.currentIndex != (
                self.stackNo.get("Search")) else displayMessage(
                    self, "Stop", "You're Already in Search")
        #this stop message is not necessary in search

    def searchBack(self):
        self.stack.setCurrentIndex(0)

    def colorChangeBtn(self, text):
        # for btn in self.btn:
        #     if btn.text() == text:
        #         print("im in if")
        #         # btn.setStyleSheet("background-color: red")
        #     else:
        #         print("im in else")
        #         btn.setStyleSheet("")
        pass

    def createSearch(self):
        widget = QWidget()
        auto_complete = QCompleter(self.tickerModel)
        auto_complete.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        search = QLineEdit()
        search.setPlaceholderText("Enter Stock Name")
        search.setMinimumSize(237, 44)
        search.setCompleter(auto_complete)
        btn_search = QPushButton("Search")
        btn_search.clicked.connect(lambda: self.searchWindow(search.text()))
        btn_search.setMinimumSize(113, 44)
        searchLayout = QHBoxLayout()
        searchLayout.addStretch(1)
        searchLayout.addWidget(search, Qt.AlignmentFlag.AlignCenter)
        searchLayout.addWidget(btn_search)
        searchLayout.addStretch(1)
        searchLayout.setSpacing(0)
        widget.setLayout(searchLayout)
        return widget

    def closeEvent(self, event):
        value = QMessageBox.question(
            self, "Quit", "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes)
        if (value == QMessageBox.StandardButton.Yes):
            print("exiting")
            del self.userData
            self.close()
            # event.accept()
        # else:
        #     event.ignore()

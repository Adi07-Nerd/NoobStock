from os import close
from PyQt6.QtCore import QSize, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QBoxLayout, QGridLayout, QGroupBox, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QStackedLayout, QPushButton, QScrollArea, QScrollBar, QSizePolicy, QSpinBox, QWidget, QVBoxLayout, QLabel, QWidgetItem
from commonFunction import searchCombo, ListOfStocks, drawGraph, createLabels, displayMessage, getTickerValue, intraDayLatest


class HomeWindow(QWidget):
    def __init__(self, papa):
        ##########
        # 1. setCurrent object name
        # 2. storing instance of main class
        # 3. Adding object name along with index into dictionary for identification purpose
        ####
        super().__init__()
        self.setObjectName("Home")
        self.main = papa
        self.labels = []
        self.addContent()

    def addContent(self):

        self.nsegrp = QGroupBox("National Stock Exchange")
        self.listNse = drawGraph("^NSEI")
        labelList = [
            "Open", "Market Cap", "Day Highest", "Close", "Dividend",
            "52 Weeks highest"
        ]
        vnse_box = QVBoxLayout(self.nsegrp)
        vnse_box.addWidget(self.listNse)
        vnse_box.addLayout(createLabels(self, 6, labelList))

        self.bsegrp = QGroupBox("Bombay Stock Exchange")
        self.listBse = drawGraph("HDFC.BO")
        self.labelListBse = QGridLayout()
        for i in range(6):
            if i < 3:
                self.labelListBse.addWidget(QLabel(str(i) + " Lable"), 0, i)
            else:
                self.labelListBse.addWidget(QLabel(str(i) + " Lable"), 1,
                                            (i - 3))
        vbse_box = QVBoxLayout(self.bsegrp)
        vbse_box.addWidget(self.listBse)
        vbse_box.addLayout(self.labelListBse)

        self.gain_lose = QGroupBox("Gainers & Losers")
        self.fav = ListOfStocks(self.btnClicked, [
            "Reliance", "TaTa", "WIPRO", "INFOSYS", "Tesla", "TCS", "BLAH",
            "Blah"
        ])
        self.fav1 = ListOfStocks(self.btnClicked, [
            "Reliance", "TaTa", "WIPRO", "INFOSYS", "Tesla", "TCS", "BLAH",
            "Blah"
        ])
        vlose_gain = QVBoxLayout(self.gain_lose)
        vlose_gain.addStretch(3)
        vlose_gain.addWidget(QLabel("GAINERS"))
        vlose_gain.addWidget(self.fav1)
        vlose_gain.addStretch(1)
        vlose_gain.addWidget(QLabel("Losers"))
        vlose_gain.addWidget(self.fav)
        vlose_gain.addStretch(3)

        hbox = QHBoxLayout()
        hbox.addWidget(self.nsegrp)
        hbox.addWidget(self.bsegrp)
        hbox.addWidget(self.gain_lose)

        self.setLayout(hbox)

    def btnClicked(self, some):
        print(type(some))
        QMessageBox.information(self, "Btn Action", "I got clicked.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)


class FavoriteWindow(QWidget):
    def __init__(self, papa):
        ##########
        # 1. setCurrent object name
        # 2. storing instance of main class
        # 3. Adding object name along with index into dictionary for identification purpose
        ####
        super().__init__()
        self.setObjectName("Fav")
        self.main = papa
        self.labels = []
        papa.stackNo.setdefault(self.objectName(),
                                len(papa.stackNo.keys()) + 1)
        self.addContent()

    def addContent(self):
        self.favbox = QGroupBox("Favorite List")
        self.favLabel = QLabel("Favorites")
        self.vfavBox = QVBoxLayout(self.favbox)
        self.vfavBox.addWidget(self.favLabel)
        self.fav11 = ListOfStocks(self.btnClick,
                                  self.main.userData.info["Favorites"])
        self.vfavBox.addWidget(self.fav11)

        self.favGrap = QGroupBox()
        self.graphStack = QStackedLayout()
        if (self.main.userData.info["Favorites"] != []):
            graph = drawGraph(
                getTickerValue(self, self.main.userData.info["Favorites"][0]))
        else:
            graph = QLabel("Oops Favorite list is empty")

        self.graphStack.insertWidget(0, graph)
        labelList = [
            "Open", "Market Cap", "Day Highest", "Close", "Dividend",
            "52 Weeks highest"
        ]
        v_box = QVBoxLayout(self.favGrap)
        v_box.addWidget(self.graphStack)
        v_box.addLayout(createLabels(self, 6, labelList))

        self.favHbox = QHBoxLayout()
        self.favHbox.addWidget(self.favbox)
        self.favHbox.addStretch(3)
        self.favHbox.addWidget(self.favGrap)

        self.setLayout(self.favHbox)

    def btnClick(self, some):
        sender = self.sender()
        QMessageBox.information(self, "Btn Action",
                                sender.objectName() + " I got clicked.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)

    def addFromSearch(self, text, graph):
        layout = (self.fav11.widget()).layout()
        itemHbox = QHBoxLayout()
        lb1 = QPushButton(text)  #stock Name
        lb1.setFlat(True)
        lb1.clicked.connect(lambda: displayMessage(self, "Hey", text))
        lb2 = QLabel(text="CurPrice")  #current day highest
        lb3 = QLabel(text="compare")  #compare to last day closing
        itemHbox.addWidget(lb1)
        itemHbox.addWidget(lb2)
        itemHbox.addWidget(lb3)
        btn = QPushButton("More")
        btn.setObjectName("More " + text)
        btn.setStyleSheet("color:green")
        btn.clicked.connect(self.btnClick)
        itemHbox.addWidget(btn)
        layout.addLayout(itemHbox)
        self.graph = graph
        #alighntment is not proper


class StockWindow(QWidget):
    def __init__(self, papa):
        ##########
        # 1. setCurrent object name
        # 2. storing instance of main class
        # 3. Adding object name along with index into dictionary for identification purpose
        ####
        super().__init__()
        self.setObjectName("MyStock")
        self.main = papa
        self.labels = []
        papa.stackNo.setdefault(self.objectName(),
                                len(papa.stackNo.keys()) + 1)
        self.addContent()

    def addContent(self):
        #main Content
        self.purchase = QGroupBox()
        self.list = QLabel("Purchased Stock")
        v_box = QVBoxLayout(self.purchase)
        v_box.addWidget(self.list)

        if self.main.userData.info["MyStock"] == []:
            self.fav = QLabel(
                "Oops seems like you don't have any purchase stock.")
            self.fav.setWordWrap(True)
        else:
            self.fav = ListOfStocks(self.btnClicked,
                                    self.main.userData.info["MyStock"])

        v_box.addWidget(self.fav)

        self.userDetails = QGroupBox("User Details")
        self.name = QLabel("Aditya")

        labelList = [
            "Open", "Market Cap", "Day Highest", "Close", "Dividend",
            "52 Weeks highest"
        ]

        v1_box = QVBoxLayout(self.userDetails)
        v1_box.addWidget(self.name)
        v1_box.addLayout(createLabels(self, 6, labelList))

        hbox = QHBoxLayout()
        hbox.addWidget(self.purchase)
        hbox.addWidget(self.userDetails)
        self.setLayout(hbox)

    def btnClicked(self):
        sender = self.sender()
        QMessageBox.information(self, "Action",
                                sender.objectName() + " got clicked.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)

    def updateUi(self, stock, price, quantity):
        layout = (self.fav.widget()).layout()
        itemHbox = QHBoxLayout()
        lb1 = QPushButton(stock)  #stock Name
        lb1.setFlat(True)
        lb1.clicked.connect(lambda: displayMessage(self, "Hey", stock))
        lb2 = QLabel(text=str(price))  #current day highest
        lb3 = QLabel(text=str(quantity))  #compare to last day closing
        itemHbox.addWidget(lb1)
        itemHbox.addWidget(lb2)
        itemHbox.addWidget(lb3)
        btn = QPushButton("More")
        btn.setObjectName(stock)
        btn.setStyleSheet("color:green")
        btn.clicked.connect(self.btnClick)
        itemHbox.addWidget(btn)
        layout.addLayout(itemHbox)


class UserWindow(QWidget):
    def __init__(self, papa):
        super().__init__()
        self.setObjectName("User")
        papa.stackNo.setdefault(self.objectName(),
                                len(papa.stackNo.keys()) + 1)
        self.addContent()

    def addContent(self):
        v_box = QVBoxLayout()
        v_box.addWidget(QLabel("User Setting"))
        self.setLayout(v_box)


class SearchEngine(QWidget):
    def __init__(self, papa, data):
        ##########
        # 1. setCurrent object name
        # 2. storing instance of main class
        # 3. Adding object name along with index into dictionary for identification purpose
        ####
        super().__init__()
        self.setObjectName("Search")
        self.main = papa  # there is no need of this here as of now
        self.labels = []
        self.main.stackNo.setdefault(self.objectName(),
                                     len(papa.stackNo.keys()) + 1)
        self.addContent(data)

    def addContent(self, stock_name):
        ###############
        # Actually Content
        ####
        self.searchGraph = QGroupBox()
        self.sname = QLabel(stock_name)
        self.graph = drawGraph(getTickerValue(self, stock_name))

        self.names = ["Add To Fav.", "Add To MyStocks", "Back"]
        hboxButton = QHBoxLayout()
        for i in range(len(self.names)):
            func = (self.favBtnClick if i == 0 else (
                self.purchaseBtnClicked if i == 1 else self.backBtnClicked))
            btn = QPushButton(self.names[i])
            btn.clicked.connect(func)
            hboxButton.addWidget(btn)

        self.vAll = QVBoxLayout(self.searchGraph)
        self.vAll.addWidget(self.sname)
        self.vAll.addWidget(self.graph)
        self.vAll.addLayout(hboxButton)

        self.searchData = QGroupBox("Details")
        # self.searchListItems = QGridLayout(self.searchData)
        # for i in range(8):
        #     if i < 4:
        #         self.searchListItems.addWidget(QLabel(str(i) + " Lable"), 0, i)
        #     else:
        #         self.searchListItems.addWidget(QLabel(str(i) + " Lable"), 1,
        #                                        (i - 4))
        labelList = [
            "Open", "Market Cap", "Day Highest", "Close", "Dividend",
            "52 Weeks highest", "Name", "I DOnt know More"
        ]
        self.searchData.setLayout(createLabels(self, 8, labelList))
        self.hAll = QHBoxLayout()
        self.hAll.addWidget(self.searchGraph)
        self.hAll.addWidget(self.searchData)
        self.setLayout(self.hAll)

    def updateUi(self, message):
        #reimpletment the above thing
        self.sname.setText(message)

    def favBtnClick(self):
        ##########
        # second time it's not working emiting
        # For later pass info object tool along with graph.
        #####
        if ("Fav" in self.main.stackNo):
            if (self.sname not in self.main.userData.info["Favorites"]):
                if (self.main.userData.addToFav(self.sname.text())):
                    displayMessage(
                        self, "Successfull",
                        self.sname.text() + " Stock Added in favorite.")
                    fav = self.main.stack.widget(self.main.stackNo["Fav"])
                    fav.addFromSearch(self.sname.text(), self.graph)
                else:
                    displayMessage(self, "Error", "Oops something went wrong.")
            else:
                displayMessage(self, "Stop",
                               "You already has this in favorites!!!!")
        else:
            if (self.sname not in self.main.userData.info["Favorites"]):
                if (self.main.userData.addToFav(self.sname.text())):
                    displayMessage(
                        self, "Successfull",
                        self.sname.text() + " Stock Added in favorite.")
                else:
                    displayMessage(self, "Error", "Oops something went wrong.")

    def purchaseBtnClicked(self):
        # displayMessage(self, "hey", "Purchase getting call.")
        #create a purchase window on top of this and don't allow any action from this window.
        self.purchaseWindow()
        #add function that will varify mystock exist other update ui call
        # self.isExist()

    def backBtnClicked(self):
        self.main.stack.setCurrentIndex(0)

    def purchaseWindow(self):
        #################
        # Remember to restict the main window to interact you have to put modality before show.
        ############
        closeValue = (intraDayLatest(getTickerValue(self, self.sname.text()),
                                     i="1m")).tail(1)["Close"]
        closeValue = round([x for x in closeValue.iteritems()][0][1], 2)

        def confirmPurchase():
            result = QMessageBox.question(
                self, "Transaction", "Are you sure you want to purchase",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes)

            if result == QMessageBox.StandardButton.Yes:
                self.main.userData.purchaseStock(self.sname.text(), closeValue,
                                                 sp.value())
                if ("MyStock" in self.main.stackNo):
                    obj = self.main.stack.widget("MyStock")
                    obj.updateUi()
                response = QMessageBox.information(
                    self, "Successfull",
                    "Stock successfully added into your account",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok)

                if response == QMessageBox.StandardButton.Ok:
                    self.widget.close()
            else:
                print("User cancelled")

        self.widget = QWidget()
        lbl = QLabel(self.sname.text())
        lbl2 = QLabel("Amount of stock want?")
        sp = QSpinBox()
        sp.setRange(1, 30)
        sp.valueChanged.connect(
            lambda x=sp.value(): lb3.setText('\u20B9 ' + str(closeValue * x)))
        lb3 = QLabel('\u20B9 ' + str(closeValue))
        btn = QPushButton("Purchase")
        btn.clicked.connect(confirmPurchase)

        grid = QGridLayout(self.widget)
        grid.addWidget(lbl, 0, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(lbl2, 0, 4, Qt.AlignmentFlag.AlignRight)
        grid.addWidget(sp, 0, 5, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(btn, 1, 0)
        grid.addWidget(lb3, 1, 2, 1, 3, Qt.AlignmentFlag.AlignRight)
        self.widget.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.widget.show()

    def isExist(self, name):
        pass

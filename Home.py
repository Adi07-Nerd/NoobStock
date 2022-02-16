from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QMessageBox, QPushButton, QSizePolicy, QSpinBox, QWidget, QVBoxLayout, QLabel
from commonFunction import graphWindow, threadSafeData, ListOfStocks, getStockItem, createLabels, displayMessage, intraDayLatest


class HomeWindow(QWidget):
    def __init__(self, papa):
        ##########
        # 1. setCurrent object name
        # 2. storing instance of main class
        # 3. Adding object name along with index into dictionary for identification purpose
        # 4 make sure addContent is on last line otherwise there could be undefined variable error
        ####
        super().__init__()
        self.setObjectName("Home")
        self.main = papa
        self.labels = []
        self.threadpool = QThreadPool()

        self.addContent()

    def addContent(self):

        self.nsegrp = QGroupBox()
        self.nsegrp.setSizePolicy(QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Minimum)

        #for testing purpose commented this and BSE also
        # self.listNse = drawGraph(self,
        #                          "National Stock Exchange",
        #                          hardCoded="^NSEI")

        self.listNse = QLabel("NationalStockExchange loading...")
        threadSafeData(self, "National Stock Exchange", "^NSEI")
        self.graph_line_Nse = None
        labelList = [
            "Open", "Market Cap", "Day Highest", "Close", "Dividend",
            "52 Weeks highest"
        ]
        vnse_box = QVBoxLayout(self.nsegrp)
        vnse_box.addWidget(self.listNse)
        vnse_box.addLayout(createLabels(self, 6, labelList))

        self.bsegrp = QGroupBox()
        self.bsegrp.setSizePolicy(QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Minimum)

        # self.listBse = drawGraph(self,
        #                          "Bombay Stock Exchage",
        #                          hardCoded="^BSESN")
        self.listBse = QLabel("BombayStockExchange")
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

        #LoseandProfit
        self.gain_lose = QGroupBox()
        self.gain_lose.setSizePolicy(QSizePolicy.Policy.Minimum,
                                     QSizePolicy.Policy.Minimum)

        self.gain_lose.setFlat(True)  #this will make disappear the box
        self.fav = ListOfStocks(self.btnClicked,
                                a=[
                                    "Reliance", "TaTa", "WIPRO", "INFOSYS",
                                    "Tesla", "TCS", "BLAH", "Blah"
                                ])
        self.fav1 = ListOfStocks(self.btnClicked,
                                 a=[
                                     "Reliance", "TaTa", "WIPRO", "INFOSYS",
                                     "Tesla", "TCS", "BLAH", "Blah"
                                 ])

        #check how to make scroll bar side thing invisible
        vlose_gain = QVBoxLayout(self.gain_lose)
        v1 = QVBoxLayout()
        v1.addStretch(3)
        g = QLabel("GAINERS")
        g.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        v1.addWidget(g)
        v1.addWidget(self.fav1)
        v1.addStretch(1)
        b = QLabel("Losers")
        b.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        v1.addWidget(b)
        v1.addWidget(self.fav)
        v1.addStretch(3)
        vlose_gain.addLayout(v1, Qt.AlignmentFlag.AlignVCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(self.nsegrp)
        hbox.addWidget(self.bsegrp)
        hbox.addWidget(self.gain_lose, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(hbox)

    def onIntervalChange(self, text):
        displayMessage(self, text, "I got changed")

    def onDayChange(self, text):
        displayMessage(self, text, "I got clicked.")

    def btnClicked(self, some):
        QMessageBox.information(self, "Btn Action", "I got clicked.",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok)

    def onError(self, text):
        self.listNse.setText(text)

    def onComplete(self, result):
        ###
        # First if will add graphwindow object when there is no graph widget existing
        ###
        if (self.listNse.objectName != "graphWindow"):
            layout = self.nsegrp.layout()
            layout.removeWidget(self.listNse)
            self.listNse.deleteLater()
            self.listNse = graphWindow(self)
            layout.insertWidget(0, self.listNse)

        self.graph_line_Nse = getStockItem(self.listNse, result[0][0],
                                           result[0][1], result[1])


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
        self.graphDict = {}
        self.threadpool = QThreadPool()
        papa.stackNo.setdefault(self.objectName(),
                                len(papa.stackNo.keys()) + 1)

        self.addContent()

    def addContent(self):
        #groupbox alignment its not working.
        #favoriteListgroup
        self.favbox = QGroupBox()
        # self.favbox.setStyleSheet("border:0px")
        self.favbox.setSizePolicy(QSizePolicy.Policy.Preferred,
                                  QSizePolicy.Policy.Preferred)
        #this make a vertical line visible on top of box
        # self.favbox.setFlat(True)
        self.favLabel = QLabel("Favorites")
        # self.favLabel.setAlignment(Qt.AlignmentFlag.AlignBottom)

        #for Label and Scroll Widget
        self.vfavBox = QVBoxLayout(self.favbox)
        self.vfavBox.addStretch(1)
        self.vfavBox.addWidget(self.favLabel)
        self.fav11 = ListOfStocks(self.moreBtnClick, self.btnClick,
                                  self.main.userData.info["Favorites"])
        # self.fav11.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vfavBox.addSpacing(2)
        self.vfavBox.addWidget(self.fav11)
        self.vfavBox.addStretch(1)

        self.favGrap = QGroupBox()
        self.favGrap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.favGrap.setStyleSheet("border:0px")
        self.favGrap.setSizePolicy(QSizePolicy.Policy.Maximum,
                                   QSizePolicy.Policy.Maximum)

        if (self.main.userData.info["Favorites"] != []):
            firstFav = self.main.userData.info["Favorites"][0]
            # graph = drawGraph(self, firstFav)
            self.graphContainer = QLabel(firstFav + "Loading")
            self.current_graphLine = None
            threadSafeData(self, firstFav)
        else:
            self.graphContainer = QLabel("Oops Favorite list is empty")

        labelList = [
            "Open", "Market Cap", "Day Highest", "Close", "Dividend",
            "52 Weeks highest"
        ]
        v_box = QVBoxLayout(self.favGrap)
        v_box.addWidget(self.graphContainer)
        v_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_box.addSpacing(12)
        v_box.addLayout(createLabels(self, 6, labelList))
        v_box.addStretch(0)

        self.favHbox = QHBoxLayout()
        self.favHbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.favHbox.addStretch(1)
        self.favHbox.addWidget(self.favbox)
        self.favHbox.addSpacing(10)
        self.favHbox.addWidget(self.favGrap)
        self.favHbox.addStretch(1)

        self.setLayout(self.favHbox)

    def onIntervalChange(self, text):
        displayMessage(self, text, "I got changed")

    def onDayChange(self, text):
        displayMessage(self, text, "I got clicked.")

    def onError(self, text):
        # set error text on label
        self.graphContainer.setText(text)

    def onComplete(self, result):
        #####
        # layout store the layout of favGrap
        # than we remove the label from layout after getting data
        # than we call stockGraph to plot
        # add the graph_line object to the dictionary
        ##
        if self.graphContainer.objectName() != "graphWindow":
            layout = self.favGrap.layout()
            layout.removeWidget(self.graphContainer)
            self.graphContainer.deleteLater()
            self.graphContainer = graphWindow(self)
            layout.insertWidget(1, self.graphContainer)

        plot_widget = self.graphContainer.layout().widget()
        if (self.current_graphLine != None):
            #remove the widget
            plot_widget.removeItem(self.current_graphLine)

        self.current_graphLine = getStockItem(plot_widget, result[0][0],
                                              result[0][1], result[1])

        self.graphDict[result[1]] = self.current_graphLine

    def moreBtnClick(self):
        sender = self.sender().objectName()
        displayMessage(self, "More", sender)

    def btnClick(self):
        sender = self.sender().objectName()

        if (sender not in self.graphDict):
            self.addGraphObject(sender)
            pass
            #add object by taking following reference
            # self.graphStack.addWidget(drawGraph(sender.objectName()))

        self.graphStack.setCurrentIndex(
            self.isExist(sender)) if self.graphStack.currentIndex() != (
                self.isExist(sender)) else displayMessage(
                    self, "Stop", "You're Already Opened that graph")

    def addFromSearch(self, text, graph):
        self.addGraphObject(text, graph)
        layout = (self.fav11.widget()).layout()
        itemHbox = QHBoxLayout()
        lb1 = QPushButton(text)  #stock Name
        lb1.setObjectName(text)
        lb1.setFlat(True)
        lb1.clicked.connect(self.btnClick)
        lb2 = QLabel(text="CurPrice")  #current day highest
        lb3 = QLabel(text="compare")  #compare to last day closing
        itemHbox.addWidget(lb1)
        itemHbox.addWidget(lb2)
        itemHbox.addWidget(lb3)
        btn = QPushButton("More")
        btn.setObjectName("More " + text)
        btn.setStyleSheet("color:green")
        btn.clicked.connect(self.moreBtnClick)
        itemHbox.addWidget(btn)
        layout.addLayout(itemHbox)
        #alighntment is not proper

    def isExist(self, name):
        return self.graphDict.setdefault(
            name) if name in self.graphDict else -1

    def addGraphObject(self, name, graphObject=None):
        ###
        # it checks if currently graphObject is avaible and if not than create new graphObject
        ###

        if graphObject == None:
            threadSafeData(self, name)
        else:
            plot_widget = self.graphContainer.layout().widget()
            plot_widget.removeItem(self.current_graphLine)
            self.current_graphLine = graphObject
            self.graphDict[name] = self.current_graphLine
            plot_widget.addItem(self.current_graphLine)


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
        self.list.setAlignment(Qt.AlignmentFlag.AlignLeft)
        v_box = QVBoxLayout(self.purchase)
        v_box.addWidget(self.list, Qt.AlignmentFlag.AlignBottom)

        if self.main.userData.info["MyStock"] == []:
            self.fav = QLabel(
                "Oops seems like you don't have any purchase stock.")
            self.fav.setWordWrap(True)
        else:
            self.fav = ListOfStocks(
                self.btnClicked, a=self.main.userData.info["MyStock"].keys())
        self.fav.setAlignment(Qt.AlignmentFlag.AlignTop)
        v_box.addWidget(self.fav, Qt.AlignmentFlag.AlignLeft)
        v_box.addStretch(1)

        self.userDetails = QGroupBox("User Details")
        self.name = QLabel("Aditya")

        labelList = [
            "Open", "Market Cap", "Day Highest", "Close", "Dividend",
            "52 Weeks highest"
        ]

        v1_box = QVBoxLayout(self.userDetails)
        v1_box.addWidget(self.name)
        v1_box.addLayout(createLabels(self, 6, labelList))
        v1_box.addStretch(0)

        hbox = QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(self.purchase)
        hbox.addSpacing(10)
        hbox.addWidget(self.userDetails)
        hbox.addStretch(0)
        self.setLayout(hbox)

    def onIntervalChange(self, text):
        displayMessage(self, text, "I got changed")

    def onDayChange(self, text):
        displayMessage(self, text, "I got clicked.")

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
        self.graphContainer = QLabel(stock_name + "Loading")
        self.current_graphLine = None
        threadSafeData(self, stock_name)
        # self.graph = drawGraph(self, stock_name)

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

    def onIntervalChange(self, text):
        displayMessage(self, text, "I got changed")

    def onDayChange(self, text):
        displayMessage(self, text, "I got clicked.")

    def error(self, text):
        self.graphContainer.setText(text)

    def onComplete(self, result):
        #####
        # layout store the layout of favGrap
        # than we remove the label from layout after getting data
        # than we call stockGraph to plot
        # add the graph_line object to the dictionary
        ##
        if self.graphContainer.objectName() != "graphWindow":
            layout = self.favGrap.layout()
            layout.removeWidget(self.graphContainer)
            self.graphContainer.deleteLater()
            self.graphContainer = graphWindow(self)
            layout.insertWidget(1, self.graphContainer)

        plot_widget = self.graphContainer.layout().widget()
        if (self.current_graphLine != None):
            #remove the widget
            plot_widget.removeItem(self.current_graphLine)

        self.current_graphLine = getStockItem(plot_widget, result[0][0],
                                              result[0][1], result[1])

    def updateUi(self, message):
        #reimpletment the above thing
        self.sname.setText(message)

    def favBtnClick(self):
        ##########
        # second time it's not working emiting
        # For later pass info object tool along with graph.
        #####
        if ("Fav" in self.main.stackNo):
            if (self.sname.text() not in self.main.userData.info["Favorites"]):
                if (self.main.userData.addToFav(self.sname.text())):
                    displayMessage(
                        self, "Successfull",
                        self.sname.text() + " Stock Added in favorite.")
                    fav = self.main.stack.widget(self.main.stackNo["Fav"])
                    fav.addFromSearch(self.sname.text(),
                                      self.current_graphLine)
                else:
                    displayMessage(self, "Error",
                                   "Can't add to favorite list.")
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
        closeValue = (intraDayLatest(self.main.data_provider.getTickerValue(
            self, self.sname.text()),
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
                displayMessage(self, "Cancellation",
                               "Your cancellation completed")

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

from tkinter import E
from unicodedata import name
from PyQt6.QtWidgets import QGridLayout, QLabel, QSpinBox, QMessageBox, QPushButton, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import Qt
import yfinance as yf
import pickle
import datetime as dt
import pyqtgraph as pg

pg.setConfigOption("background", "w")
pg.setConfigOption('foreground', 'k')

import pandas as pd

from Worker_Slot_Runnable import Worker


class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [
            dt.datetime.fromtimestamp(value).strftime("%Y-%m-%d")
            for value in values
        ]


def graphWindow(obj):
    try:
        graphWin = QWidget()
        graphWin.setObjectName("graphWindow")
        graphWin.setMinimumSize(300, 300)

        sp = QSpinBox()
        sp.setRange(1, 3)
        sp.setSuffix(" Min")
        sp.valueChanged.connect(
            lambda x=sp.value(): obj.onIntervalChange(str(x)))

        hbox = createButtons(func=obj.onDayChange,
                             names=["1 Day", "1 Month", "1 Year"])

        hbox.insertWidget(0, sp)
        graphWin.setSizePolicy(QSizePolicy.Policy.Maximum,
                               QSizePolicy.Policy.Preferred)
        vbox = QVBoxLayout()
        dataaxis = TimeAxisItem(orientation="bottom")
        graphWidget = pg.PlotWidget(axisItems={"bottom": dataaxis})
        vbox.addLayout(hbox)
        vbox.addWidget(graphWidget)
        graphWin.setLayout(vbox)
    except Exception as e:
        print(str(e))
    return graphWin


def getStockItem(graphWindow, x_date, y_value, name):
    ###
    #
    ##
    try:
        ##to do get the current ploted line remove that line add new item
        graphObject = (graphWindow.layout()).itemAt(1).widget()
        graphObject.setTitle(name, size="15pt")
        pen = pg.mkPen(color=(255, 0, 0))
        return graphObject.plot(x_date, y_value, pen=pen, clear=True)

    except Exception as e:
        print(str(e))


def threadSafeData(obj, a, hardCoded=None):
    worker = Worker(obj, a, hardCoded)
    worker.signals.finished.connect(obj.onComplete)
    worker.signals.error.connect(obj.onError)
    obj.threadpool.start(worker)


def searchCombo(obj, slayout):
    ##almost depreciated
    ##########
    # 1. obj parameter holds value of self object
    ####
    #how to change parent
    vbox = QVBoxLayout()
    vbox.addLayout(obj.main.searchbox)
    vbox.addLayout(slayout)
    return vbox


def ListOfStocks(detailFunc, showGraph=None, a=[]):
    # main to connnect with the function of the parents and list of the stock.
    scrollarea = QScrollArea()
    scrollw = QWidget()
    listVBox = QVBoxLayout(scrollw)
    listVBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
    for x in a:
        ##showing bool object has no attribut like split in stockname
        itemHbox = QHBoxLayout()
        if showGraph != None:
            lb1 = QPushButton(x)  #stock Name
            lb1.setObjectName(x)
            lb1.setFlat(True)
            lb1.clicked.connect(showGraph)
        else:
            lb1 = QLabel(x)
        lb2 = QLabel(text="CurPrice")  #current day highest
        lb3 = QLabel(text="compare")  #compare to last day closing
        itemHbox.addWidget(lb1)
        itemHbox.addWidget(lb2)
        itemHbox.addWidget(lb3)
        btn = QPushButton("More")
        btn.setObjectName(x)
        btn.setStyleSheet("color:green")
        btn.clicked.connect(detailFunc)
        itemHbox.addWidget(btn)
        # itemHbox.setObjectName("Hbox")
        listVBox.addLayout(itemHbox)
        listVBox.setSpacing(2)
        listVBox.setObjectName("listvbox")
    scrollarea.setWidget(scrollw)
    scrollarea.setStyleSheet("border:2px")
    scrollarea.setMaximumSize(300, 300)
    scrollarea.setSizePolicy(QSizePolicy.Policy.Preferred,
                             QSizePolicy.Policy.Maximum)
    scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    return scrollarea


def intraDayFirst(a, p="1d", i="5min"):
    #this to get intraday data
    a = yf.download(a, period=p, interval=i)
    return a[['Open', 'Close']]


def intraDayLatest(a, p="1d", i="5min"):
    #to retrieve las updated value
    return (yf.download(a, period=p, interval=i)).tail(1)


def createLabels(obj, number, names=[]):
    ##############
    # 1. obj has instance of current class , number stores no. of labels, names stores list of names put on labels
    # 2. mid divide number of label in two equal parts
    # 3. Make sure your obj has attribute name labels=[]
    ######
    searchListItems = QGridLayout()
    mid = number / 2
    for i in range(number):
        if i < mid:
            obj.labels.insert(i, QLabel(names[i] + " Lable"))
            searchListItems.addWidget(obj.labels[i], 0, i)
        else:
            obj.labels.insert(i, QLabel(names[i] + " Lable"))
            searchListItems.addWidget(obj.labels[i], 1, (i - mid))

    return searchListItems


def createButtons(func, names=[]):
    ###
    # make sure lambda have first variable as checked because it takes check value.
    ###
    hbox = QHBoxLayout()
    for i in range(len(names)):
        buttons = QPushButton(names[i])
        buttons.clicked.connect(lambda checked, text=names[i]: func(text))
        hbox.addWidget(buttons)
    return hbox


def displayMessage(obj, title, message):
    return QMessageBox.information(obj, title, message,
                                   QMessageBox.StandardButton.Ok,
                                   QMessageBox.StandardButton.Ok)

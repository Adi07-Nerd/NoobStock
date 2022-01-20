from unicodedata import name
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget, QCompleter
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.express as px
from plotly.offline import plot
import yfinance as yf
import pickle


def tickerlist():
    # providing dicitonary of valid tickers and model for auto completor
    with open(
            "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/tickerlist.txt",
            "rb") as file:
        data = file.read()
        data = pickle.loads(data)
        # print(data)
        file.close()
        words = []
        for i, j in data.items():
            for a in j:
                #spliting and finding who belongs to which exchanges
                if (a.split(".")[1] == "NS"):
                    words.append(i + " " + "(NSE)")
                else:
                    words.append(i + " " + "(BSE)")
        return data, words


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
    scrollarea.setMaximumSize(300, 300)
    scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    return scrollarea


def intraDayFirst(a, p="1d", i="5min"):
    #this to get intraday data
    a = yf.download(a, period=p, interval=i)
    return a[['Open', 'Close']]


def intraDayLatest(a, p="1d", i="5min"):
    #to retrieve las updated value
    return (yf.download(a, period=p, interval=i)).tail(1)


def drawGraph(obj, a, hardCoded=None):
    #take valid ticker and provide data from yahoo finance
    if hardCoded != None:
        tickerValue = hardCoded
    else:
        tickerValue = getTickerValue(obj, a)
    data = yf.download(tickers=tickerValue,
                       period='1y',
                       interval='1d',
                       group_by='ticker')
    close_data = data[['Close']]

    c_area = px.area(close_data, title=a + ' CLOSE PRICE')
    c_area.update_xaxes(
        title_text='Date',
        rangeslider_visible=True,
        rangeselector=dict(buttons=list([
            dict(count=1, label='1M', step='month', stepmode='backward'),
            dict(count=6, label='6M', step='month', stepmode='backward'),
            dict(count=1, label='YTD', step='year', stepmode='todate'),
            dict(count=1, label='1Y', step='year', stepmode='backward'),
            dict(step='all')
        ])))

    c_area.update_yaxes(title_text=a + 'Close Price', tickprefix='\u20B9')
    c_area.update_layout(showlegend=False,
                         title={
                             'text': a + ' CLOSE PRICE',
                             'y': 0.9,
                             'x': 0.5,
                             'xanchor': 'center',
                             'yanchor': 'top'
                         })

    # html = '<html><body>'
    html = plot(c_area,
                output_type='div',
                include_plotlyjs='cdn',
                config={'displayModeBar': False})
    # html += '</body></html>'

    # we create an instance of QWebEngineView and set the html code
    plot_widget = QWebEngineView()
    plot_widget.setObjectName(a)
    plot_widget.setHtml(html)
    return plot_widget


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


def createButtons(obj, number, func, names=[]):
    hbox = QHBoxLayout()
    for i in range(len(names)):
        buttons = QPushButton(names[i])
        buttons.clicked.connect(lambda text=names[i]: func(text))
        hbox.addWidget(buttons)
    return hbox


def displayMessage(obj, title, message):
    return QMessageBox.information(obj, title, message,
                                   QMessageBox.StandardButton.Ok,
                                   QMessageBox.StandardButton.Ok)


def getTickerValue(obj, stock):
    ############
    # make sure your main HomeWindow object is store in main only
    # This function takes search text and result its ticker to search from yahoo finance
    ######
    splited = stock.split(" ")
    name = " ".join(splited[:-1])
    options = obj.main.tickers[name]
    if (len(options) > 1):
        return "".join(options[0] if splited[-1] == "(NSE)" else options[1])
    else:
        return "".join(options)

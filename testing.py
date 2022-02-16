from datetime import datetime
import random
from this import d
from turtle import setx, sety
import pandas as pd
# import matplotlib.pyplot as plt

# data = pd.read_csv("C:/Users/shyam/Documents/aditya/Project/HDFC.csv",
#                    index_col="Date")
# print(data)
# fig, ax = plt.subplots()
# print(data[["Close"]].min())
# ax.plot(data.index, data[["Close"]])
# # ax.fill_between(data.index, data[["Close"]].min(), data["Close"], alpha=0.7)
# ax.set_ylabel("price")
# fig.suptitle('Google (GOOG) daily closing price')
# fig.autofmt_xdate()
# plt.show()
# fig.set
import numpy as np
import sys
from PyQt6 import QtCore
from PyQt6 import QtWidgets  # import PyQt6 before matplotlib
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pyparsing import line

from commonFunction import separation

matplotlib.use("QtAgg")
fig = Figure(figsize=(5, 6), dpi=100)
b = FigureCanvasQTAgg(fig)
fig.add_subplot


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.line = None
        super().__init__(fig)

    def plotting(self,
                 x_vec,
                 y1_data,
                 identifier='',
                 alpha=0.8,
                 pause_time=0.01):
        if self.line == None:
            self.ion
            self.line, _ = self.axes.plot(x_vec, y1_data, 'r', alpha)
            self.axes.set_ylabel('Y Label')
            self.axes.set_xlabel('x Label')
            # self.window_title('Title: {}'.format(identifier))
            self.axes.set_title('Title: {}'.format(identifier))
            self.draw()
        # print(y1_data)
        # self.line.set_data()
        # self.line.setx(x_vec)
        self.line.sety(y1_data)
        # self.line.set_data(x_vec, y1_data)
        # #check the value of y1_data and and it showing it ambigous
        self.axes.set_xlim(np.min(x_vec), np.max(x_vec))
        # print(y1_data)
        # print(self.line.axes.get_ylim()[0])
        if np.min(y1_data) <= self.line.axes.get_ylim()[0] or np.max(
                y1_data) >= self.line.axes.get_ylim()[1]:
            self.axes.set_ylim([
                np.min(y1_data) - np.std(y1_data),
                np.max(y1_data) + np.std(y1_data)
            ])
        # plt.pause(pause_time)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        mydateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d")
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.data = pd.read_csv(
            "C:/Users/shyam/Documents/aditya/Project/HDFC.csv",
            index_col="Date",
            parse_dates=["Date"],
            date_parser=mydateparser)[["Close"]].round(2)
        # self.data = pd.read_csv(
        #     "C:/Users/shyam/Documents/aditya/Project/HDFC.csv",
        #     index_col="Date")
        self.canvas = MplCanvas(
            self,
            width=5,
            height=4,
            dpi=100,
        )
        self.data.plot(ax=self.canvas.axes)
        # self.data.index = pd.to_datetime(self.data.index)
        self.setCentralWidget(self.canvas)
        # self.xdata = list(range(50))
        # self.ydata = [random.randint(0, 10) for i in range(50)]

        x, y = separation(self.data)
        # # index = self.data.index.map(
        # #     lambda x: datetime.strptime(str(x), "%Y-%m-%d "))
        self.canvas.axes.plot(x, y, "g")
        self.canvas.draw()
        # self.canvas.plotting(x, y)
        # print(self.canvas.axes.get_yaxis())
        # self.update_plot()
        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start()
        # self.show()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        # Note: we no longer need to clear the axis.
        x = self.data[['Close']].tail(1)
        x = x.to_dict()["Close"].values()
        for i in x:
            x = i
        print(x)
        y_data = np.append(self.ref.get_ydata(), x)
        x_data = np.append(self.ref.get_xdata(), str(self.data.index[-1]))

        self.canvas.plotting(x_data, y_data)
        self._plot_ref.set_xdata(x_data)
        self._plot_ref.set_ydata(y_data)
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            self.ydata = self.data[['Date']]
            plot_ref = self.canvas.axes.plot(self.xdata, self.ydata, "r")
            self._plot_ref = plot_ref[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self.ydata = self.data[['Date']].append(self.data[['Date'
                                                               ]].tail(1))
            self._plot_ref.set_ydata(self.ydata)
        # Trigger the canvas to update and redraw.
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()

# import sys
# import time
# import yfinance as yf
# import numpy as np
# import pandas as pd

# # from matplotlib.backends.qt_compat import QtWidgets
# from PyQt6 import QtWidgets
# from matplotlib.backends.backend_qtagg import (FigureCanvas,
#                                                NavigationToolbar2QT as
#                                                NavigationToolbar)
# from matplotlib.figure import Figure

# class ApplicationWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self._main = QtWidgets.QWidget()
#         self.setCentralWidget(self._main)
#         layout = QtWidgets.QVBoxLayout(self._main)

#         self.data = pd.read_csv(
#             "C:/Users/shyam/Documents/aditya/Project/HDFC.csv",
#             index_col="Date")

#         # data = yf.download(tickers="HDFC.NS",
#         #                    period='1d',
#         #                    interval='5m',
#         #                    group_by='ticker')
#         # self.close_data = data[['Close']]
#         # print(self.close_data)
#         static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
#         # Ideally one would use self.addToolBar here, but it is slightly
#         # incompatible between PyQt6 and other bindings, so we just add the
#         # toolbar as a plain widget instead.
#         # layout.addWidget(NavigationToolbar(static_canvas, self))
#         layout.addWidget(static_canvas)

#         dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
#         layout.addWidget(dynamic_canvas)
#         # layout.addWidget(NavigationToolbar(dynamic_canvas, self))

#         self._static_ax = static_canvas.figure.subplots()
#         self._static_ax.plot(self.data.index, self.data[["Close"]])
#         # t = np.linspace(0, 10, 501)
#         # self._static_ax.plot(t, np.tan(t), ".")

#         self._dynamic_ax = dynamic_canvas.figure.subplots()
#         # t = np.linspace(0, 10, 101)
#         # Set up a Line2D.
#         # self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))
#         self._line, = self._dynamic_ax.plot(self.data.index,
#                                             self.data[['Close']])
#         self._timer = dynamic_canvas.new_timer(1000)
#         self._timer.add_callback(self._update_canvas)
#         self._timer.start()

#     def _update_canvas(self):
#         # t = np.linspace(0, 10, 101)
#         # Shift the sinusoid as a function of time.
#         # print(self.data.tail(1))
#         a = self.data.tail(1)
#         # self._line.set_data(self.close_data.index, self.close_data['Close'])
#         # a = np.sin(t + time.time())
#         # print(self._line.get_xdata())

#         self._line.set_xdata(np.append(self._line.get_xdata(), a.index))
#         self._line.set_ydata(np.append(self._line.get_ydata(), a["Close"]))

#         self._line.figure.canvas.draw()

# if __name__ == "__main__":
#     # Check whether there is already a running QApplication (e.g., if running
#     # from an IDE).
#     qapp = QtWidgets.QApplication.instance()
#     if not qapp:
#         qapp = QtWidgets.QApplication(sys.argv)

#     app = ApplicationWindow()
#     app.show()
#     app.activateWindow()
#     app.raise_()
#     qapp.exec()

# ## testing to store data of user

# # import pickle

# # user = {
# #     "Name": "",
# #     "NickName": "",
# #     "Wallet": 10000,
# #     "Favorites": [],
# #     "MyStocks": [],
# #     "UserID": 0,
# #     "SessionValid": True
# # }
# # with open(
# #         "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/userInfo.txt",
# #         'wb') as op:
# #     print("Im start writhing")
# #     op.write(pickle.dumps(user))
# #     print("DOne writing")
# #     op.close()
# # print("Im DOne")

# # with open(
# #         "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/userInfo.txt",
# #         'rb') as op:
# #     print("Im start reading")
# #     user1 = op.readlines()
# #     user1 = pickle.loads(user1[0])
# #     print("DOne Reading")
# #     op.close()
# # print(user1)

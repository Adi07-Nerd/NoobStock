from tkinter.font import names
import yfinance as yf
import pandas as pd


class Stocks(yf):
    def __init__(self):
        super().__init__()
        # self.aboutStock = {}

    def getStock(self, name, multi=False):
        aboutStock = ()
        if self.multi:
            aboutStock = name, multi, self.ticker.Tickers(name)
        else:
            aboutStock = name, self.ticker.Ticker(name), multi
        return aboutStock

    # def __repr__(self) -> str:
    #     return ((super().__str__()).split())[-1]

    def getPic(self, aboutStock):
        names = aboutStock[0]
        isMultiple = aboutStock[1]
        tickerValue = aboutStock[2]
        urlDict = {}
        if isMultiple:
            for i in names.split():
                # self.aboutStock.tickers[name.split()[0].info['logo_url']]
                urlDict[i] = tickerValue.tickers[i.info['logo_url']]
            return urlDict
        else:
            # self.aboutStock.info['logo_url']
            return tickerValue.tickers[names.info['logo_url']]

    def getName(self, aboutStock):
        names = aboutStock[0]
        isMultiple = aboutStock[1]
        tickerValue = aboutStock[2]
        nameDict = {}
        if isMultiple:
            for i in names.split():
                nameDict[i] = tickerValue.tickers[i.info['shortName']]
                # self.aboutStock.tickers[self.name.split()[1].info['shortName']]
            return nameDict
        else:
            return tickerValue.tickers[names.info['logo_url']]

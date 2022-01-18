import yfinance as yf
import pandas as pd


class Stocks(yf):
    def __init__(self, a):
        super().__init__()
        self.name = a
        self.multi = False
        self.aboutStock

    def getStock(self):
        if len(self.name.split()) == 1:
            self.aboutStock = self.ticker.Ticker(self.name)
        elif len(self.name.split()) > 1:
            self.multi = True
            self.aboutStock = self.ticker.Tickers(self.name)

    def __repr__(self) -> str:
        return ((super().__str__()).split())[-1]

    def getPic(self):
        if self.multi:
            self.aboutStock.tickers[self.name.split()[0].info['logo_url']]
            self.aboutStock.tickers[self.name.split()[1].info['logo_url']]
        else:
            self.aboutStock.info['logo_url']

    def getName(self):
        if self.multi:
            self.aboutStock.tickers[self.name.split()[0].info['shortName']]
            self.aboutStock.tickers[self.name.split()[1].info['shortName']]
        else:
            self.aboutStock.info['shortName']

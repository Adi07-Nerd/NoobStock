### this class will contain the yahoofinance function.
import yfinance as yf
import pickle
import pandas as pd


class DataProvider():
    def __init__(self):
        self.tickers, self.tickerModel = self.__tickerList__()

    def getData(self, c_name, hardcoded=None, interval="1mo", period="1y"):
        if hardcoded == None:
            ticker = self.getTickerValue(c_name)
        else:
            ticker = hardcoded
        mydateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d")
        result = pd.read_csv(
            "C:/Users/shyam/Documents/aditya/Project/HDFC.csv",
            index_col="Date",
            parse_dates=["Date"],
            date_parser=mydateparser)[["Close"]].round(2)
        # result = yf.download(ticker,
        #                      interval=interval,
        #                      period=period,
        #                      rounding=True)
        return self.separating(result), c_name
        # else:
        #     result=yf.download()

    def separating(self, value):
        # value[["Close"]].round(2)  #this will round of the value
        #this will make proper dictionary
        value = list(value.to_dict().values())[0]
        #1. will return all the dates 2. will return all the stock value
        return [x.timestamp() for x in value.keys()], list(value.values())

    def __tickerList__(self):
        with open(
                "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/tickerlist.txt",
                "rb") as file:
            data = file.read()
            data = pickle.loads(data)  #this contains valid tickers to search

            file.close()
            words = []  #this has tickers name to show user
            for i, j in data.items():
                for a in j:
                    #spliting and finding who belongs to which exchanges
                    if (a.split(".")[1] == "NS"):
                        words.append(i + " " + "(NSE)")
                    else:
                        words.append(i + " " + "(BSE)")
            return data, words

    def getTickerValue(self, stock):
        ############
        # make sure your main HomeWindow object is store in main only
        # This function takes search text and result its ticker to search from yahoo finance
        ######
        splited = stock.split(" ")
        name = " ".join(splited[:-1])  #this will add stock name to name
        options = self.tickers[
            name]  #this will search for value(ticker) of stock name
        if (len(options) > 1):
            return "".join(options[0] if splited[-1] ==
                           "(NSE)" else options[1])
        else:
            return "".join(options)